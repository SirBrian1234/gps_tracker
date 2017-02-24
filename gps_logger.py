"""
gps_logger.py logs received gps points in a local file.
"""

__author__ = "Konstantinos Kagiampakis"
__license__ = """ 
Creative Commons Attribution 4.0 International
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode
"""

import gpsd
import json
import time
import sys

STEP = 3
# Connect to the local gpsd
while True:
   try:
      print("Connecting on GPSD...")
      gpsd.connect()      
   except:
      print("Could not connect to GPSD.\nThis script is persistent and will try to reconnect to GPSD in 10 sec.",sys.exc_info()[0])
      time.sleep(10)
   else:
      print("GPSD connected!")
      break

filename = "/home/pi/gps_route.log"
try:
   f = open(filename, 'a')  
except:
   raise

while True:
   try:
      try:
        packet = gpsd.get_current()
        
        if packet.mode > 1:           
           if packet.mode >= 2:
              print("Latitude: " + str(packet.lat))
              print("Longitude: " + str(packet.lon))
              print("Track: " + str(packet.track))
              print("Horizontal Speed: " + str(packet.hspeed))
              print("Time: " + str(packet.time))
              print("Error: " + str(packet.error))
           if packet.mode == 3:
              print("Altitude: " + str(packet.alt))
              print("Climb: " + str(packet.climb))
              
           point = {'lat': str(packet.lat), 'lon': str(packet.lon),  'track': str(packet.track), 'hspeed': str(packet.hspeed), 'time': str(packet.time)}
           if packet.mode == 3:
             point['alt'] = str(packet.alt)
             point['climb'] = str(packet.climb)
  
           str_point = json.dumps(point)
           print("storing point to file:#"+str_point+"# str len:"+str(len(str_point)))
           f.write(str_point+',\n')
           
        else:
           print("There is no GPS FIX yet. Packet mode 0.")
           time.sleep(10)
      except (NameError, KeyError): 
         print("There is no GPS FIX yet. Key or Name exception.")
         time.sleep(3) 
      except:
         print (sys.exc_info()[0]) 
         time.sleep(10)      
      
      time.sleep(STEP)
   
   except KeyboardInterrupt:
      print(" Received KeyboardInterrupt")
      try:
         print("Closing file.")
         f.close()
      except:
         raise   
      else:
         print("File closed.")
         break
   except:
      print(sys.exc_info()[0])      
               