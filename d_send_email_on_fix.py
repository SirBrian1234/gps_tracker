""" 
d_send_email_on_fix.py: This script sends an email on a gps fix. After that 
point it sends every 15 min an email with the latest gps fix in a simple text 
format. 
"""

__author__ = "Konstantinos Kagiampakis"
__license__ = """ 
Creative Commons Attribution 4.0 International
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode
"""

import gpsd
import sys 
import time
from daemon import Daemon
import datetime
import smtplib
from email.mime.text import MIMEText
import configure

def send_email(text):
  #send_email = False
  send_email = True
  st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
  msg = MIMEText(text+"\nData captured at: "+st)

  me =   configure.EMAIL_ADDRESS
  you =  configure.DESTINATION_EMAIL

  msg['Subject'] = 'GPS Tracker'
  msg['From'] = me
  msg['To'] = you

  if send_email:
    s = smtplib.SMTP_SSL('smtp.gmail.com:465')
    s.login(configure.EMAIL_ADDRESS, configure.EMAIL_PASSWORD)
    s.sendmail(me, [you], msg.as_string())
    s.quit()
 
class MyDaemon(Daemon):
        def run(self):
          STEP = 5 * 60 #5min
          #STEP = 50
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
              
          while True:
            str_out = ""
            try:
              packet = gpsd.get_current()
                                
              if packet.mode > 1:           
                 if packet.mode >= 2:
                    str_out = str_out + "Latitude: " + str(packet.lat) + "\n"
                    str_out = str_out + "Longitude: " + str(packet.lon) + "\n"
                    str_out = str_out + "Track: " + str(packet.track) + "\n"
                    str_out = str_out + "Horizontal Speed: " + str(packet.hspeed) + "\n"
                    str_out = str_out + "Time: " + str(packet.time) + "\n"
                    str_out = str_out + "Error: " + str(packet.error) + "\n"
                 if packet.mode == 3:
                    str_out = str_out + "Altitude: " + str(packet.alt) + "\n"
                    str_out = str_out + "Climb: " + str(packet.climb) + "\n"
                    
                 print("We have a fix!:#"+str_out+"#\nSending email.")
                 
                 send_email(str_out) 
                 
                 print("script sleeps for "+str(STEP)) 
                 time.sleep(STEP)                                            
              
              else:
                 print("There is no GPS FIX yet. Packet mode 0.")
                 time.sleep(3)                       
            
            except:
               print (sys.exc_info()[0]) 
               time.sleep(3)                                          
 
if __name__ == "__main__":
        daemon = MyDaemon('/tmp/send-email-on-fix.pid','/dev/null','/home/pi/stdout','/home/pi/stderr')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print ("Unknown command")
                        sys.exit(2)
                sys.exit(0)
        else:
                print ("usage: %s start|stop|restart" % sys.argv[0])
                sys.exit(2)
