#!/usr/bin/env python
#*-*coding:utf-8*-*
#

from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from hashlib import md5
import time
import sys
import types
reload(sys)
sys.setdefaultencoding('utf8')
from contextlib import closing

import logging
import logging.config

DEBUG = True
SECRET_KEY = 'I AM TURTLE ENDER'

app = Flask(__name__)
app.config.from_object('config')

logging.config.fileConfig("logging.conf")
LOG = logging.getLogger(__name__)

@app.before_request
def before_request():
    pass

@app.teardown_request
def teardown_request(exception):
    pass

'''
def get_token(host_ip):
    global G_INFO
    params = '{"auth": {"tenantName": "%s", "passwordCredentials": {"username": "%s", "password": "%s"}}}' 
                % (G_INFO['tenant'], G_INFO['user'], G_INFO['password'])
    headers = {"Content-type": "application/json"}
    req = {"flag": "getToken",
           "url": _host_ip + ':35357',
           "method": "POST",
           "path": SERVICE_PATH_TEMP['getToken'],
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
            elif server_ctl.get('name', None) == 'Identity Service':
                keystone_adminurl = urlparse.urlparse(
                    server_ctl['endpoints'][0].get('adminURL', None))
                keystone_publicurl = urlparse.urlparse(
                    server_ctl['endpoints'][0].get('publicURL', None))
    except e:
        LOG.error("Can not get server catalog, error: %(error)s", {'error': e})


    return token_id, nova_url, keystone_adminurl, keystone_publicurl
'''

@app.route('/')
def index():
    LOG.debug(app.config['RABBITMQ_IP'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
