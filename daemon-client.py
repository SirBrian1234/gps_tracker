"""
source taken from:
https://web.archive.org/web/20160305151936/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
"""

__author__ = "Sander Marechal"

import sys, time
from daemon import Daemon
 
class MyDaemon(Daemon):
        def run(self):
                while True:
                   print("works!")     
                   time.sleep(1)
 
if __name__ == "__main__":
        daemon = MyDaemon('/tmp/daemon-example.pid','/dev/null','/dev/null','/dev/null')
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
