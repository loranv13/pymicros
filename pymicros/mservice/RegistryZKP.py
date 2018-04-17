from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError, NoNodeError


class zkp:

    def __init__(self, ip, port):
        
        self.zk = KazooClient(hosts=ip+':'+port)
        self.zk.start()


    def register(self, serviceName, serviceId, s):
        self.zk.ensure_path("/registry/"+serviceName)
        #self.zk.ensure_path("/registry/"+self.MS_NAME+"/"+self.MS_ID)

        try:
            self.zk.create("/registry/"+serviceName+"/"+serviceId, s.encode())
            return True
        except NodeExistsError:
            self.zk.delete("/registry/"+serviceName+"/"+serviceId, recursive=True)
            self.register(serviceName, serviceId, s)
            pass

    def unregister(self, serviceName, serviceId):
        self.zk.delete("/registry/"+serviceName+"/"+serviceId, recursive=True)
   

    def treeService(self, liste):
        srv = liste.split(',')
        for item in srv:
            try:
                print( self.zk.get("/registry/"+item)) 
            except NoNodeError:
                print ('Oups....service '+item+' does not exist!!!\n')    
