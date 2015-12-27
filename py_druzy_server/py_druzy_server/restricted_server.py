#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 22 déc. 2015

@author: druzy
'''

import cherrypy
from cherrypy.lib.static import serve_file
from mimetypes import MimeTypes
import threading
import os
from py_druzy_utils import network_utils

class RestrictedFileServer(object):
    '''serveur http très restrictif
    le serveur démarre automatiquement à l'ajout d'un fichier'''
    
    _instances=dict()
    
    def __new__(cls,port):
        if not (port in cls._instances):
            cls._instances[port]=object.__new__(cls,port)
            
        return cls._instances[port]
    
    def __init__(self,port):
        
        self._files=dict()
        self._port=port
        self._identifiant=0

        pass
    
    @cherrypy.expose
    def file(self,identifiant):
        '''path /file du serveur'''
        try:
            identifiant=int(identifiant)
        except:
            raise cherrypy._cperror.NotFound()
        
        if identifiant in self._files:
            mime=str(MimeTypes().guess_type(self._files[identifiant])[0])
            return serve_file(self._files[identifiant],mime)
        else:
            raise cherrypy._cperror.NotFound()
            
    def _start(self):
        threading.Thread(None,self._start_cherrypy).start()
        
    def _start_cherrypy(self):
        
        cherrypy.config.update({'server.socket_port': self._port,
                                'server.socket_host': network_utils.get_local_ip()})
        cherrypy.quickstart(self)
        
    def _stop(self):
        cherrypy.engine.exit()
        
    def add_file(self,f):
        ''' ajoute un fichier autorisé au serveur'''
        if os.path.isfile(f):
            self._files[self._identifiant]=f
            self._identifiant+=1
            self._start()
            return self._identifiant-1
        else:
            return None
        
    def remove_file(self,f):
        '''Supprime un fichier autorisé du fichier'''
        identifiant=self.get_id(f)
        if identifiant is not None:
            del self._files[identifiant]
            if len(self._files)==0:
                self._stop()
        
    def get_id(self,f):
        ''' Renvoie l'identifiant selon le nom du fichier'''
        res=None
        for identifiant in self._files:
            if self._files[identifiant]==f:
                res=identifiant
                break
        
        return res
    
    def get_address(self,identifiant):
        ''' Renvoie l'adresse relative à l'identifiant ou le nom du fichier'''
        if isinstance(identifiant, str):
            return self.get_address(self.get_id(identifiant))
        else:
            if (identifiant is not None) and (identifiant in self._files):
                return "http://"+network_utils.get_local_ip()+":"+str(self._port)+"/file?identifiant="+str(identifiant)
            else:
                return None
    
    
if __name__=="__main__":
    server=RestrictedFileServer(10000)
    server2=RestrictedFileServer(10000)
    server3=RestrictedFileServer(10001)
    
    print(server is server2)
    print(server is server3)