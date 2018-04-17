from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError




class TreeService:

    def __init__(self,liste):
        
        srv = liste.split(',')
        for item in liste:
                
