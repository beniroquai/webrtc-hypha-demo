import firebase_admin
from firebase_admin import credentials, db
import Pyro5.api
from _serialize import register_serializers
import requests 

TIMEOUT = 1
baseurl = "http://127.0.0.1:8000"
def move(steps=1000, axis="X", isAbsolute=False):
    endoint = "/PositionerController/movePositioner"
    payload = {
        "positionerName": "ESP32Stage",
        "axis": axis, 
        "isAbsolute": isAbsolute, 
        "dist": steps
        }
    return requests.get(baseurl+endoint, params=payload, timeout=TIMEOUT)

    
# Firebase-related settings
db_url = "https://openuc2-microscope-default-rtdb.europe-west1.firebasedatabase.app/"
api_key = 'AIzaSyB2IdfWKmP-cxOQGqo95bS_cVDGaXGNYqk'
jsonfile = "cred.json"

# setting up imsiwtch
register_serializers()
uri = 'PYRO:ImSwitchServer@0.0.0.0:54333'
imswitchServer = Pyro5.api.Proxy(uri)
try:
    imswitchServer.exec("ViewController", "liveview", [True])
except Exception as e:
    print(e)
    pass

# Initializing the database with URL
cred = credentials.Certificate(jsonfile)
firebase_admin.initialize_app(cred,{
    'databaseURL': db_url
}) 


def listener(event):
    print(event.event_type)  # Indicates the type of the event done
    print(event.path)  # References the path of the event
    print(event.data)  # Gives the UPDATED DATA, None if deleted

    # Now, executing specific functions based on the new data(UPDATED DATA)

    if "task" in event.data:
        if event.data["task"] == 'move':
            steps = event.data["steps"]
            speed = event.data["speed"]
            axis = event.data["axis"]
            try:
                move(steps=steps, axis=axis, isAbsolute=False)
            except Exception as e:
                print(e)
                pass

db.reference('/').listen(listener) # It calls the above listener method(It continuosly listens for the data changes in your database)
# Everytime the data changes, listener function will be called
