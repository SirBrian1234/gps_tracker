""" 
generate_gmap.py generates a gmaps .html standalone file from a list
of gps points logged from gps_logger.py . 
"""

__author__ = "Konstantinos Kagiampakis"
__license__ = """ 
Creative Commons Attribution 4.0 International
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode
"""

import json
import configure

GPS_DATA_FILE = 'gps_route.log'
GMAPS_FILE_TO_BE_GENERATED = 'generated_gmaps.html'

try:
   f = open(GPS_DATA_FILE,'r')
except:
   raise
else:
   try:
      g = open(GMAPS_FILE_TO_BE_GENERATED,'w')   
   except:
      raise
   else:
      str_pointList = f.read()
      str_pointList_out = "["+str_pointList.replace("\0","").strip()[:-1]+"]"
      print(str_pointList_out)
      pointList = json.loads(str_pointList_out)
      
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

      try:
         g.write(GENERATED_HTTP_PAGE)
      except:
         try:
            f.close()
            g.close()
         except:
            raise
         else:
            raise      
      else:
         print("Gmaps HTML Generated!")      
         try:
            f.close()
            g.close()
         except:
            raise