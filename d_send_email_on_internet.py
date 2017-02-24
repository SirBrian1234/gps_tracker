"""
This script will let you receive feedback for when the internet drops and 
reconnects.
"""

__author__ = "Konstantinos Kagiampakis"
__license__ = """ 
Creative Commons Attribution 4.0 International
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode
"""

import socket
import sys
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from daemon import Daemon
import configure

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
      while True:
        while not internet():
           print("Still no internet...")
           time.sleep(20)
        
        print("We have internet!") 
        send_email("We have internet!")  
        
        while internet():
           print("Still connected...")
           time.sleep(60)

if __name__ == "__main__":
        daemon = MyDaemon('/tmp/send-email-wan.pid','/dev/null','/home/pi/stdout','/home/pi/stderr')
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
                      