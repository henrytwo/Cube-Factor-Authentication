from firebase_admin import credentials, firestore, auth
import firebase_admin
import threading
import uuid

cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred)

def listener():
    while True:
        commands = firebase_admin.firestore.client(app=None).collection('queue').get()

        for c in commands:
            command = c.to_dict()

            if command['command'] == 'program':
                pass
            print(command)

            firebase_admin.firestore.client(app=None).collection('queue').document(c.id).delete()

        # do shit here
