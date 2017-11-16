import stomp
import sys
import logging
from time import sleep

#
#
#
class COMPStompListener(stomp.ConnectionListener):
    ''' '''
    def __init__(self, *args, **kwargs):
        ''' '''
        super(msListener, self).__init__(*args, **kwargs)

    def on_heartbeat_timeout(self):
        ''' '''

    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        ''' '''



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


    def connexion(self):
        ''' '''
        CONNEXION = []
        for h in self.HOSTS.split(','):
            CONNEXION.append((h,self.PORT))
        try:
            self.AMQP_CONNEXION = stomp.Connection(host_and_ports=CONNEXION, keepalive=True, vhost=self.HOSTS, heartbeats=(0, 0))
        except Exception:
            _, e, _ = sys.exc_info()
            sys.stdout.write("Unable to send heartbeat, due to: "+str(e))
            sys.stdout.flush()


    def sendRR(self):
        ''' '''

    def sendFF(self):
        ''' '''

    def sendMonit(self):
        ''' '''

    def loop(self):
        ''' '''
        while self.AMQP_CONNEXION.is_connected():
            sleep(1)
