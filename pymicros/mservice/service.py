import configparser
import signal
import os
import sys
from time import sleep
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from pymicros.mservice.COMStomp import COMStomp
from pymicros.mservice.COMWs import COMWs
from pymicros.mservice.RegistryZKP import zkp
from threading import current_thread 
import queue
from flask import Flask
from kazoo.client import KazooClient
import logging
import uuid
import time
import json

qrcv = queue.Queue()

class service:
    ''' '''

    def __init__(self,fileConf='./etc/defaults.cfg'):
        ''' '''
        registre ={}
        zkp_registre={}
        #logging.basicConfig()
        #

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
        self.MONIT	     = config.get('stomp','monitorring')
        # -- read configuration
        #-
        interfaces           = config.get('administration','interfaces').split(',')
        for interface in interfaces:
            if interface == "stomp":
                #sys.stdout.flush()
                self.stomp_connexion = COMStomp(config.get('stomp','host'),\
                                                config.get('stomp','port'),\
                                                config.get('stomp','b2b_topic'),\
                                                config.get('stomp','b2b_queue'),\
                                                config.get('stomp','b2b_topic_evt'),\
                                                config.get('stomp','monitorring'),\
                                                config.get('stomp','management'))
                self.info()
                sys.stdout.write("Start thread Stomp from "+current_thread().name+"\n")
                sys.stdout.flush()
                self.stomp = self.executor.submit(self.stomp_connexion.connexion)
                registre = {'topic':config.get('stomp','b2b_topic'),'queue': config.get('stomp','b2b_queue')}
                zkp_registre['STOMP']= registre

            if interface == "ws":
                self.WS_PORT = config.get('ws','port')
                self.WS_IP= config.get('ws','ip')
                self.ws_connexion = COMWs(self.WS_IP, int(self.WS_PORT))
                sys.stdout.write("Start thread WS from "+current_thread().name+"\n")
                sys.stdout.flush()
                self.executor.submit(self.ws_connexion.listen)
                registre = {'ip':self.WS_IP,'port':self.WS_PORT}
                zkp_registre['WS']= registre
                
        # -- Read conf zkp
        self.zk = zkp(config.get('zkp','ip'), config.get('zkp','port'), config.get('dependances','services'))
        self.zk.register(self.MS_NAME, self.MS_ID, json.dumps(zkp_registre))
	# -- get liste service dependency
        self.zk.treeService()


    def info(self):
        ''' '''
        sys.stdout.write("Service Name...: "+self.MS_NAME+"\n")
        sys.stdout.write("Service ID.....: "+self.MS_ID+"\n")
        sys.stdout.write("PID MAIN.......: "+str(os.getpid())+"\n")
        sys.stdout.write("Main Thread....: "+current_thread().name+"\n")
        sys.stdout.flush()
        self.stomp_connexion.sendFF(self.MONIT, "{'service':'"+self.MS_NAME+"','id':'"+self.MS_ID+"','state':'start'}") 

    
    def loop(self):
        global qrcv
        while True:
            try: 
                while not qrcv.empty():
                    sys.stdout.write(" --- "+current_thread().name+" : "+qrcv.get()+" - "+str(time.time())+"\n")
                    sys.stdout.flush()
                sleep(0.1)
            except KeyboardInterrupt:
                self.zk.unregister(self.MS_NAME, self.MS_ID)
                print("\n-----------------------Purge des queues...\n")
                while not qrcv.empty():
                    sys.stdout.write(" - "+str(time.time())+"\n")
                    sys.stdout.flush()
                sys.exit(0)
