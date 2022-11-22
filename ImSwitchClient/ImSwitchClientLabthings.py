#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 14:29:05 2022

@author: bene
"""

#%%
import Pyro5.api
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

import uvicorn
from _serialize import register_serializers

import io
from starlette.responses import StreamingResponse



# Initialize the app
app = FastAPI()


'''
class Pipette(BaseModel):
    name: str
    position: str
'''

register_serializers()
uri = 'PYRO:ImSwitchServer@127.0.0.1:54333'
imswitchServer = Pyro5.api.Proxy(uri)


@app.post('/camera/liveview')
async def liveview(isrunning: bool):
    print("Switching Liveview")
    imswitchServer.exec("ViewController", "liveview", [isrunning])
    return {"Message" : "Switching Liveview"}

@app.get('/camera/frame')
async def getframe():
    print("get frame")
    image = imswitchServer.get_image()
    print(image)
    return image

@app.post("/camera/frame2")
async def image_endpoint(*, vector):
    # Returns a cv2 image array from the document vector
    cv2img = imswitchServer.get_image()
    res, im_png = cv2.imencode(".png", cv2img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")




if __name__ == "__main__":
    uvicorn.run(app, host="10.34.178.175", port=88)
