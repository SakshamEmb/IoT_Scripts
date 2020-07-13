# Import socket module 
import socket  
import time               
  
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 20050       
  
# connect to the server on local computer 
s.connect(('127.0.0.2', port)) 
a = "0x000000000000008c08010000013feb55ff74000f0ea850209a690000940000120000001e09010002000300040016014703f0001504c8000c0900730a00460b00501300464306d7440000b5000bb60007422e9f180000cd0386ce000107c700000000f10000601a46000001344800000bb84900000bb84a00000bb84c00000000024e0000000000000000cf00000000000000000100003fca"[2:]  

s.send(a)  
time.sleep(2) 
#s.connect(('127.0.0.2', port)) 

print s.recv(1024) 
time.sleep(1) 

# close the connection 

s.close()   
