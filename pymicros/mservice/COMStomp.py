import stomp
import sys
import logging
from time import sleep
from threading import Thread, current_thread
import pymicros.mservice.service
import time

#
#
#
class COMPStompListener(stomp.ConnectionListener):
    ''' '''
    def __init__(self, *args, **kwargs):
        ''' '''
        super(COMPStompListener, self).__init__(*args, **kwargs)

    def on_heartbeat_timeout(self):
        ''' '''

    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        ''' '''
        sys.stdout.write(current_thread().name+" : "+message+" - "+str(time.time()))
        pymicros.mservice.service.qrcv.put(message)



#
#
#
class COMStomp:
    ''' '''
    def __init__(self, hosts, port, topic, queue, evt, monit, management):
        ''' '''
        self.HOSTS           = hosts
        self.PORT            = port
        self.MONITORRING     = monit
        self.MANAGEMENT      = management
        self.MS_TOPIC        = topic
        self.MS_QUEUE        = queue
        self.MS_EVT_PUBLISH  = evt


        CONNEXION = []
        for h in self.HOSTS.split(','):
            CONNEXION.append((h,self.PORT))
        try:
            self.AMQP_CONNEXION = stomp.Connection(host_and_ports=CONNEXION, keepalive=True, vhost=self.HOSTS, heartbeats=(0, 0))
            sys.stdout.write("Stomp connection established...\n")
            sys.stdout.flush()
        except ConnectionRefusedError:
            _, e, _ = sys.exc_info()
            sys.stdout.write("Unable to send heartbeat, due to: "+str(e))
            sys.stdout.flush()
        except exception.ConnectionRefusedError:
            pass

        self.AMQP_CONNEXION.start()
        self.AMQP_CONNEXION.connect(username='',passcode='',wait=True)



    def connexion(self):
        ''' '''
        self.listener = COMPStompListener()
        self.AMQP_CONNEXION.set_listener('MS', self.listener) 
        #self.AMQP_CONNEXION.start() 
        #self.AMQP_CONNEXION.connect(username='',passcode='',wait=True)
        self.AMQP_CONNEXION.subscribe(self.MS_QUEUE, id=121, ack='auto')
        self.AMQP_CONNEXION.subscribe(self.MS_TOPIC, id=122, ack='auto')


    def sendRR(self):
        ''' '''

    def sendFF(self, rcv, message):
        ''' '''
        #try:
        self.AMQP_CONNEXION.send(rcv,message)
        '''except Exception as e:
            _, e, _ = sys.exc_info()
            sys.stdout.write(">>>> "+str(e)+"\n")
            sys.stdout.flush()'''


    def loop(self):
        ''' '''
        while self.AMQP_CONNEXION.is_connected():
            sleep(1)
