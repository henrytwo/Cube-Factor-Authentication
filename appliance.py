from firebase_admin import credentials, firestore, auth
import firebase_admin
import threading
import uuid
import crypto
import traceback

cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred)

def scan():
    return [0, 0, 0]

def program_cube(request_id, name):
    cube_pattern = scan()

    c = crypto.Cube(cube_pattern)
    c.generate_pair()

    firebase_admin.firestore.client(app=None).collection('cubes').document(name).set(c.export_pair())
    firebase_admin.firestore.client(app=None).collection('callback').document(request_id).set({'response' : 'Key successfully generated'})


def listener():
    while True:
        try:
            commands = firebase_admin.firestore.client(app=None).collection('queue').get()

            for c in commands:

                command = c.to_dict()

                print(command)

                if command['command'] == 'program':
                    program_cube(c.id, command['name'])
                    pass

                print('Incoming command...', c.id, command)

                firebase_admin.firestore.client(app=None).collection('queue').document(c.id).delete()
        except:
            print('Something broke...')
            traceback.print_exc()

if __name__ == '__main__':
    threading.Thread(target=listener).start()
