#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 14:29:05 2022

@author: bene
"""
'''
import Pyro5.api


class imswitchclient(object):
    
    def __init__(self, url="127.0.0.1", port="54333"):
        self.uri = 'PYRO:ImSwitchServer@1'+url+port
        self.imswitchServer = Pyro5.api.Proxy(uri)

    def enableLiveview(self, enable=True):
        # start/stop live view
        self.imswitchServer.receive("ViewController", "liveview", enable)

    def move(self, axis="X", steps=1, stagetype='LightsheetStage'):
        # move x/y
        self.imswitchServer.receive("PositionerController", "move", (stagetype, axis, steps))

# snap image
imswitchServer.receive("RecordingController", "snap", ())

# snap image with return matrix
imswitchServer.receive("RecordingController", "snapNumpy", ())

# turn on/off laser
imswitchServer.receive("LaserController", "move", ("LightsheetStage", "X", 1))
setLaserActive(self, laserName: str, active: bool) -> None:

    setLaserValue(self, laserName: str, value: Union[int, float]) -> None:

# we can draw from these controllers
from .AlignAverageController import AlignAverageController
from .AlignXYController import AlignXYController
from .AlignmentLineController import AlignmentLineController
from .BeadRecController import BeadRecController
from .ConsoleController import ConsoleController
from .FFTController import FFTController
from .FocusLockController import FocusLockController
from .AufofocusController import AutofocusController
from .ImageController import ImageController
from .LaserController import LaserController
from .PositionerController import PositionerController
from .RecordingController import RecordingController
from .SLMController import SLMController
from .ScanController import ScanController
from .SettingsController import SettingsController
from .ULensesController import ULensesController
from .ViewController import ViewController
from .WellPlateController import WellPlateController
'''
#%%
import Pyro5.api
from _serialize import register_serializers

register_serializers()
ipaddress = "0.0.0.0"
#ipaddress = "192.168.2.162"
uri = 'PYRO:ImSwitchServer@'+ipaddress+':54333'
imswitchServer = Pyro5.api.Proxy(uri)
imswitchServer.exec("ViewController", "liveview", [True])
#imswitchServer.exec("ViewController", "liveview", [False])
imswitchServer.move(positionerName=None, axis="X", dist=1000) 
imswitchServer.move(positionerName=None, axis="Y", dist=1000) 
image = imswitchServer.get_image()