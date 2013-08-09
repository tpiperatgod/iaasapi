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


@app.before_request
def before_request():
    g.iaas = utils.DoAsIAAS()
    pass


@app.teardown_request
def teardown_request(exception):
    pass


@app.route('/', methods=["POST"])
def index():

    return '[*] IAASAPI POWER ON [*]'





@app.route('/check_server/<server_id>/<_type>')
def check_server(server_id, _type='normal'):
    res = checkserver.apply_async((server_id, _type))
    context = {"id": res.task_id, "server_id": server_id, "type": _type}
    goto = "{}".format(context['id'])
    return jsonify(goto=goto)

@app.route('/create_tenant/<tenant_name>')
@RSPDE.create_tenant_deco
def create_tenant(tenant_name):
    rsp = g.iaas.create_tenant(tenant_name)
    return rsp

@app.route('/release_tenant/<tenant_id>')
def release_tenant(tenant_id):
    rsp = g.iaas.release_tenant(tenant_id)
    return rsp

@app.route('/get_quota/', methods=['POST'])
@RSPDE.get_quota_deco
def get_quota():
    tenant_id = request.form.get('tenant_id', None)
    print tenant_id
    rsp = g.iaas.get_quota(tenant_id)
    return rsp

@app.route('/get_images')
@RSPDE.get_images_deco  
def get_images():
    rsp = g.iaas.get_images()
    return rsp

@app.route('/get_flavors')
@RSPDE.get_flavors_deco
def get_flavors():
    rsp = g.iaas.get_flavors()
    return rsp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
