#!pip install nest_asyncio
import argparse
import asyncio
import logging
import os
import uuid
import fractions
import cv2

import numpy as np
from av import VideoFrame
from imjoy_rpc.hypha import connect_to_server

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription

ROOT = os.path.dirname(__file__)

logger = logging.getLogger("pc")
pcs = set()


#!pip install Pyro5
#!pip install useq-schema
import Pyro5.api
from _serialize import register_serializers

register_serializers()
uri = 'PYRO:ImSwitchServer@0.0.0.0:54333'
imswitchServer = Pyro5.api.Proxy(uri)
imswitchServer.exec("ViewController", "liveview", [True])
imswitchServer.exec("ViewController", "liveview", [False])




class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, transform):
        super().__init__()  # don't forget this!
        self.transform = transform
        self.count = 0

    async def recv(self):
        # frame = await self.track.recv()
        img = np.uint8(imswitchServer.get_image())

        img = img[:200,:200]
        
        img = cv2.normalize(img,img,0,255,cv2.NORM_MINMAX) 
        
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = self.count # frame.pts
        self.count+=1
        new_frame.time_base = fractions.Fraction(1, 1000)
        return new_frame

async def offer(params, context=None):
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pcs.add(pc)

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    log_info("Created for offer")

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            if isinstance(message, str) and message.startswith("ping"):
                channel.send("pong" + message[4:])
            elif message in ["right", "left", "up", "down"]:
                print(f"===> command received: {message}")
                if message=="right":
                    imswitchServer.move(positionerName=None, axis="X", dist=1000)
                if message=="left":
                    imswitchServer.move(positionerName=None, axis="X", dist=-1000)
                if message=="up":
                    imswitchServer.move(positionerName=None, axis="Y", dist=1000)
                if message=="down":
                    imswitchServer.move(positionerName=None, axis="Y", dist=-1000)
                    
                    
                # pc.transport.send(message.encode())
                channel.send("completed")

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        log_info("Connection state is %s", pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)
        pc.addTrack(
            VideoTransformTrack(transform=params["video_transform"]
            )
        )
        @track.on("ended")
        async def on_ended():
            log_info("Track %s ended", track.kind)

    # handle offer
    await pc.setRemoteDescription(offer)

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}


async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


async def start_service(service_id, workspace=None, token=None):
    client_id = service_id + "-client"
    print(f"Starting service...")
    server = await connect_to_server(
        {
            "client_id": client_id,
            "server_url": "https://ai.imjoy.io/",
            "workspace": workspace,
            "token": token,
        }
    )
    
    
    # print("Workspace: ", workspace, "Token:", await server.generate_token({"expires_in": 3600*24*100}))
    await server.register_service(
        {
            "id": service_id,
            "config": {
                "visibility": "public",
                "require_context": True,
            },
            "offer": offer,
        }
    )
    async def turn_on():
        await print("Turn on") #svc.show_status("turn 222")

    print(
        f"Service (client_id={client_id}, service_id={service_id}) started successfully, available at https://ai.imjoy.io/{server.config.workspace}/services"
    )
    print(f"You can access the webrtc stream at https://oeway.github.io/webrtc-hypha-demo/?service_id={service_id}")

if __name__ == "__main__":
    #parser = argparse.ArgumentParser(
    #    description="WebRTC demo for video streaming"
    #)
    #parser.add_argument("--service-id", type=str, default="aiortc-demo", help="The service id")
    #parser.add_argument("--verbose", "-v", action="count")
    #args = parser.parse_args()

    #import nest_asyncio
    #nest_asyncio.apply()
    if 1:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.create_task(start_service(
        "UC2ImSwitch",
        workspace=None,
        token=None,
    ))
    loop.run_forever()

    
