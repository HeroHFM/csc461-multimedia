#!/usr/bin/env python3

# Modified from https://github.com/aiortc/aiortc/tree/main/examples/server

import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid

from aiohttp import web, ClientSession
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay
from av import VideoFrame

ROOT = os.path.dirname(__file__)
peer_connections = set()
logger = logging.getLogger("pc")

SIGNAL_URL = 'http://localhost:8080/offer'
PLAYER = {"file": "default", "format" : "alsa"}
RECORDER = {"file": "default", "format" : "alsa"} # dshow for windows

### Web Server

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    peer_connections.add(pc)

    log_info = lambda msg, *args: logger.info(pc_id + " " + msg, *args)

    log_info("Created for %s", request.remote)

    # Prepare Local Media
    player   = MediaPlayer(**PLAYER)
    recorder = MediaRecorder(**RECORDER)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        log_info("Connection state is %s", pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            peer_connections.discard(pc)

    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)

        if track.kind == "audio":
            pc.addTrack(player.audio)
            recorder.addTrack(track)
        else:
            raise Exception("Non-audio track")

        @track.on("ended")
        async def on_ended():
            log_info("Track %s ended", track.kind)
            await player.close()
            await recorder.stop()

    # Handle Offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # Send Answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )

# Close Peer Connections
async def on_shutdown(app):
    coros = [pc.close() for pc in peer_connections]
    await asyncio.gather(*coros)
    peer_connections.clear()

async def connect():

    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    log_info = lambda msg, *args: logger.info(pc_id + " " + msg, *args)

    # Create peer connection
    
    config = RTCConfiguration([RTCIceServer("stun:stun.l.google.com:19302")])
    pc = RTCPeerConnection(config)
    peer_connections.add(pc)

    player = MediaPlayer(**PLAYER)
    pc.addTrack(player.audio)
    recorder = MediaRecorder(**RECORDER)

    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)

        if track.kind == "audio":
            recorder.addTrack(track)
        else:
            raise Exception("Non-audio track")

        @track.on("ended")
        async def on_ended():
            log_info("Track %s ended", track.kind)
            await player.close()
            await recorder.stop()

    await pc.setLocalDescription(await pc.createOffer())

    async with ClientSession() as session:
        async with session.post(SIGNAL_URL, json={"sdp" : pc.localDescription.sdp, "type" : pc.localDescription.type}) as resp:
            print(resp.status)
            answer = json.loads(await resp.text())
            await pc.setRemoteDescription(RTCSessionDescription(answer["sdp"], answer["type"]))

    await recorder.start()
    await asyncio.sleep(600)

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description = "VOIP Demo")

    parser.add_argument("--cert-file", help = "SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help = "SSL key file (for HTTPS)")
    
    parser.add_argument("--host", default="0.0.0.0", help="Host for HTTP server (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Port for HTTP server (default: 8080)")

    parser.add_argument("--verbose", "-v", action="count")

    parser.add_argument("--connect", "-c", action="store_true", help="Initiate connection")
    
    args = parser.parse_args()

    # Configure logging level
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    # SSL
    if args.cert_file:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(args.cert_file, args.key_file)
    else:
        ssl_context = None

    # Go!
    if args.connect:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(connect())
    else: # Spin up web server, wait for incomming connection
        app = web.Application()
        app.on_shutdown.append(on_shutdown)
        app.router.add_post("/offer", offer)
        web.run_app(
            app, access_log=None, host=args.host, port=args.port, ssl_context=ssl_context
        )