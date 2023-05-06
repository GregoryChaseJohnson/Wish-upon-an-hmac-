                                                                   
import hashlib
import requests
import hmac
import random
import string

SECRET_KEY = "Af5J7F2VJ8hrdw3dyjtr4"


def generate_initiation_string(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(chars, k=length))


initiation_string = generate_initiation_string(20)

def generate_hmac(message, key):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

def generate_substring(s):
    seed = int(hashlib.sha256(s.encode()).hexdigest(), 16) % (2**32 - 1)
    random.seed(seed)
    substring_length = random.randint(2, 3)
    start_index = random.randint(0, len(s) - substring_length)
    return s[start_index:start_index + substring_length]

def main():
    previous_handshake_fullstring = ""
    is_first_iteration = True

    for i in range(50):  # 50 iterations
        # Generate handshake_fullstring using the previous handshake_fullstring or the initiation string
        if is_first_iteration:
            handshake_fullstring = generate_hmac(initiation_string, SECRET_KEY)
        else:
            handshake_fullstring = generate_hmac(previous_handshake_fullstring, SECRET_KEY)

        # Generate handshake_clip
        handshake_clip = generate_substring(handshake_fullstring)

        # Send the initiation string and handshake_clip to the Authenticator on the first iteration, otherwise just send the handshake_clip
        if is_first_iteration:
            response = requests.post('http://localhost:5000/authenticate', json={"initiation_string": initiation_string, "handshake_clip": handshake_c>
        else:
            response = requests.post('http://localhost:5000/authenticate', json={"handshake_clip": handshake_clip})

        if response.status_code == 200:
            print("Authentication successful")
            print("Response body: ", response.json())
        else:
            print("Authentication failed")
            print("Response body: ", response.text)

        # Print newlines to add spacing between iterations
        print("\n" * 4)

        # Update the previous_handshake_fullstring for the next iteration
        previous_handshake_fullstring = handshake_fullstring

        # Update is_first_iteration to False after the first iteration
        if is_first_iteration:
            is_first_iteration = False

if __name__ == "__main__":
    main()



