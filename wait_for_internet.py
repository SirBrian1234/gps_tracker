import socket
import sys
import time

def internet(host="8.8.8.8", port=53, timeout=3):
   """
   Host: 8.8.8.8 (google-public-dns-a.google.com)
   OpenPort: 53/tcp
   Service: domain (DNS/TCP)
   """
   try:
      socket.setdefaulttimeout(timeout)
      socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
      return True
   except:
      print (sys.exc_info()[0])
      return False

step = 20 

while not internet():
   print("Still no internet...")
   time.sleep(20)

print("We have internet!")   
   