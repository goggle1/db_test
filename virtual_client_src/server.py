#!/usr/bin/python
'''Server.

Note: this is a server for single threading.
'''

#Filename:server.py
import BaseHTTPServer
#import cshandler

#import work


class Server:
    ''' a server for single threading.
    '''

    def __init__(self, server_class=BaseHTTPServer.HTTPServer,
                 handler_class=BaseHTTPServer.BaseHTTPRequestHandler, port=0):
        server_address = ('', port)
        self._svc = server_class(server_address, handler_class)

    def run(self):
        ''' run the server.
        '''
        self._svc.serve_forever()
        
        

