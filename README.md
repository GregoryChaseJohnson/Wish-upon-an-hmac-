# <span style="font-size:48px;">Wish upon an hmac</span>
This repository contains a dynamic challenge-response authentication system designed to bolster security by using variable passwords to mitigate eavesdropping and brute force attacks. It achieves this by transmitting small segments of large strings from the client to the server, making reverse engineering significantly harder for potential eavesdroppers.

Here's how it works:

The client generates a large "initiation string" and passes it through an HMAC function with a shared secret key, resulting in the 'handshake fullstring', which both parties derive internally.

A small clip (the 'handshake clip') of size and location N within the fullstring is determined by a random function. Both client and server deterministically produce this clip.

The client sends the clip to the server for validation. If the server successfully predicts the client's clip, the process proceeds to the next iteration. 

Subsequent iterations use the previous fullstring, so no new initiation string is required. The client sends only the handshake clips to the server.

The authorization process completes after 50 iterations, as defined in the code.

The code runs 50 iterations in less that a second.

# <span style="font-size:48px;">basic architecture</span>
The process starts with the client sending an "initiation string" of ASCII characters to the server. I used 
len 20 in the code.

#initiation string "k9Ao5rJc6Fcm02HvX2k4"


The client and server both create and store, but do not transmit, a new string created from the initiation 
string called the "handshake fullstring". This is done by passing an hmac function (which uses the SHA-256 
hashing algorithm) to the initiation. This handshake fullstring string is preferrably a long string for
more key space and thus more complexity. 

#handshake full_string "f75e6a02a9a98343227b1c2c95c91b329dd50a9077c5fc3758502888b9f37e30"

Next both the client and the server internally generate a truncated version of this
handshake full string, called the handshake clip. The length of the handshake clip varies randomly as 
does it's position within the handshake fullstring. In my code it varies in length from 2 to 3 characters

#handshake fullstring "f75e6a02a9a98343227b1c2c95c91b329dd50a9077c5fc3758502888b9f37e30"
#handshake clip                                "5c9"       


The client sends the handshake clip to the server 
(in the "auth.py" script) for validation.

The server then compares the received handshake clip with its own internally generated handshake clip. 


Client/Requester --------------------------------"5c9"----------------------------Server/Authenticator

                                                                                   predicted:"5c9" 
                                                                                   received: "5c9"
                                                                                   
                                                                                   50 iterations
                                                                                   
                                                                                   Matched. 1 /50
                                                                                   Matched. 2 /50
                                                                                   ..............
If they match, the server considers the authentication successful for that iteration. 
The process is repeated for a pre-determined number of iterations, with each iteration using the previous
handshake full string as input instead of the initiation string which only happens once. 


# <span style="font-size:48px;">a bit more detailed</span>

Requester                                            


1. Randmonly Generate Initiation String

   └───> Store Initiation String

2. Generate Full string by passing 
HMAC with Key to Initiation
String.

└───> Store Handshake Full String

3. Generate "Handshake Clip"
(substring) from Handshake
Full String


└───> Transmit Handshake Clip
   (and Initiation String for
   first iteration)
 

└───> Use current iterations handshake_fullstring as next iterations handhshake fullstring. 
***Initiation string only on first iteration***




Transmit.....
============================================================================>             

                                                                                        Authenticator

                                                                               4. Receive and store Handshake Clip (and
                                                                                  Initiation String for first
                                                                                                   iteration)
                                                                                └───> 
                                                                             
                                                                                5. Generate & strore 
                                                                                Handshake full_string using 
                                                                                either the Initiation String
                                                                                or the  previous 
                                                                                Handshake Full String
                                                                                └───> 
                                                                                
                                                                                    
                                                                                  └───> Compare the recieved handshake clip 
                                                                                  with interanlly generated handshake clip.
                                                                                  If same then authenticate.
#next iteration
# <span style="font-size:48px;">potential downsides</span>     
Ultimately the model cannibolizes the initiation string which is sent on the 1st iteration. The subsequent iterations are essentially recycling the previous iterations " handshake_fullstring " as the message that then gets used in the function

"def generate_hmac(message, key):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()
"
                                                                                  
A new handshake fullstring is then produced, but I can imagine the randomness gets progressivelly reduced per subsequent iteration. But the question is, does it matter? Is it still mathematically infeasable for an eaves dropper to be able to send an initiation string and guess the handshake fullstring and the handhsake clip without having the secret key for the hmac and the seed to the random number generator ( which truncates the handshake fullstring to create the handhsake clip.                                                                                
# <span style="font-size:48px;">License</span>   
MIT 
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                        
                   

                                                                                 

 
                                                                                
                            
                                                                            
                                                                               
