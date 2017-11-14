

import configparser
import os
import sys

class service:
    ''' '''

    def __init__(self,fileConf='./etc/defaults.cfg'):
        ''' '''

        #
        # identify if it's the first start
        #
        self.FILE_ID         = './filegen/.id_srv'
        # case restart. Return the ID save in the file
        if ( os.path.isfile(self.FILE_ID) ):
            fichier = open(self.FILE_ID, "r")
            self.MS_ID = fichier.readline()
            fichier.close()
            self.sendMonit()
        # case first start. We generate the UUID
        else:
            self.MS_ID = str(uuid.uuid1());
            fichier = open(self.FILE_ID, "w")
            fichier.write(str(self.MS_ID))
            fichier.close()
            self.sendMonit()

        #
        # Read the conf file
        #
        config = configparser.ConfigParser()
        config.readfp(open(fileConf))
        # read fixe parameter
        self.MS_NAME         = config.get('administration','service_name')
        self.MS_JOB          = config.get('functional','class')
        self.MS_MODULE_JOB   = config.get('functional','module')
        # read configuration
        interfaces           = config.get('administration','interfaces')
        for interface in interfaces:
            if interface == "STOMP":
                self.STOMP_HOST = config.get('stomp','host')
                self.STOMP_PORT = config.get('stomp','port')


    def info(self):
        ''' '''
        sys.stdout.write("HOST...: "+self.STOMP_HOST+"\n")
        sys.stdout.flush()
