
import uuid
import configparser
import os
import sys
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from pymicros.mservice.COMStomp import COMStomp

class service:
    ''' '''

    def __init__(self,fileConf='./etc/defaults.cfg'):
        ''' '''

        # Thread pool
        self.executor = ThreadPoolExecutor(max_workers=5)


        #
        # identify if it's the first start
        #
        self.FILE_ID         = './filegen/.id_srv'
        # case restart. Return the ID save in the file
        if ( os.path.isfile(self.FILE_ID) ):
            f = open(self.FILE_ID, "r")
            self.MS_ID = f.readline()
        # case first start. We generate the UUID
        else:
            self.MS_ID = str(uuid.uuid1());
            f = open(self.FILE_ID, "w")
            f.write(str(self.MS_ID))
        f.close()

        #
        # Read the user conf file
        #
        config = configparser.ConfigParser()
        config.readfp(open(fileConf))
        # -- read parameter
        self.MS_NAME         = config.get('administration','service_name')
        self.MS_JOB          = config.get('functional','class')
        self.MS_MODULE_JOB   = config.get('functional','module')
        # -- read configuration
        #-
        interfaces           = config.get('administration','interfaces').split(',')
        for interface in interfaces:
            if interface == "stomp":
                sys.stdout.write("INT STOMP.......: start\n")
                sys.stdout.flush()
                self.stomp_connexion = COMStomp(config.get('stomp','host'),\
                                                config.get('stomp','port'),\
                                                config.get('stomp','b2b_topic'),\
                                                config.get('stomp','b2b_queue'),\
                                                config.get('stomp','b2b_topic_evt'),\
                                                config.get('stomp','monitorring'),\
                                                config.get('stomp','management'))
                self.stomp = self.executor.submit(self.stomp_connexion.loop)

            if interface == "ws":
                self.WS_PORT = config.get('ws','port')


    def info(self):
        ''' '''
        sys.stdout.write("Service Name...: "+self.MS_NAME+"\n")
        sys.stdout.write("Service ID.....: "+self.MS_ID+"\n")
        sys.stdout.write("PID MAIN.......: "+str(os.getpid())+"\n")
        sys.stdout.flush()
