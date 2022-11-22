#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 22:47:02 2022

@author: bene
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

db_url = "https://openuc2-microscope-default-rtdb.europe-west1.firebasedatabase.app/"

api_key = 'AIzaSyB2IdfWKmP-cxOQGqo95bS_cVDGaXGNYqk'

jsonfile = "openuc2-microscope-firebase-adminsdk-a25ih-040a394a22.json"

#% RECEIVER
# Importing required packages
import firebase_admin
from firebase_admin import credentials, db

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

    if str(event.data) == 'hello':
        # /// Execute your code here ///
        print('Data updated as ', str(event.data))

    elif str(event.data) == None:
        # /// Execute your code here ///
        print('Your data has been deleted!')

    # Follow these steps

db.reference('/').listen(listener) # It calls the above listener method(It continuosly listens for the data changes in your database)
# Everytime the data changes, listener function will be called


#%% SENDER 
#!pip install git+https://github.com/ozgur/python-firebase
if(1):
    from firebase import firebase  
    db_url = "https://openuc2-microscope-default-rtdb.europe-west1.firebasedatabase.app/"
    firebase = firebase.FirebaseApplication(db_url, None)  
    data =  { 'task': 'move', 
             'axis': 'X',  
              'steps': 1000,  
              'speed': 100,
              'id':1
              }  
    result = firebase.post('/microscope',data)  
