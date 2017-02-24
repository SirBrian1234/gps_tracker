import sys
from requests import get


if len(sys.argv) == 2:
  ip = get('https://api.ipify.org').text
  print('My public IP address is: {}'.format(ip))
  if ip == sys.argv[1]:
     answ = "it is!"
     ex = 1
  else:
     answ = "it is not!"
     ex = 0
  print('Therefore... '+answ)
  sys.exit(ex)
else:
   print("use as: "+sys.argv[0]+" [wan ip address]")
