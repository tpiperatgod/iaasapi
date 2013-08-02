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
import logging
from contextlib import closing

DEBUG = True
SECRET_KEY = 'I AM TURTLE ENDER'

app = Flask(__name__)
app.config.from_object('iaasapi.config')

@app.before_request     
def before_request():
    pass
        
def teardown_request(exception):
    pass

@app.route('/')
def index():
    print app.config.RABBITMQ_IP

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')