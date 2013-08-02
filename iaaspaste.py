#!/usr/bin/python
#*-*coding:utf-8*-*
#
#IaaSapi Paste
#

import os
import time
import iaasapi as api 
import webob
import sys
import re
import logging
from webob import exc
from webob import Request
from webob import Response
from paste.deploy import loadapp
from wsgiref.simple_server import make_server
from daemon import Daemon

_host_ip = '192.168.0.55'
_nova_ip = _host_ip + ':8774'
_keystone_ip = _host_ip + ':35357'
_quantum_ip = '192.168.0.56:9696'
_disk_dir = "/ft_storage"
_networ_id = 'f8aff156-7e5b-4286-8883-67b1e7aa7c8d'
_iface = "eth1"

SERVER_INFO = {'host': '172.18.1.17',
               'port': 8080}

G_INFO = {'token': 'admin',
          'tenant': 'admin',
          'user': 'admin',
          'password': 'admin_pass'}

def path_check(_url):
    urlmatch = re.match(r"/iaas[a-zA-Z]+.action$", _url)
    if urlmatch:
        return _url.split('/')[-1].split('.')[0]
    else:
        return 'None'

def initlog(logfile):
    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    return logger

#Filter
class LogFilter():
    def __init__(self, app):
        self.app = app
        self.logger = initlog('logs/iaasapi.log')
        
    def __call__(self, environ, start_response):
        _str = '<path_info: %s>' % environ['PATH_INFO'] + '<query_string: %s>' % environ['QUERY_STRING'] + '<remote_addr: %s>' % environ['REMOTE_ADDR']
        self.logger.info(_str)
        return self.app(environ, start_response)
   
    @classmethod
    def factory(cls, global_conf, **kwargs):
        return LogFilter

class IaasApi():
    def __init__(self):
        pass
    def __call__(self, environ, start_response):
        req = Request(environ)
        print '>>>Req at ', time.strftime("%Y-%m-%d|%H:%M:%S", time.localtime()) 
        print 'method: ', req.method
        print 'path_info: ', req.path_info
        print 'query_string: ', req.query_string    
        print 'headers: ', req.headers
#    pprint(environ)
        path_url = req.path_info
        service = path_check(path_url)
