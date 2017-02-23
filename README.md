# gps_tracker
This repository keeps standalone python scripts for various gps tracking and networking tasks: 

-> logging gps data and generate google maps in .html files

-> streaming gps data over LAN/Internet from a client to a server

-> to check a device's Public (WAN) IP adress

-> to check wheter a host may be/not be connected to the Internet

-> to send the proper email notifications for the above

-> to provide daemon services for the above


The repository's source code is used for the [] project which may be viewed from my blog from here:


Installing
----------

In order to be able to run them you should have a linux distribution with python3 and gpsd installed, most preferably, debian based. In addition you should have the gpsd-py3 package wich may be found here:
https://github.com/MartijnBraam/gpsd-py3

In Raspbian/Debian In order to install all the above dependencies:

  $ sudo apt-get update
  
  $ sudo apt-get install gpsd python3 git
  
  $ sudo pip3 install gpsd-py3
  
  $ cd ~
  
  $ git clone https://github.com/kostiskag/gps_tracker.git
  
  $ cd gps_tracker
  
  
Setting Up
----------

Google maps
-----------
If you decide to modify the visual output of the generated map you may study google's guides:
https://developers.google.com/maps/documentation/javascript/

In order to generate google map files in .html you should issue one personal API key. Please study the following guides:
https://developers.google.com/maps/documentation/javascript/get-api-key

https://console.developers.google.com/project/_/apiui/credential

Gmail notifications
-------------------
In order to be able to send proper email notifications from a gmail email, you should create or edit an account to allow less secure apps to use the service. Please conult the following guides:
https://support.google.com/accounts/answer/6010255

http://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python

Testing gmail
-------------
You may send test your email setup with this script:

  $ python3 test_gmail.py
  
Running
-------

