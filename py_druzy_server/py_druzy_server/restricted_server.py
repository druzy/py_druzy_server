#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 22 déc. 2015

@author: druzy
'''

import cherrypy
from cherrypy.lib.static import serve_file
from mimetypes import MimeTypes
import uuid

class RestrictedFileServer:
    
    def __init__(self):
        self._files=dict()
        self._namespace="server"
        pass
    
    @cherrypy.expose
    def file(self,id):
        if ( id in self._files):
            mime=str(MimeTypes().guess_type(self._files[id])[0])
            return serve_file(self._files[id],mime)
        else:
            return cherrypy.NotFound
    
    def start(self):
        cherrypy.config.update({'server.socket_port': 9090})
        cherrypy.quickstart(self)
        
    def stop(self):
        cherrypy.engine.exit()
        
    def add_file(self,f):
        identifiant=uuid.uuid5(self._namespace,str(f))
        self._files[identifiant,file]
        return id
        
    def remove_file(self,f):
        identifiant=self.get_id(f)
        if identifiant is not None:
            del self._files[identifiant]
        
            
            
            
    def get_id(self,f):
        res=None
        for identifiant in self._files:
            if self._files[identifiant]==f:
                res=identifiant
                break
        
        return res
        
        
if __name__=="__main__":
    server=RestrictedFileServer()
    server.start()