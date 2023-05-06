# <span style="font-size:48px;">Wish upon an hmac</span>



Data is the fuel that many computation processes use to derive patterns. So giving less data to an eaves 
dropper is a virtue no doubt. Therefor in a client-server authentication protocal wouldn't it be nice to 
truncate a large, complex string into a smaller string thus making it harder for an eaves dropper to infer 
structure from and reverse engineer? But a small code could easily suffer from brute force attacks. But 50
or 100 small codes in an explicit sequence that varies every instance the authentication protocal is run would be quite a bit 
more challenging to hack. And in the interest of better security, I invite all who want to contribute by 
decoding transmissions or by preventing that from happening.

At a high level, Wish Upon an HMAC is an iterative challenge-response system for client-server authentication. The communication is one-way, with the client (in the "req.py" script) initiating the process. The client generates a large initiation string, which is then passed through an HMAC function along with a secret key shared between the client and the server.



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
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                                                  
                                                        
                   

                                                                                 

 
                                                                                
                            
                                                                            
                                                                               
