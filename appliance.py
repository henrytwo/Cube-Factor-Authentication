from firebase_admin import credentials, firestore, auth
import firebase_admin
import threading
import uuid
import crypto
import traceback
import pyotp
import time

cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred)

def scan():
    return [0, 0, 0]

def decrypt_code(request_id, encrypted_secret, cube_name):

    try:
        cubes = firebase_admin.firestore.client(app=None).collection('cubes').get()

        for cube in cubes:
            if cube.id == cube_name:

                print('Cube found!')

                cube_pattern = scan()

                c = crypto.Cube(cube_pattern)
                c.import_pair(cube.to_dict())

                decrypted_code = c.decrypt(encrypted_secret)

                print(decrypted_code)

                code_generator = pyotp.TOTP(decrypted_code)
                print('Current code:', code_generator.now())

                firebase_admin.firestore.client(app=None).collection('callback').document(request_id).set(
                    {'response': 'Secret successfully decrypted'})

                break

        else:
            print('shit, can\'t find the cube!')
            firebase_admin.firestore.client(app=None).collection('callback').document(request_id).set(
                {'response': 'Decryption failed'})
    except:
        firebase_admin.firestore.client(app=None).collection('callback').document(request_id).set(
                        {'response': 'Decryption failed'})

def program_cube(request_id, name):

    try:
        cube_pattern = scan()

        c = crypto.Cube(cube_pattern)
        c.generate_pair()

        firebase_admin.firestore.client(app=None).collection('cubes').document(name).set(c.export_pair())
        firebase_admin.firestore.client(app=None).collection('callback').document(request_id).set({'response' : 'Key successfully generated'})
    except:
        traceback.print_exc()
        firebase_admin.firestore.client(app=None).collection('callback').document(request_id).set(
            {'response': 'boi something went wrong'})


def listener():
    while True:
        try:
            commands = firebase_admin.firestore.client(app=None).collection('queue').get()

            for c in commands:

                command = c.to_dict()

                #print(command)

                if command['command'] == 'program':
                    program_cube(c.id, command['name'])
                elif command['command'] == 'decrypt':
                    decrypt_code(command['request_id'], command['code'], command['cube'])

                print('Incoming command...', c.id)

                firebase_admin.firestore.client(app=None).collection('queue').document(c.id).delete()
        except:
            print('Something broke...')
            traceback.print_exc()

        time.sleep(1)

if __name__ == '__main__':
    print('Starting service')
    #threading.Thread(target=listener).start()
    listener()