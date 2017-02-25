""" 
gps_stream_server.py creates a server responsible to listen and collect data 
from gps_stream_client.py and therefore used to track its location. After a 
number of points it generates a gmaps html file which presents these points 
on the map.
"""

__author__ = "Konstantinos Kagiampakis"
__license__ = """ 
Creative Commons Attribution 4.0 International
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode
"""

import socket
import time
import json
import sys
import configure
  
#leave the ip 0.0.0.0 in order to listen from all interfaces
#select one specific IP in order to liste from a default interface  
IP_ADDR = '0.0.0.0'
TCP_PORT = 2345
BUFFER_SIZE = 1024
ACK = bytes("ack","utf-8")
MAXIMUM_POINTS_PER_FILE = 10 

while True: 
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((IP_ADDR, TCP_PORT))
  s.listen(1)
  
  print('Listening for the client...')
  conn, addr = s.accept()
  print('Client connected!')
  
  i=0
  pointList = []
  while True:
     try:
       data = conn.recv(BUFFER_SIZE)
       if not data: break   
       data = data.decode("utf-8").strip()
       print("received:#"+data+"#")
       
       if not data == 'NO-FIX':
         try:
            point = json.loads(data)
            pointList.append(point)
            i+=1
         except (ValueError, TypeError):
            print('Received malformed json data. Skipping.')
         except:
            raise     
       
       if i>= MAXIMUM_POINTS_PER_FILE:
          print(str(MAXIMUM_POINTS_PER_FILE) + ' points collected, exporting to html...')
          i=0
          js_data_points = ""
          for point in pointList:
              str_point = "{lat: "+point['lat']+", lng: "+point['lon']+"},\n"
              js_data_points = js_data_points + str_point
          print('collected js_data_points\n'+js_data_points)    
           
          GENERATED_HTTP_PAGE = """
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Generated Route</title>
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 100%;
      }
      /* Optional: Makes the sample page fill the window. */
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>

      // This generated html script is based on the example on: 
      // https://developers.google.com/maps/documentation/javascript/examples/polyline-simple
      
      function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 20,
          center: {lat: """+pointList[0]['lat']+""", lng: """+pointList[0]['lon']+"""},
          mapTypeId: 'terrain'
        });

        var listOfPoints = [
        """+js_data_points+"""];
          
        var PolylinePath = new google.maps.Polyline({
          path: listOfPoints,
          geodesic: true,
          strokeColor: '#FF0000',
          strokeOpacity: 1.0,
          strokeWeight: 7
        });

        for ( var i = 0; i < PolylinePath.getPath().getLength(); i++ ) {
           var marker = new google.maps.Marker({
             icon     : {
               // use whatever icon you want for the "dots"
               url     : "https://maps.gstatic.com/intl/en_us/mapfiles/markers2/measle_blue.png",
               size    : new google.maps.Size( 7, 7 ),
               anchor  : new google.maps.Point( 4, 4 )
             },
             title    : PolylinePath.getPath().getAt( i ),
             position : PolylinePath.getPath().getAt( i ),
             map      : map
           });
        }
        
        PolylinePath.setMap(map);
      }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key="""+configure.GMAPS_API_KEY+"""&callback=initMap">
    </script>
  </body>
</html>
"""
          filename = 'gps/snapshot-'+pointList[0]['time'].replace(':','_')+'.html'         
          try:
             f = open(filename, 'w')  
             f.write(GENERATED_HTTP_PAGE)
             f.close()
          except:
             raise
             
          pointList = []       
       conn.send(ACK)
       
     except socket.error:
       print("Socket error. Socket drops and reconnects.", sys.exc_info()[0])
       break
     except:
       raise  
       
  conn.close()
  time.sleep(10)
