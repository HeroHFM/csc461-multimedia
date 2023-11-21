---
layout: default
---

# Bi-Weekly Update 3: WebRTC
## Nov 06 - Nov 20
## Victor K., Matthew D.

> These past two weeks, we worked on transmitting voice over WebRTC.

## WebRTC
[WebRTC](https://webrtc.org/) is an open-source project created to simplify the task of transmitting audio, video, and other arbitrary data over the internet. We have chosen to take a closer look at WebRTC in particular due to its strong support base in modern web browsers and its ubiquitous use in modern voice chat applications such as Discord, Zoom, Microsoft Teams, and Google Meet. It is important to note that WebRTC is not itself a protocol, but rather a standardized interface (JavaScript API) to a collection of protocols that have been in use for a long time for real-time communication. We will mainly focus on the facilities of WebRTC that allow for connection establishment and voice communication.

In order to establish a peer-to-peer voice communication channel, several protocols are at play. To first establish a connection, a signaling protocol must be used to negotiate the parameters of the connection with the other peer. Although WebRTC provides functionality to construct a Session Description Protocol (SDP) offer, it does not specify the signaling protocol used to transmit the offer and to receive an SDP answer from the remote peer. Traditionally, protocols such as the Session Initiation Protocol (SIP) are used for this purpose, but anything that can transmit plain text can be used.

Since WebRTC is often used in peer-to-peer contexts, NAT traversal is a core component of the API. Connections in WebRTC use Interactive Connectivity Establishment (ICE) in order to establish and maintain a connection. This includes the use of Session Traversal Utilities for NAT (STUN) to establish whether a peer is behind a NAT, to query for the public IP address and UDP port, and to keep the connection alive. In addition, a Traversal Using Relay NAT (TURN) server can be specified to relay traffic if a connection fails to be established. Even if UDP traffic is completely blocked, a TURN server can relay traffic over TCP.

Accessing devices such as a microphone on the host system is also provided for by WebRTC. Audio streams use SRTP and SRTCP (secure variants of RTP and RTCP respectively) over UDP along with DTLS (the TLS equivalent for UDP datagrams) for key exchange since WebRTC traffic is required to be encrypted. Although RTP and RTCP typically use consecutive ports, one port is multiplexed to support both since fewer ports are better for NAT traversal.

## A Simple WebRTC Server/Client Example
For our demonstration, we want to emulate a bi-directional voice call and experiment with how it performs under varying network conditions, as one of the benefits of WebRTC is its support for [adaptive bitrate streaming with the OPUS codec](https://hpbn.co/webrtc/#audio-opus-and-video-vp8-bitrates). In our implementation, we will use the [`aiortc` project](https://aiortc.readthedocs.io/en/latest/index.html) that is an implementation of the WebRTC API using Python3’s `asyncio` library. The advantages of this approach were discussed in the recent [Midterm Update](midterm-update.md).
The project provides an [example](https://github.com/aiortc/aiortc/tree/main/examples/server) of `aiortc` used in a JavaScript client and Python server which will be our starting point for the implementation.

## Establishing a Connection
To begin, we have stripped out all of the code that does not pertain to voice. In the current configuration, the client and the server are hosted on the same server. This means that for a local connection, we do not need to use ICE for NAT traversal. However, Google’s public STUN server (`stun:stun.l.google.com:19302`) is used anyway.

In order to create a connection to a peer, we must create an `RTCPeerConnection`. Next, we add an audio track using `navigator.mediaDevices.getUserMedia()` and add the voice track to the peer connection. This will be used to send and receive audio. Now, we can generate a SDP offer. Since we do not have a SIP server set up, the current code is using an HTTP POST request to send the offer from the client to the server. The server will respond with the SDP answer. This is, in effect, SDP over HTTP.

This is the offer generated:

```
v=0
o=- 8498233979625313580 2 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE 0
a=extmap-allow-mixed
a=msid-semantic: WMS 140ad551-512d-4ebe-8fad-04f60ccd1caf
m=audio 55175 UDP/TLS/RTP/SAVPF 111 63 9 0 8 13 110 126
c=IN IP4 192.168.3.106
a=rtcp:9 IN IP4 0.0.0.0
a=candidate:3742922256 1 udp 2122260223 192.168.3.106 55175 typ host generation 0 network-id 1 network-cost 10
a=candidate:565355140 1 tcp 1518280447 192.168.3.106 9 typ host tcptype active generation 0 network-id 1 network-cost 10
a=ice-ufrag:5DH+
a=ice-pwd:coLPjdqH9norYQpnPyFS4JP9
a=ice-options:trickle
a=fingerprint:sha-256 A6:2E:2E:1F:1E:29:D1:53:B1:71:B5:12:9B:8D:DE:44:B3:48:A0:99:92:42:00:04:A5:6F:F6:A7:59:35:0D:DA
a=setup:actpass
a=mid:0
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time
a=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=sendrecv
a=msid:140ad551-512d-4ebe-8fad-04f60ccd1caf 96260768-0bcc-40ac-ade0-9d89c4f1514d
a=rtcp-mux
a=rtpmap:111 opus/48000/2
a=rtcp-fb:111 transport-cc
a=fmtp:111 minptime=10;useinbandfec=1
a=rtpmap:63 red/48000/2
a=fmtp:63 111/111
a=rtpmap:9 G722/8000
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:13 CN/8000
a=rtpmap:110 telephone-event/48000
a=rtpmap:126 telephone-event/8000
a=ssrc:2962455826 cname:QCVZMO/hYO4WHDB0
a=ssrc:2962455826 msid:140ad551-512d-4ebe-8fad-04f60ccd1caf 96260768-0bcc-40ac-ade0-9d89c4f1514d
```

We can see the various ICE candidates (`a=candidate` lines, listing an IP address, port and protocol) that will be considered to establish a connection, as well as the media format (`a=rtpmap:111 opus/48000/2`) and other information (such as the port multiplexing `a=rtcp-mux`). The server then creates its own `RTCPeerConnection` based on the description provided by the client and responds with an answer:

```
v=0
o=- 3909534172 3909534172 IN IP4 0.0.0.0
s=-
t=0 0
a=group:BUNDLE 0
a=msid-semantic:WMS *
m=audio 45632 UDP/TLS/RTP/SAVPF 111 0 8
c=IN IP4 192.168.3.106
a=sendrecv
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=mid:0
a=msid:b8cff6c1-be83-499e-b258-ec158b3aaf87 7f491ad5-f76b-4af9-a09d-f6922ca77662
a=rtcp:9 IN IP4 0.0.0.0
a=rtcp-mux
a=ssrc:3118474735 cname:54fd8049-429c-469a-9dc0-fa318353484d
a=rtpmap:111 opus/48000/2
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=candidate:62072eb9c6e1999dc6bfffd7e63b7452 1 udp 2130706431 192.168.3.106 45632 typ host
a=candidate:b01e63478a980080b68324ebe32767e7 1 udp 1694498815 70.66.224.121 45632 typ srflx raddr 192.168.3.106 rport 45632
a=end-of-candidates
a=ice-ufrag:ljko
a=ice-pwd:T3qJ5NFNo7zgUuyJH6qLeJ
a=fingerprint:sha-256 28:7F:06:CB:23:F7:97:DE:83:6B:39:97:F6:29:EF:54:4C:1A:BA:E5:DE:AE:C6:57:35:2C:79:39:B2:8A:D3:D9
a=setup:active
```

This answer contains the respective candidates for the server, as well as other information about the audio track. Once the connection is established, the peers can now communicate directly.

## Transmitting Voice
There are several ways to get audio from a microphone using Python. The three main ways that we had found were to use [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/), [sounddevice](https://python-sounddevice.readthedocs.io/), and [PyAV](https://github.com/PyAV-Org/PyAV). PyAudio and sounddevice both provide bindings to the port [PortAudio](https://www.portaudio.com/) library and are basically just wrappers for code written in C. PyAV is a wrapper for the [`ffmpeg` library](https://www.ffmpeg.org/).

`aiortc` expects audio data to be streamed in via PyAV frames and there are helper functions that can open a microphone stream using `ffmpeg`. However, this is not portable across operating systems as getting the default microphone on Windows may require a call to the `ffmpeg` command line utility.

Although modules such as PyAudio and sounddevice provide a much more user-friendly interface to select the default microphone and read PCM samples, reading from the microphone involves either a blocking call or a callback (since this is fundamentally a C API). However, `aiortc` uses `asyncio`’s concurrency model based on coroutines. Thus, an adapter must be written to have the callback write to a queue in a thread-safe manner, so that audio frames can be consumed according to `aiortc`’s API. In addition, the raw PCM samples need to be converted into PyAV Frame objects. We have begun to experiment with creating this conversion with PyAudio, although if it proves too troublesome we will stick with PyAV since we know it works.

## Next Steps
Since we have a much better understanding of the WebRTC API, we will work to make the client and server into a single Python script, and work on a more sophisticated signaling system.

