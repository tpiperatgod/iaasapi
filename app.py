#!/usr/bin/env python
#*-*coding:utf-8*-*
#
from __future__ import with_statement


import sys
import utils
import logging
import logging.config

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, Blueprint, abort, jsonify

from tasks import checkserver

import decorator


RSPDE = decorator.ResponseDecorator()

reload(sys)
sys.setdefaultencoding('utf8')

DEBUG = True
SECRET_KEY = 'I AM TURTLE ENDER'

app = Flask(__name__)
app.config.from_object('config')

logging.config.fileConfig("logging.conf")
LOG = logging.getLogger(__name__)

REQ_START = "*"*20 + "  REQUEST START  " + "*"*20
REQ_END = "*"*20 + "  REQUEST END  " + "*"*20
RSP_START = "*"*20 + "  RESPONSE START  " + "*"*20
RSP_END = "*"*20 + "  RESPONSE END  " + "*"*20

@app.before_request
def before_request():
    LOG.debug(REQ_START)
    g.iaas = utils.DoAsIAAS()
    g.env = request.environ
    g.p = request.args
    g.h = request.headers
    pass


@app.teardown_request
def teardown_request(exception):
    pass

@app.route('/', methods=['POST', 'GET'])
def index():
    power_info = ">> [*] IAASAPI POWER ON [*]"
    version_info = ">> VERSION 1.0 on Flask"
    author_info = ">> by turtle_ender @2013.8"
    print g.p
    LOG.debug(power_info)
    LOG.debug(version_info)
    LOG.debug(author_info)
    info = power_info + '\n' + version_info + '\n' + author_info
    return info

@app.route('/services/iaasCreateServer.action', methods=['POST'])
def create_server():
    image_id = g.p.get('imageId', None)
    flavor_id = g.p.get('flavorId', None)
    quantity = int(g.p.get('quantity', None))
    appkey = g.h.get('x-wocloud-iaas-appkey', None)
    _type = 'check_status'
    LOG.debug('>> image id:\t %(image_id)s <<' % locals())
    LOG.debug('>> flavor id:\t %(flavor_id)s <<' % locals())
    LOG.debug('>> quantity:\t %(quantity)s <<' % locals())
    LOG.debug('>> appkey:\t %(appkey)s <<' % locals())
    LOG.debug(REQ_END)
    if image_id and flavor_id:
        rsp, delay_rsp, t = g.iaas.create_server(image_id, flavor_id, appkey, quantity)
        res = checkserver.apply_async((quantity, delay_rsp, t, _type))
        context = {"id": res.task_id, "delay_req": delay_rsp, "time": t, "type": _type}
        LOG.debug(">>> CELERY MSG: %(context)s" % locals())
        return rsp
    else:
        return None

@app.route('/services/iaasStartServer.action', methods=['POST'])
def start_server():
    server_id = g.p.get('serverId', None)
    LOG.debug('>> server id:\t %(server_id)s <<' % locals())
    LOG.debug(REQ_END)
    rsp = g.iaas.start_server(server_id)
    return rsp

@app.route('/services/iaasStopServer.action', methods=['POST'])
def stop_server():
    server_id = g.p.get('serverId', None)
    LOG.debug('>> server id:\t %(server_id)s <<' % locals())
    LOG.debug(REQ_END)
    rsp = g.iaas.stop_server(server_id)
    return rsp

@app.route('/services/iaasCheckServer.action', methods=['POST'])
def check_server():
    server_id = g.p.get('serverId', None)
    LOG.debug('>> server id:\t %(server_id)s <<' % locals())
    LOG.debug(REQ_END)
    rsp = g.iaas.check_server(server_id, _type='normal')
    return rsp

@app.route('/services/iaasGetServerStatus.action', methods=['POST'])
def get_status():
    server_id = g.p.get('serverId', None)
    LOG.debug('>> server id:\t %(server_id)s <<' % locals())
    LOG.debug(REQ_END)
    rsp = g.iaas.check_server(server_id, _type='check_status')
    return rsp

@app.route('/services/iaasReleaseServer.action', methods=['POST'])
def release_server():
    server_id = g.p.get('serverId', None)
    LOG.debug('>> server id:\t %(server_id)s <<' % locals())
    LOG.debug(REQ_END)
    rsp = g.iaas.release_server(server_id)
    return rsp

@app.route('/services/iaasGetOsTenant.action', methods=['POST'])
@RSPDE.create_tenant_deco
def create_tenant():
    tenant_name = g.p.get('portalTenantId', None)
    LOG.debug('>> tenant name:\t %(tenant_name)s <<' % locals())
    LOG.debug(REQ_END)
    rsp = g.iaas.create_tenant(tenant_name)
    return rsp

@app.route('/services/iaasReleaseTenant.action', methods=['POST'])
@RSPDE.release_tenant_deco
def release_tenant():
    LOG.debug('>> release tenant <<')
    tenant_id = g.h.get('x-wocloud-iaas-tenantid', None)
    LOG.debug('>> tenant id:\t %(tenant_id)s <<' % locals())
    LOG.debug(REQ_END)
    rsp = g.iaas.release_tenant(tenant_id)
    return rsp

@app.route('/services/iaasGetQuotas.action', methods=['POST'])
@RSPDE.get_quota_deco
def get_quota():
    LOG.debug('>> get quota <<')
    tenant_id = g.h.get('x-wocloud-iaas-tenantid', None)
    LOG.debug('>> tenant id:\t %(tenant_id)s <<' % locals())
    LOG.debug(REQ_END)
    rsp = g.iaas.get_quota(tenant_id)
    return rsp

@app.route('/services/iaasGetImages.action', methods=['POST'])
@RSPDE.get_images_deco  
def get_images():
    LOG.debug('>> get images <<')
    LOG.debug(REQ_END)
    rsp = g.iaas.get_images()
    return rsp

@app.route('/services/iaasGetFlavors.action', methods=['POST'])
@RSPDE.get_flavors_deco
def get_flavors():
    LOG.debug('>> get flavors <<')
    LOG.debug(REQ_END)
    rsp = g.iaas.get_flavors()
    return rsp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
