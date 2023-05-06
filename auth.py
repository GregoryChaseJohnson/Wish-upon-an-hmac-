                                                                      
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

app = Flask(__name__)

iteration = 0
previous_handshake_fullstring = ""

@app.route('/authenticate', methods=['POST'])
def authenticate():
    global iteration
    global previous_handshake_fullstring
    data = request.get_json()
    initiation_string = data.get('initiation_string')
    received_handshake_clip = data['handshake_clip']
    


    if iteration == 0:
        # Generate the handshake_fullstring using the initiation_string
        handshake_fullstring = generate_hmac(initiation_string, SECRET_KEY)
    else:
        # Generate the handshake_fullstring using the previous handshake_fullstring
        handshake_fullstring = generate_hmac(previous_handshake_fullstring, SECRET_KEY)
  
    # Generate the expected_handshake_clip from the handshake_fullstring
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
        return {"received_handshake_clip": received_handshake_clip}, 200
    else:
        print("Authentication failed.\n\n")
        return "Not Authenticated", 401

if __name__ == '__main__':
    app.run()




