  GNU nano 6.2                                                                                                                                                                                                                     auth.2.py                                                                                                                                                                                                                              
import json
from flask import Flask, request
import random
import string
import hashlib
import hmac

SECRET_KEY = "Af5J7F2VJ8hrdw3dyjtr4"

def generate_hmac(message, key):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

def generate_substring(s):
    seed = int(hashlib.sha256(s.encode()).hexdigest(), 16) % (2**32 - 1)
    random.seed(seed)
    substring_length = random.randint(2, 3)
    start_index = random.randint(0, len(s) - substring_length)
    return s[start_index:start_index + substring_length]

def load_used_initiation_strings():
    try:
        with open("used_initiation_strings.json", "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_used_initiation_strings(used_initiation_strings):
    with open("used_initiation_strings.json", "w") as f:
        json.dump(list(used_initiation_strings), f)

app = Flask(__name__)

iteration = 0
previous_handshake_fullstring = ""
used_initiation_strings = load_used_initiation_strings()

@app.route('/authenticate', methods=['POST'])
def authenticate():
    global iteration
    global previous_handshake_fullstring
    global used_initiation_strings
    data = request.get_json()
    initiation_string = data.get('initiation_string')
    received_handshake_clip = data['handshake_clip']

    if iteration == 0 and initiation_string in used_initiation_strings:
        print("Authentication failed: initiation string already used.\n\n")
        return "Not Authenticated: initiation string already used", 401

    if iteration == 0:
        handshake_fullstring = generate_hmac(initiation_string, SECRET_KEY)
    else:
        handshake_fullstring = generate_hmac(previous_handshake_fullstring, SECRET_KEY)

    expected_handshake_clip = generate_substring(handshake_fullstring)

    print("Handshake full string: ", handshake_fullstring)
    print("Expected handshake clip: ", expected_handshake_clip)
    print("Received handshake clip: ", received_handshake_clip)

    if received_handshake_clip == expected_handshake_clip:
        print("Authentication successful!\n\n")
        if iteration == 0:
            print(f"Initiation string: {initiation_string}")
            print(f"Expected: {expected_handshake_clip}")
            print(f"Received: {received_handshake_clip}")
        else:
            print(f"Expected full string: {handshake_fullstring}")
            print(f"Expected: {expected_handshake_clip}")
            print(f"Received: {received_handshake_clip}")
        iteration += 1
        previous_handshake_fullstring = handshake_fullstring

        if iteratio  GNU nano 6.2                                                                                                                                                                                                                     auth.2.py                                                                                                                                                                                                                              
import json
from flask import Flask, request
import random
import string
import hashlib
import hmac

SECRET_KEY = "Af5J7F2VJ8hrdw3dyjtr4"

def generate_hmac(message, key):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

def generate_substring(s):
    seed = int(hashlib.sha256(s.encode()).hexdigest(), 16) % (2**32 - 1)
    random.seed(seed)
    substring_length = random.randint(2, 3)
    start_index = random.randint(0, len(s) - substring_length)
    return s[start_index:start_index + substring_length]

def load_used_initiation_strings():
    try:
        with open("used_initiation_strings.json", "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_used_initiation_strings(used_initiation_strings):
    with open("used_initiation_strings.json", "w") as f:
        json.dump(list(used_initiation_strings), f)

app = Flask(__name__)

iteration = 0
previous_handshake_fullstring = ""
used_initiation_strings = load_used_initiation_strings()

@app.route('/authenticate', methods=['POST'])
def authenticate():
    global iteration
    global previous_handshake_fullstring
    global used_initiation_strings
    data = request.get_json()
    initiation_string = data.get('initiation_string')
    received_handshake_clip = data['handshake_clip']

    if iteration == 0 and initiation_string in used_initiation_strings:
        print("Authentication failed: initiation string already used.\n\n")
        return "Not Authenticated: initiation string already used", 401

    if iteration == 0:
        handshake_fullstring = generate_hmac(initiation_string, SECRET_KEY)
    else:
        handshake_fullstring = generate_hmac(previous_handshake_fullstring, SECRET_KEY)

    expected_handshake_clip = generate_substring(handshake_fullstring)

    print("Handshake full string: ", handshake_fullstring)
    print("Expected handshake clip: ", expected_handshake_clip)
    print("Received handshake clip: ", received_handshake_clip)

    if received_handshake_clip == expected_handshake_clip:
        print("Authentication successful!\n\n")
        if iteration == 0:
            print(f"Initiation string: {initiation_string}")
            print(f"Expected: {expected_handshake_clip}")
            print(f"Received: {received_handshake_clip}")
        else:
            print(f"Expected full string: {handshake_fullstring}")
            print(f"Expected: {expected_handshake_clip}")
            print(f"Received: {received_handshake_clip}")
        iteration += 1
        previous_handshake_fullstring = handshake_fullstring

        if iteration == 1:
            used_initiation_strings.add(initiation_string)
            save_used_initiation_strings(used_initiation_strings)  # Save the used initiation strings to the JSON file

        return {"received_handshake_clip": received_handshake_clip}, 200
    else:
        print("Authentication failed.\n\n")
        return "Not Authenticated", 401

if __name__ == '__main__':
    app.run()






n == 1:
            used_initiation_strings.add(initiation_string)
            save_used_initiation_strings(used_initiation_strings)  # Save the used initiation strings to the JSON file

        return {"received_handshake_clip": received_handshake_clip}, 200
    else:
        print("Authentication failed.\n\n")
        return "Not Authenticated", 401

if __name__ == '__main__':
    app.run()






