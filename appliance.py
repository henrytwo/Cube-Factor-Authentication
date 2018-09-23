from firebase_admin import credentials, firestore, auth
import firebase_admin
import threading
import uuid
import crypto

cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred)

def scan():
    return [0, 0, 0]

def program_cube(name):
    cube_pattern = scan()

    cr

    firebase_admin.firestore.client(app=None).collection('queue').document(name).set({'command':'program', 'name': name})


def listener():
    while True:
        commands = firebase_admin.firestore.client(app=None).collection('queue').get()

        for c in commands:

            command = c.to_dict()

            if command['command'] == 'program':
                pass

            print('Incoming command...', c.id, command)

            firebase_admin.firestore.client(app=None).collection('queue').document(c.id).delete()

if __name__ == '__main__':
    threading.Thread(target=listener).start()
