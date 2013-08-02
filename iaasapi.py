#!/usr/bin/env python
#*-*coding:utf-8*-*
#

from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from hashlib import md5
import time
import MySQLdb
import sys
import types
reload(sys)
sys.setdefaultencoding('utf8')
from contextlib import closing

import logging
import logging.config

import json
import httplib
import urlparse
import urllib
#import pika, uuid
import os
import subprocess
import random

DEBUG = True
SECRET_KEY = 'I AM TURTLE ENDER'

app = Flask(__name__)
app.config.from_object('config')

logging.config.fileConfig("logging.conf")
LOG = logging.getLogger(__name__)

@app.before_request
def before_request():
    g.token, nova_url = get_token()
    g.nova_path = nova_url[2]
    pass

@app.teardown_request
def teardown_request(exception):
    pass



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


def iaas_func(_req):  
    '''
    _req = {"flag": func_name,
            "url": keystone_url,
            "method": method_temp['post'],
            "path": "/v2.0/tenants",
            "params": json.dumps(_params),
            "headers": headers_temp % _token_id}
    _rsp = {"flag": "func_name",
            "data": {"...": "...",
                     "...": "...",
                     "...": "..."}}
    '''
    data = json.loads(_req)
    conn = GetHTTPConnect(data['url'], data['method'], data['path'], data['params'], data['headers'])
    iaas_rsp = conn.get_data()
    rsp_to_box = {}
    rsp_to_box['flag'] = data['flag']
    try: 
        rsp_to_box['data'] = json.loads(iaas_rsp)
    except:
        rsp_to_box['data'] = {"success": True}
    rsp = json.dumps(rsp_to_box)
    return rsp

def get_token():
    params = '{"auth": {"tenantName": "%s", "passwordCredentials": {"username": "%s", "password": "%s"}}}' \
                % (app.config['ADMIN_TENANT'], app.config['USER_NAME'], app.config['ADMIN_TENANT_PASSWORD'])
    headers = {"Content-type": "application/json"}
    req = {"flag": "getToken",
           "url": app.config['OPSTACK_IP'] + ':35357',
           "method": "POST",
           "path": app.config['SERVICE_PATH_TEMP']['getToken'],
           "params": params,
           "headers": headers}
    
    rreq = json.dumps(req)
    rsp = json.loads(iaas_func(rreq))
    token_id = rsp['data']['access']['token']['id']
    
    try:
        for i in range(len(rsp['data']['access']['serviceCatalog'])):
            server_ctl = rsp['data']['access']['serviceCatalog'][i]
            if server_ctl.get('name', None) == 'Compute Service':
                nova_url = urlparse.urlparse(
                    server_ctl['endpoints'][0].get('publicURL', None))
    except e:
        LOG.error("Can not get server catalog, error: %(error)s", {'error': e})
        
    return token_id, nova_url

@app.route('/')
def index():
    LOG.debug("+"*20)
    LOG.debug("token: %(token)s, nova: %(nova)s", 
              {'token': g.token, 'nova': g.nova_path})
    LOG.debug("+"*20)
    return 'a'

@app.route('/get_quota/<tenant_id>')
def get_quota(tenant_id):
    LOG.debug("start get quota")
    headers = {"X-Auth-Token": g.token, "Content-type": "application/json",
               "X-Auth-Project-Id": "admin"}
 
    req = {"flag": "getQuota",
           "url": app.config['NOVA_IP'],
           "method": "GET",
           "path": app.config['SERVICE_PATH_TEMP']['getQuota'] % (g.nova_path, tenant_id),
           "params": urllib.urlencode({}),
           "headers": headers}
 
    rreq = json.dumps(req)
    rsp_from_iaas = json.loads(iaas_func(rreq))
    
    rsp = {}
    data = {}
    quota = {}
    data['message'] = ""
    data['quotas'] = {}
    data['success'] = True 
    
    iaas_quota = rsp_from_iaas['data']['quota_set']
    quota['cores'] = iaas_quota.get('cores', None)
    quota['floatingIps'] = iaas_quota.get('floating_ips', None)
    quota['gigaBytes'] = iaas_quota.get('gigabytes', None)
    quota['injectedFileContentBytes'] = iaas_quota.get('injected_file_content_bytes', None)
    quota['injectedFilePathBytes'] = iaas_quota.get('injected_file_path_bytes', None)
    quota['injectedFiles'] = iaas_quota.get('injected_files', None)
    quota['instances'] = iaas_quota.get('instances', None)
    quota['keyPairs'] = iaas_quota.get('key_pairs', None)
    quota['metadataItems'] = iaas_quota.get('metadata_items', None)
    quota['ram'] = iaas_quota.get('ram', None)
    quota['securityGroupRules'] = iaas_quota.get('cores', None)
    quota['securityGroups'] = iaas_quota.get('security_groups', None)
    quota['volumes'] = iaas_quota.get('volumes', None)
    data['quotas'] = quota
     
    if data['quotas']:
        data['message'] = "获取配额成功"
         
    rsp['data'] = data
    fin_rsp = json.dumps(rsp)
    return fin_rsp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
