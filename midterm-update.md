---
layout: default
---

# Midterm Update
## Oct 23 - Nov 6
## Victor K., Matthew D.

## Update

The primary focus of our project is building our own basic VoIP system using the existing protocols and standards that power modern, mainstream VoIP applications. VoIP has a long history, with a wide array of standards and protocols that have evolved alongside the internet. To that end, we have chosen to use the WebRTC project, as it is a mature, free, and open-source collection of APIs implemented by all mainstream browsers. WebRTC is already being used by many popular communications platforms such as Discord, Zoom, Microsoft Teams, and Google Meet. Therefore, spending time to understand how it works and implement it will provide us with practical insight into these everyday applications.

Conventionally, WebRTC is used with JavaScript APIs in a web browser. While this makes sense for common usage, we want more control over how WebRTC works and the ability to use our own code for audio processing in a language we are comfortable with. As such, we will be using a Python implementation of WebRTC called [`aiortc`](https://github.com/aiortc/aiortc). This project is very similar to the [official WebRTC standard](https://www.w3.org/TR/webrtc/) (which specifies APIs in ECMAScript), but certain elements have been replaced by constructs more common in Python, such as the use of `asyncio` coroutines from Python’s standard library.

So far, our research has focused on using and exploring the [audio server implementation](https://github.com/aiortc/aiortc/tree/main/examples/server) provided by `aiortc`. This implementation includes a Python server that hosts a website which can stream audio to the web client from a file on the server, along with other features that we will not be focusing on such as video and data transfer. Code for the web client, in JavaScript, is also provided. From both the client and the server, we are able to infer how a WebRTC session is managed, how SDP is used for negotiating a media stream, and ultimately how audio is transmitted from the server to the client. This provides us with a solid baseline which we can improve with our own code to produce a working demo of a two-way VoIP system.

There are still several challenges we need to resolve, however. Instead of streaming audio from a local file, we would like to capture audio input from a microphone attached to the computer, which is necessary for real-time VoIP communication. An additional library to handle this aspect will be needed. Our target VoIP system will also focus on a peer-to-peer model rather than a client-server model, since we want to allow bidirectional communication between parties. Ideally, we can develop an improved Python application that can function as both the client and the server. Our target configuration, then, would involve two copies of our application running on different computers on the same network. Finally, if time permits, we would like to investigate the techniques used in WebRTC to allow direct communication across the internet, including NAT traversal. This will require additional research into protocols like Interactive Connectivity Establishment (ICE), Session Traversal Utilities for NAT (STUN), and Traversal Using Relays around NAT (TURN). The `aiortc` library may already have some limited support for these features.

In terms of our schedule, we have completed our research into the wide selection of VoIP protocols available and will be focusing on the demo for the next several weeks. We hope to have addressed some of the challenges outlined above by the next biweekly update.

- 
