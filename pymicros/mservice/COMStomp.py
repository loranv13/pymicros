import stomp



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
        for h in self.HOST_STOMP.split(','):
            CONNEXION.append((h,self.PORT_STOMP))
        try:
            self.AMQP_CONNEXION = stomp.Connection(host_and_ports=CONNEXION, keepalive=True, vhost=self.HOST_STOMP, heartbeats=(0, 0))
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
