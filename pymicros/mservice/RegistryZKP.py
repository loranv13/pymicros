from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError, NoNodeError


class zkp:

    def __init__(self, ip, port, listeService):
        
        self.listeService = listeService
        self.zk = KazooClient(hosts=ip+':'+port)
        self.zk.start()


    def register(self, serviceName, serviceId, s):
        self.zk.ensure_path("/registry/"+serviceName)
        #self.zk.ensure_path("/registry/"+self.MS_NAME+"/"+self.MS_ID)

        try:
            self.zk.create("/registry/"+serviceName+"/"+serviceId, s.encode(), ephemeral=True)
            return True
        except NodeExistsError:
            self.zk.delete("/registry/"+serviceName+"/"+serviceId, recursive=True)
            self.register(serviceName, serviceId, s)
            pass

    def unregister(self, serviceName, serviceId):
        self.zk.delete("/registry/"+serviceName+"/"+serviceId, recursive=True)
   

    def treeService(self,*args, **kwargs):
        
        srv = self.listeService.split(',')
        for item in srv:
            try:
                for i in self.zk.get_children("/registry/"+item,watch=self.treeService):
                    print(self.zk.get("/registry/"+item+"/"+i)) 
            except NoNodeError:
                print ('Oups....service '+item+' does not exist!!!\n')    
