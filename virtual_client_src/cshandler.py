#!/usr/bin/python
'''Config Server Handler.

Note: the class will handler all request via the mgmt port of Config
Server. To let Config Server work is also via mgmt port. And to
handler work cmd is return OK firstly, and do the rest work in back.
'''

#Filename:cshandler.py
import BaseHTTPServer
import urlparse
import work


class CSHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    ''' Config Server Handler handlers all request via the mgmt port.

    It inherid from BaseHTTPRequestHandler, and only handle http
    request.
    '''

    # set timeout of the handler
    def setup(self):
        ''' set time out when the connection is to be founded
        '''
        BaseHTTPServer.BaseHTTPRequestHandler.setup(self)
        self.request.settimeout(30)

    def _mgmt(self):
        '''mgmt interface to parse the url
        '''
        ms_dict = {}
        try:
            req_str = urlparse.urlparse(self.path)
            com_list = req_str.query.split(r'/')
            cmd_dict  =  dict(urlparse.parse_qsl(com_list[0]))
            if len(com_list) > 1:
                ms_dict   = dict(urlparse.parse_qsl(com_list[1]))
        except (AttributeError, TypeError, KeyError, IndexError):
            return 'return=error\r\nerrorinfo=wrongurlpath'
        try:
            req_cmd = cmd_dict['cmd']
#            print req_cmd
        except (IndexError, TypeError):
            return 'return=error\r\nerror=errorcmd'
        if ms_dict.has_key("num"):
            num = ms_dict["num"]
        else:
            num = None
        handler_name = '_mgmt_'+req_cmd
        if not hasattr(self,  handler_name):
            return 'return=error\r\nerrorinfo=unknowncmd'
        handler_func = getattr(self, handler_name)
        return handler_func(num)

    def _mgmt_query_stat(self):
        '''query the mgmt stat
        '''
#        print "query_stat"
        return work.Work.ins().query_stat()


    def _mgmt_set_ms_num(self, num):
        ''' add a black ms to black_list
        '''
        return work.Work.ins().set_ms_num(num)

    def _mgmt_set_ms_error_num(self, num):
        '''del a black ms  in black 
        '''
        return work.Work.ins().set_ms_error_num(num)

    def do_GET(self):
        ''' handle GET request of HTTP
        '''
        resp = self._mgmt()
#        print resp
        if resp is not None:
            self.send_response(200)
            self.send_header('Content-Length', len(resp))
            self.end_headers()
            self.wfile.write(resp)
        else:
            self.send_error(404)
            
            
