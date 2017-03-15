# gps_tracker
This repository is used for the gps_tracker project and keeps standalone Python scripts for various gps tracking and networking tasks: 

- Logging gps data and generate google maps in .html files
- Streaming gps data over LAN/Internet from a client with gps to a server
- To check a device's Public (WAN) IP adress
- To check wheter a host may be/not be connected to the Internet
- To send the proper email notifications for the above
- To provide daemon services for the above

In order to learn more about the gps_tracker project, how it works and how to build and set up your own device, please visit the project's page from here:
https://kostiskag.wordpress.com/2017/02/27/how-to-build-a-highly-resilient-raspberry-pi-gps-tracker-and-visualize-your-data-real-time-on-google-maps/

## Installing
In order to be able to run the scripts you should have a linux distribution with python3 and gpsd installed, most preferably, debian based. In addition you should have the gpsd-py3 package wich may be found here:
https://github.com/MartijnBraam/gpsd-py3

In Raspbian/Debian In order to install all the above dependencies:  
```
sudo apt-get update
sudo apt-get install gpsd python3 python3-pip git
sudo pip3 install gpsd-py3
cd ~
git clone https://github.com/kostiskag/gps_tracker.git
cd gps_tracker
``` 
  
## Setting Up

### Google maps
If you decide to modify the visual output of the generated map you may study google's guides:
https://developers.google.com/maps/documentation/javascript/

In order to generate google map files in .html you should issue one personal API key. Please study the following guides:
https://developers.google.com/maps/documentation/javascript/get-api-key

https://console.developers.google.com/project/_/apiui/credential

### Gmail account
In order to be able to send proper email notifications from a gmail email, you should create or edit an account to allow less secure apps to use the service. Please conult the following guides:
https://support.google.com/accounts/answer/6010255

http://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python

## Configuring setup

You should pass on your API key and your gmail credentials to configure.py

```
nano configure.py
```

### Testing gmail

You may send test your email setup with the following script:

```
python3 test_gmail.py
```
  
## How to use
With the scripts you may do the following actions:

### Logging and generating gmaps
  
```
#starts logging gps data
python3 gps_logger.py
  
#logs gps data as a daemon service and therefore is not afeced by shell hangups
python3 d_gps_logger.py start|stop|restart
  
#generates a visual map from the logged data
python3 generate_gmap.py
```
  
### Streaming from the tracker (client) to a server and generate gmaps on the fly

```
#starts a server, to be used from another host
python3 gps_stream_server.py
  
#starts a client from the gps tracker host
python3 gps_stream_client.py
  
#controlls a client from the gps tracker as a daemon
python3 d_gps_stream_client.py [server's ip address] [server's tcp port] start|stop|restart
```
  
### Sending email notifications

```
#starts a daemon service to send an email every time the device connects/reconnects to the Internet
python3 d_send_email_on_internet.py start|stop|restart
  
#starts a daemon service to send an email every time the tracker has a gps FIX and every 5min
#the latest known location
python3 d_send_email_on_fix.py start|stop|restart
```
  
### Internet/Network

```
#returns to the shell 0 when there is no Internet and 1 when there is
#access the return variable with the $? shell variable
python3 is_there_internet.py
  
#waits while there is no Internet
python3 wait_for_internet.py
  
#checks wheter an expected public ip address is the hosts ip address 
#returns to the shell 1 when you have guessed right and 0 when you have not.
#this feature is mainly used to detect U-turns and do the appropriate actions.
python3 is_my_wan_ip.py [public ip address]
```
  
### Daemon services

```
#to make your own services
cp daemon-client.py new-service.py
nano new-service.py
```
  
Thanks to Sander Marechal for the daemon code found from:
https://web.archive.org/web/20160305151936/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
  
### To create a script bundle in order to start|stop|restart all the daemon services together

```
cd ~
nano gps_bundle_services
```  
Inside the file:
```
#!/bin/bash
# comment the lines of the services you do not need to be started on the group
# you may run this file as ./gps_bundle start|stop|restart
# allways use absolute paths
  
echo "starting/stopping logger"
python3 /home/pi/gps_tracker/d_gps_logger.py $1
sleep 1
echo "starting/stopping stream client lan"
python3 /home/pi/gps_tracker/d_gps_stream_client.py 192.168.1.2 2345 $1
sleep 1
python3 /home/pi/gps_tracker/is_my_wan_ip.py 1.2.3.4
if [ $? = "0" ]; then
   #this is not a U-turn!
   echo "starting/stopping stream client internet"
   python3 /home/pi/gps_tracker/d_gps_stream_client.py 1.2.3.4 2345 $1
   sleep 1
fi
echo "start/stop email on internet"
python3 /home/pi/gps_tracker/d_send_email_on_internet.py $1
sleep 1
echo "start/stop fix email notify"
python3 /home/pi/gps_tracker/d_send_email_on_fix.py $1

ps -A | grep python3
```  
Save the file and provide execution permissions for it:
```
chmod +x gps_bundle_services
```
Use the script like:
```
./gps_bundle_services start|stop|restart
```
If you decide to run it from the system's start in an init script run it like this:
```
sudo -u pi /home/pi/gps_bundle_services start
```
On raspberry pi, rasapbian: If you decide to config 3g with wvdial and init scripts for 3g, gpsd and gps_bundle to be executed on the system's start, you may find those on the scripts directory.

## License
The source code written by me is licensed under Creative Commons Atribution 4.0 International:
https://creativecommons.org/licenses/by/4.0/

You may use the source code commercially.
You should provide attribution for all the source code authors.
