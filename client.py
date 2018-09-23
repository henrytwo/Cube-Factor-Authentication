from firebase_admin import credentials, firestore, auth
import firebase_admin
import uuid
import sys
import traceback
import time
import crypto

cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred)

REQUEST_TIMEOUT = 30 # timeout in seconds

def get_cubes():
    print('Fetching from database...')

    cube_list = []
    cubes = firebase_admin.firestore.client(app=None).collection('cubes').get()

    count = 0

    for cube in cubes:
        if cube.id:  # valid code

            if count == 0:
                print('|-ID-|-----------Name-----------|')

            count += 1
            data = cube.to_dict()

            data['name'] = cube.id

            cube_list.append(data)

            print('|%4i|%26s|' % (count, cube.id))

    if not count:
        print('No cubes found!')
    else:
        print('|----|--------------------------|')

    return cube_list

def get_codes():
    print('Fetching from database...')

    code_list = []
    codes = firebase_admin.firestore.client(app=None).collection('codes').get()

    count = 0

    for code in codes:
        if code.id: # valid code

            if count == 0:
                print('|-ID-|-----------Name-----------|----------Cubename-----------|')

            count += 1
            data = code.to_dict()
            data['name'] = code.id

            code_list.append(data)

            print('|%4i|%26s|%29s|' % (count, code.id, data['cube']))

    if not count:
        print('No 2FA codes found!')
    else:
        print('|----|--------------------------|-----------------------------|')

    return code_list

def add_code(name, code):

    cubes = get_cubes()

    if not cubes:
        print('boi u need to add a cube key first')
    else:
        while True:
            selection = int(input('Enter cube to encrypt with [ID]: ')) - 1

            try:
                cube = cubes[selection]

                print(cube)

                rsa_pair = crypto.RSACipher(cube)

                encrypted_code = rsa_pair.cube_encrypt(code)

                firebase_admin.firestore.client(app=None).collection('codes').document(name).set(
                    {'secret': encrypted_code, 'cube': cube['name']})

                break

            except:
                traceback.print_exc()
                print('no that doesn\'t fcking work')

def get_code():

    codes = get_codes()
    request_id = str(uuid.uuid4())
    
    if not codes:
        print('boi u have no codes to get')
    else:
        while True:
            selection = int(input('Enter code to decrypt [ID]: ')) - 1

            try:
                code = codes[selection]

                print('Setting reader to code getting mode...\nGetting code: "%s"...' % code['name'])

                firebase_admin.firestore.client(app=None).collection('queue').document(str(uuid.uuid4())).set(
                    {'command': 'decrypt', 'code': code['secret'], 'cube': code['cube'], 'request_id' : request_id})

                callback_recieved = False
                start_time = time.time()

                print('Waiting for response...')

                while True:

                    if time.time() > start_time + 30:
                        print('Aborted: Request timed out')
                        break

                    callback = firebase_admin.firestore.client(app=None).collection('callback').get()

                    for c in callback:

                        if c.id == request_id:
                            print('Response:', c.to_dict()['response'])

                            callback_recieved = True

                            firebase_admin.firestore.client(app=None).collection('callback').document(c.id).delete()

                            break

                    if callback_recieved:
                        break


                break

            except:
                traceback.print_exc()
                print('no that doesn\'t fcking work')

def program_cube(name):
    print('Setting reader to programming mode...\nProgramming configuration: "%s"...' % name)

    request_id = str(uuid.uuid4())

    #firebase_admin.firestore.client(app=None).collection('callback').document(request_id).set({'response': 'u literally fucked everything up'})
    firebase_admin.firestore.client(app=None).collection('queue').document(request_id).set({'command':'program', 'name': name})

    print('\nCommand sent! Please follow prompt on screen\nWaiting for response...')

    callback_recieved = False
    start_time = time.time()

    while True:

        if time.time() > start_time + 30:
            print('Aborted: Request timed out')
            break

        callback = firebase_admin.firestore.client(app=None).collection('callback').get()

        for c in callback:

            if c.id == request_id:

                print('Response:', c.to_dict()['response'])

                callback_recieved = True

                firebase_admin.firestore.client(app=None).collection('callback').document(c.id).delete()

                break

        if callback_recieved:
            break

try:
    if len(sys.argv) == 1:
        print('boi u need to provide an argument')

    elif sys.argv[1] == 'add':
        if len(sys.argv) < 3:
            print('boi u need to specify the type u wanna add')
        else:

            if sys.argv[2] == 'cube':
                program_cube(sys.argv[3])
            elif sys.argv[2] == 'code':
                add_code(sys.argv[3], sys.argv[4])
            else:
                print('bro invalid selection')

    elif sys.argv[1] == 'list':
        if len(sys.argv) < 3:
            print('boi u need to specify the thing u wanna list')
        else:
            list_thing = sys.argv[2]
            if list_thing == 'cubes':
                get_cubes()
            elif list_thing == 'codes':
                get_codes()
            else:
                print('wtf? invalid selection')

    elif sys.argv[1] == 'decrypt':
        get_code()

    else:
        print('boi dis command is not recognized')

except:
    print('ok u broke something')
    traceback.print_exc()