#        if req.method != 'POST':
#            return ["ERROR: Invaild method"]
        if service != 'None':
            REQ_DICT = {"params": {}, "headers": {}}
            token_id, nova_url, keystone_adminurl, keystone_publicurl = api.iaas_get_token(_host_ip)
            REQ_DICT['params'] = {"tenant": req.params['portalTenantId']}
            nova_path = nova_url[2]
            

            if service == 'iaasGetOsTenant':
                REQ_DICT['params'] = {"tenant_name": req.params['portalTenantId']}

                rsp = 

                try:
                    _tenant_name = req.params['portalTenantId']
                    print "tenant name: ", _tenant_name
                    _rsp = api.iaas_create_tenant(_keystone_ip, _tenant_name)
                    print ">>>Rsp: ", _rsp
                except:
                    _rsp = exc.HTTPBadRequest('Invaild params')
                    
            elif service == 'iaasReleaseTenant':
                try:
                    tenant_id = req.headers['x-wocloud-iaas-tenantid']
                    print "tenant id: ", tenant_id
                    _rsp = api.iaas_release_tenant(_keystone_ip, tenant_id)
                    print ">>>Rsp: ", _rsp
                except:
                    _rsp = exc.HTTPBadRequest('Invaild params')
                    
            elif service == 'iaasGetQuotas':
                try:
                    tenant_id = req.headers['x-wocloud-iaas-tenantid']         
                    print "tenant id: ", tenant_id
                    _rsp = api.iaas_get_quota(token_id, _nova_ip, nova_path, tenant_id)
                    print ">>>Rsp: ", _rsp
                except:
                    _rsp = exc.HTTPBadRequest('Invaild params')
                    
            elif service == 'iaasCreateServer':
                try:
                    image_id, flavor_id, quantity, appkey = req.params['imageId'], req.params['flavorId'], req.params['quantity'], req.headers['x-wocloud-iaas-appkey']           
                    print "image id: ", image_id
                    print "flavor id: ", flavor_id  
                    print "quantity: ", quantity       
                    print "appkey: ", appkey
                    quantity = int(quantity)
                    _rsp = api.iaas_create_server(token_id, _nova_ip, nova_path, image_id, flavor_id, appkey,
                                                  _networ_id, _iface, _disk_dir, _quantum_ip, quantity)
                    print ">>>Rsp: ", _rsp
                except:
                    _rsp = exc.HTTPBadRequest('Invaild params')
                    
            elif service == 'iaasReleaseServer':
                try:
                    server_id = req.params['serverId']
                    print "server id: ", server_id
                    _rsp = api.iaas_release_server(token_id, _nova_ip, nova_path, server_id)
                    print ">>>Rsp: ", _rsp
                except:
                    _rsp = exc.HTTPBadRequest('Invaild params')
                               
            elif service == 'iaasStartServer':
                try:
                    server_id = req.params['serverId'] 
                    print "server id: ", server_id
                    _rsp = api.iaas_start_server(token_id, _nova_ip, nova_path, server_id)
                    print ">>>Rsp: ", _rsp
                except:
                    _rsp = exc.HTTPBadRequest('Invaild params')
                    
            elif service == 'iaasStopServer':
                try:
                    server_id = req.params['serverId'] 
                    print "server id: ", server_id
                    _rsp = api.iaas_stop_server(token_id, _nova_ip, nova_path, server_id)
                    print ">>>Rsp: ", _rsp
                except:
                    _rsp = exc.HTTPBadRequest('Invaild params')

            elif service == 'iaasCheckServer':
                try:
                    server_id = req.params['serverId']
                    print "server id: ", server_id
                    _rsp = api.iaas_check_server(token_id, _nova_ip, nova_path, server_id, _type='normal')
                    print ">>>Rsp: ", _rsp
                except:
                    _rsp = exc.HTTPBadRequest('Invaild params')
            
            elif service == 'iaasGetServerStatus':
                try:
                    server_id = req.params['serverId'] 
                    print "server id: ", server_id
                    _rsp = api.iaas_check_server(token_id, _nova_ip, nova_path, server_id, _type='check_status')
                    print ">>>Rsp: ", _rsp
                except:
                    _rsp = exc.HTTPBadRequest('Invaild params')
                    
            elif service == 'iaasGetImages':
                _rsp = api.iaas_get_images(token_id, _nova_ip, nova_path)
                print ">>>Rsp: ", _rsp
                    
            elif service == 'iaasGetFlavors':
                _rsp = api.iaas_get_flavors(token_id, _nova_ip, nova_path)
                print ">>>Rsp: ", _rsp
                    
            else:
                _rsp = exc.HTTPBadRequest('Invaild path')
                return _rsp(environ, start_response)
            _rrsp = Response()
            _rrsp.status = "200 OK"
            _rrsp.content_type = "text/plain"
            _rrsp.body = _rsp
            return _rrsp(environ, start_response)
        _rsp = exc.HTTPBadRequest('Invaild path')
        return _rsp(environ, start_response)
    
    @classmethod
    def factory(cls,global_conf,**kwargs):
        return IaasApi()

class MyDaemon(Daemon):
    def do(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def run(self):
        server = make_server(SERVER_INFO['host'], SERVER_INFO['port'], self.wsgi_app)
        server.serve_forever()
        pass


if __name__ == '__main__':
    print("IAASPASTE.... %s" % (sys.argv[1] if len(sys.argv)>1 else ''))
    configfile = "iaas-paste.ini"
    appname = "ephem"
    wsgi_app = loadapp("config:%s" % os.path.abspath(configfile), appname)
    
    daemon = MyDaemon('/tmp/iaaspaste.pid',
              '/dev/null',
                 '/tmp/iaaspaste_out.log',
              '/tmp/iaaspaste_err.log')
    
    daemon.do(wsgi_app)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
