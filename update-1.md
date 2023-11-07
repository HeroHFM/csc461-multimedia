---
layout: default
---

# Bi-Weekly Update 1: Survey of VoIP Protocols
## Oct 09 - Oct 23
## Victor K., Matthew D.

> For this week, we surveyed some common VoIP protocols to get an idea of the landscape of internet-mediated telephony. 

## Intro
Voice over Internet Protocol (VoIP) is not a single protocol as the name might imply, but rather a collection of different protocols and standards that have evolved over time in order to facilitate voice communication over the internet. We have taken a selection of protocols that are commonly associated with VoIP, and summarized them below.

## H.323
H.323, formally titled “Packet-Based Multimedia Communications Systems”, is one of the oldest VoIP standards. It was originally published by the ITU-T in 1996, but the most recent version was published in 2022. It describes the use of several ITU-T and IETF protocols that can be used together to facilitate multimedia communication over a variety of mediums, including the internet. The protocols used in H.323 are binary in order to facilitate efficient message processing.

The most basic element of an H.323 system is the terminal, which is the device (or software) used to make a call. Gateways allow communication to flow between the H.323 network and other networks, such as the PSTN. Gatekeepers provide additional optional services such as address resolution, which allows two terminals to communicate without knowing each others’ IP addresses ahead of time.

To communicate with the gatekeepers, terminals use the H.225.0 Registration, Admission and Status (RAS) protocol. Once the address of the remote endpoint is known, the H.225.0 Call Signaling protocol is used to establish a connection. H.245 is the control protocol that manages and describes the multimedia communication used. It can be tunneled within H.225.0 messages for ease of firewall traversal. Finally, the Real-time Transport Protocol (RTP) is used for sending and receiving multimedia payloads between terminals. This makes H.323 one of the first standards to adopt RTP. However, with the development of newer and simpler protocols like SIP, H.323 usage has been declining.

## SIP
The Session Initiation Protocol (SIP), standardized as RFC 2543 in 1999, serves a critical role in many different multimedia and communication systems. SIP is a signaling protocol, which is used by hosts to initiate, maintain, and terminate single or multi-party communication sessions. Although this protocol is very popular in internet telephony in particular, it has applications in other forms of multimedia communication such as video conferencing or instant messaging. Essentially, SIP functions as an out-of-band signaling mechanism for a party to “invite” another party to start a call, at which point a protocol like RTP may be used to send the actual data payload. The SIP protocol can then be used to terminate the connection.

SIP is an application-layer text-based protocol (much like HTTP and SMTP) designed to be transport-layer protocol agnostic, and thus can function over TCP and UDP, among others, and be encrypted with TLS. SIP messages can contain data such as text messages, bypassing the need for a separate stream, and can be used with the Session Description Protocol (SDP) in order to negotiate the parameters of the communication such as codecs. A request-response transaction model underpins SIP communication. 

Resources on a SIP network are identified by a web-style Uniform Resource Identifier (URI). An endpoint in a SIP network is termed a user agent (UA), which can serve the role of client when requesting a service function from another, or a server when responding to a request. Although two user agents are enough for simple SIP communication, a more comprehensive infrastructure is typically used in order to provide directory services and interoperate between other networks such as the PSTN.

## XMPP
The Extensible Messaging and Presence Protocol (XMPP), originally known as Jabber, makes use of Extensible Markup Language (XML) to allow for instant messaging between clients. The protocol is designed entirely in the application layer and is decentralized, requiring no master server; everyone is free to run their own server by creating the appropriate SRV records for their domain. Users connect to one another using an address called a JID, which closely resembles an email address.

An important aspect of XMPP is that it is extensible. Although anyone can create an extension, the XMPP Standards Foundation (XSF) manages common extensions known as XMPP Extension Protocols (XEPs) to maintain interoperability between implementations. A particularly important extension is XEP-0166, otherwise known as Jingle, which allows for direct peer-to-peer communication for multimedia purposes such as VoIP or videoconferencing. Jingle handles session control and signaling, while RTP is used to deliver the multimedia payload.

XMPP and Jingle have seen widespread usage in a variety of applications. Google Talk (which has since been discontinued) used XMPP for instant messaging and developed the Jingle extension for voice and file transfer, before releasing Jingle publicly under a permissive license. Gaming platforms such as Playstation and Origin use XMPP to allow private chat between users. Many general-purpose XMPP clients exist, too, to serve as a replacement for older protocols and software.

## RTP
The Real-time Transport Protocol (RTP) is one of the most important protocols involved in VoIP communication, as RTP facilitates the end-to-end transfer of the underlying media being communicated (be it voice, video or other multimedia). RTP was developed alongside SIP, SDP, and Session Announcement Protocol (SAP) by the IETF in the early 1990s and was first published in 1996 (RFC 1889), with an update in 2003 (RFC 3550).

RDP is an application-layer protocol, conventionally run over UDP. Since most multimedia applications are more sensitive to jitter and delay than regular internet traffic, RTP is rarely used with TCP. Thus, it implements its own provisions for both packet loss and reordering. Since RTP is real-time, packets carry timestamps for synchronization, in addition to sequence numbers. It is also common for an additional RTP stream to be opened per media type (i.e. separate streams for audio and video). To monitor the statistics about the transmission, the RTP Control Protocol (RTCP) is utilized.

## WebRTC
Web Real-Time Communication (WebRTC) is a free and open-source project born out of Google’s acquisition of Global IP Solutions, a VoIP software company, in 2010. The first specification was subsequently drafted by the W3C in 2011. WebRTC provides an API—now supported by most modern browsers—for real-time, peer-to-peer audio and video transmission. Since many modern chat apps such as Discord are browser-based, WebRTC has seen wide adoption in this domain, separate (although compatible) with other VoIP infrastructure. WebRTC does not provide signaling, relying instead on protocols such as SIP or XMPP to facilitate connections between peers. Data transfer via WebRTC relies on other protocols such as RTP.
