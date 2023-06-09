# <span style="font-size:48px;">Wish upon an hmac</span>

This code is meant to be a dynamic challenge-response authentication system aiming to increase security by employing infinitely variable passwords to protect against eavesdropping and brute force attacks. By truncating large strings which hold the parent structure, into smaller segments transmintted from the client to the server, eavesdroppers have a smaller amount of information with which to infer structure from the much larger string, thus increasing the diffficulty of reverse engineering the transmissions.

In this cocnept, the authentication process starts with the client generating a large initiation string, which is then passed through an HMAC function together with a secret key shared between the server. The resultant offpsring of the initiation string being passed through the hmac function is derived internally by both the client and server and is reffered to as  the " handshake fullstring." From this handhshake fullstring a small clip is extracted of N size and N location within the handshaske fullstring. N is the result of passing the string to a random function which produces a deterministic output string called the "handshake clip." Both client and server produce the same clip deterministically. The clip is then shared, from the client to the server for autherization for that iteration. If it's a success, meaning if the server  predicted what the client sent, then the next iteration begins. The initiation string gets stored and checked against in future authorization attempts. The next iteration is begining it's process with the previous iterations handshake fullstring so no initiation string is required. Both server and client derive the next iterations handshake fullstring internally. Only the handhsake clips are sent by the client to the server. Iterations are set at 50 in the code, after which the autherization process is complete.

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
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                        
                   

                                                                                 

 
                                                                                
                            
                                                                            
                                                                               
