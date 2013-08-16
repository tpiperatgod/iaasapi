#!/usr/bin/env python
#*-*coding:utf-8*-*
#

import json
import httplib
import urlparse
import urllib
import os

SER_ID = "75821b8b-03ff-4a57-81b6-9fd2cd74e2b3"
TENT_NAME = "test_t"
IMG_ID = "ef132735-2419-4984-8d12-2a769cdb5abd"
FLR_ID = "d97a0d30-537a-4543-9aa8-2aed966d1b10"
Q = "1"
appkey = "3a754eb9-7689-4d9a-ab9a-g451sd124113"
TENT_ID = "e6442e3d73cc4a848d5acb44b618c144"

class GetHTTPConnect():

    def __init__(self, url, method, path, params, headers):
        self.url = url
        self.method = method
        self.path = path
        self.params = params
        self.headers = headers

    def get_data(self):
        try:
            conn = httplib.HTTPConnection(self.url)
            conn.request(self.method, self.path, self.params, self.headers)
            response = conn.getresponse()
            rsp = response.read()
            conn.close()
            try:
                rrsp = json.loads(rsp)
            except:
                rrsp = rsp
            finally:
                rrsp = rsp
        except:
            rsp = '[EEEOR] : unable to connect'
        finally:
            rrsp = rsp
        return rrsp

def index():
    url = "localhost:8080"
    method = "POST"
    params = urllib.urlencode({})
    path = '?%(params1)s' % locals() 
    headers = {"Content-type": "application/json"}
    conn = GetHTTPConnect(url, method, path, params, headers)
    rsp = conn.get_data()

    print rsp

def get_quota():
    url = "localhost:8080"
    method = "POST"
    params = urllib.urlencode({})
    path = '/services/iaasGetQuotas.action?%(params)s' % locals() 
    headers = {"Content-type": "application/json", "x-wocloud-iaas-tenantid": TENT_ID}
    conn = GetHTTPConnect(url, method, path, params, headers)
    rsp = conn.get_data()

    print rsp

def get_image():
    url = "localhost:8080"
    method = "POST"
    params = urllib.urlencode({})
    path = '/services/iaasGetImages.action?%(params)s' % locals() 
    headers = {"Content-type": "application/json"}
    conn = GetHTTPConnect(url, method, path, params, headers)
    rsp = conn.get_data()

    print rsp

def get_flavor():
    url = "localhost:8080"
    method = "POST"
    params = urllib.urlencode({})
    path = '/services/iaasGetFlavors.action?%(params)s' % locals() 
    headers = {"Content-type": "application/json"}
    conn = GetHTTPConnect(url, method, path, params, headers)
    rsp = conn.get_data()

    print rsp

def create_server():
    url = "localhost:8080"
    method = "POST"
    params1 = 'imageId=%s&flavorId=%s&quantity=%s' % (IMG_ID, FLR_ID, quantity)
    params = urllib.urlencode({})
    path = '/services/iaasCreateServer.action?%(params1)s' % locals() 
    headers = {"Content-type": "application/json", "x-wocloud-iaas-appkey": appkey}
    conn = GetHTTPConnect(url, method, path, params, headers)
    rsp = conn.get_data()

    print rsp

def start_server():
    url = "localhost:8080"
    method = "POST"
    params1 = 'serverId=%s' % SER_ID  
    params = urllib.urlencode({})
    path = '/services/iaasStartServer.action?%(params1)s' % locals() 
    headers = {"Content-type": "application/json"}
    conn = GetHTTPConnect(url, method, path, params, headers)
    rsp = conn.get_data()

    print rsp

def stop_server():
    url = "localhost:8080"
    method = "POST"
    params1 = 'serverId=%s' % SER_ID 
    params = urllib.urlencode({})
    path = '/services/iaasStopServer.action?%(params1)s' % locals() 
    headers = {"Content-type": "application/json"}
    conn = GetHTTPConnect(url, method, path, params, headers)
    rsp = conn.get_data()

    print rsp

def check_server():
    url = "localhost:8080"
    method = "POST"
    params1 = 'serverId=%s' % SER_ID 
    params = urllib.urlencode({})
    path = '/services/iaasCheckServer.action?%(params1)s' % locals() 
    headers = {"Content-type": "application/json"}
    conn = GetHTTPConnect(url, method, path, params, headers)
    rsp = conn.get_data()

    print rsp

def get_status():
    url = "localhost:8080"
    method = "POST"
    params1 = 'serverId=%s' % SER_ID
    params = urllib.urlencode({})
    path = '/services/iaasGetServerStatus.action?%(params1)s' % locals() 
    headers = {"Content-type": "application/json"}
    conn = GetHTTPConnect(url, method, path, params, headers)
    rsp = conn.get_data()

    print rsp

def release_server():
    url = "localhost:8080"
    method = "POST"
    params1 = 'serverId=%s' % SER_ID 
    params = urllib.urlencode({})
    path = '/services/iaasReleaseServer.action?%(params1)s' % locals() 
    headers = {"Content-type": "application/json"}
    conn = GetHTTPConnect(url, method, path, params, headers)
    rsp = conn.get_data()

    print rsp

def create_tenant():
    url = "localhost:8080"
    method = "POST"
    params1 = 'portalTenantId=%s' % TENT_NAME 
    params = urllib.urlencode({})
    path = '/services/iaasGetOsTenant.action?%(params1)s' % locals() 
    headers = {"Content-type": "application/json"}
    conn = GetHTTPConnect(url, method, path, params, headers)
    rsp = conn.get_data()

    print rsp

def release_tenant():
    t_id = "107b51890f474eae83403333813153f2"
    url = "localhost:8080"
    method = "POST"
    params = urllib.urlencode({})
    path = '/services/iaasReleaseTenant.action?%(params)s' % locals() 
    headers = {"Content-type": "application/json", "x-wocloud-iaas-tenantid": t_id}
    conn = GetHTTPConnect(url, method, path, params, headers)
    rsp = conn.get_data()

    print rsp

if __name__ == '__main__':
    index()
    #get_quota()
    #get_image()
    #get_flavor()
    #create_server()
    #start_server()
    #stop_server()
    #release_server()
    #create_tenant()
    #release_tenant()
    #check_server()
    #get_status()
    