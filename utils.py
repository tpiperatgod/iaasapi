#!/usr/bin/env python
#*-*coding:utf-8*-*
#
import config as FLAG
import json
import httplib
import urlparse
import urllib
import os
import sys
import time
import subprocess
import random
import decorator

RSPDE = decorator.ResponseDecorator()


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


class DoAsIAAS():

    """do as iaas"""

    def __init__(self):
        first_rsp, second_rsp = self.get_token()
        if first_rsp:
            self.token, nova_url = self.get_token()
            self.nova_path = nova_url[2]
        else:
            return second_rsp

    def node_allow(self, node):
        cmd = """ping %s -c2 1> /dev/null
                if [ $? -eq 0 ];
                then
                    echo 1;
                else
                    echo 0;
                fi""" % node

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        allow = p.stdout.readline()

        if int(allow):
            return True
        else:
            return False

    def node_scheduler(self):
        FIN_NODE = []
        for k, v in FLAG.NODE_MAP.items():
            if not self.node_allow(v):
                FLAG.NODE_MAP.pop(k)

        node_no = random.randint(0, len(FLAG.NODE_MAP) - 1)
        n_k, n_v = FLAG.NODE_MAP.items()[node_no]
        if n_k and n_v:
            FIN_NODE.append(n_k)
        return FIN_NODE

    def knock_iaas(self, req):
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
        data = json.loads(req)
        conn = GetHTTPConnect(
            data['url'], data['method'], data['path'], data['params'], data['headers'])
        iaas_rsp = conn.get_data()
        rsp_to_box = {}
        rsp_to_box['flag'] = data['flag']
        try:
            rsp_to_box['data'] = json.loads(iaas_rsp)
        except:
            rsp_to_box['data'] = {"success": True}
        rsp = json.dumps(rsp_to_box)
        return rsp

    def get_token(self):
        params = '{"auth": {"tenantName": "%s", "passwordCredentials": {"username": "%s", "password": "%s"}}}' \
            % (FLAG.ADMIN_TENANT, FLAG.USER_NAME, FLAG.ADMIN_TENANT_PASSWORD)
        headers = {"Content-type": "application/json"}
        req = {"flag": "getToken",
                   "url": FLAG.OPSTACK_IP + ':35357',
                   "method": "POST",
                   "path": FLAG.SERVICE_PATH_TEMP['getToken'],
                   "params": params,
                   "headers": headers}

        rreq = json.dumps(req)
        rsp = json.loads(self.knock_iaas(rreq))
        token_id = rsp['data']['access']['token']['id']

        try:
            for i in range(len(rsp['data']['access']['serviceCatalog'])):
                server_ctl = rsp['data']['access']['serviceCatalog'][i]
                if server_ctl.get('name', None) == 'Compute Service':
                    nova_url = urlparse.urlparse(
                        server_ctl['endpoints'][0].get('publicURL', None))
        except:
            err = "Cannot get serviceCatalog"
            return False, err

        return token_id, nova_url

    def create_tenant(self, tenant_name):
        params = '{"tenant": {"enabled": true, "name": "%s", "description": null}}' % tenant_name
        headers = {"X-Auth-Token": FLAG.ADMIN_TOKEN,
                   "Content-type": "application/json"}
        req = {"flag": "createTenant",
                   "url": FLAG.KEYSTONE_IP,
                   "method": "POST",
                   "path": FLAG.SERVICE_PATH_TEMP['createTenant'],
                   "params": params,
                   "headers": headers}

        rreq = json.dumps(req)
        rsp_from_iaas = json.loads(self.knock_iaas(rreq))
        return rsp_from_iaas

    def release_tenant(self, tenant_id):
        params = urllib.urlencode({})
        headers = {"X-Auth-Token": FLAG.ADMIN_TOKEN,
                   "Content-type": "application/json"}
        req = {"flag": "releaseTenant",
                   "url": FLAG.KEYSTONE_IP,
                   "method": "DELETE",
                   "path": FLAG.SERVICE_PATH_TEMP['releaseTenant'] % tenant_id,
                   "params": params,
                   "headers": headers}

        rreq = json.dumps(req)
        rsp_from_iaas = json.loads(self.knock_iaas(rreq))
        return rsp_from_iaas

    def get_quota(self, tenant_id):
        headers = {
            "X-Auth-Token": self.token, "Content-type": "application/json",
            "X-Auth-Project-Id": "admin"}

        req = {"flag": "getQuota",
                   "url": FLAG.NOVA_IP,
                   "method": "GET",
                   "path": FLAG.SERVICE_PATH_TEMP['getQuota'] % (self.nova_path, tenant_id),
                   "params": urllib.urlencode({}),
                   "headers": headers}

        rreq = json.dumps(req)
        rsp_from_iaas = json.loads(self.knock_iaas(rreq))
        return rsp_from_iaas

    def create_port(self):
        params = '{"port": {"network_id": "%s", "attached_phyport": "%s", "admin_state_up": true}}' \
            % (FLAG.NETWORK_ID, FLAG.IFACE)
        headers = {"X-Auth-Token": self.token,
                   "Content-type": "application/json"}

        req = {"flag": "createPort",
                   "url": FLAG.QUANTUM_IP,
                   "method": "POST",
                   "path": FLAG.SERVICE_PATH_TEMP['createPort'],
                   "params": params,
                   "headers": headers}

        rreq = json.dumps(req)
        rsp_from_iaas = json.loads(self.knock_iaas(rreq))
        port_id = rsp_from_iaas['data']['port']['id']
        return port_id

    def create_acl(self, port_id):
        params = """{"acl": {"src": "0.0.0.0/0", "tenant_id": "%s",
                    "port_id": "%s", "name": "%s", "proto": "IP"}}""" % \
            (FLAG.ADMIN_TENANT_ID, port_id, FLAG.ACL_NAME)
        headers = {"X-Auth-Token": self.token,
                   "Content-type": "application/json"}

        req = {"flag": "createAcl",
                   "url": FLAG.QUANTUM_IP,
                   "method": "POST",
                   "path": FLAG.SERVICE_PATH_TEMP['createAcl'],
                   "params": params,
                   "headers": headers}

        rreq = json.dumps(req)
        rsp_from_iaas = json.loads(self.knock_iaas(rreq))
        return rsp_from_iaas

    def create_server(self, image_id, flavor_id, appkey, quantity):
        fin_node = self.node_scheduler()
        t = time.time()
        t = int(t)
        delay_rsp = []
        rsp = {}
        req_data = {}
        req_data['seq'] = t
        req_data['msg'] = "正在发送rabbitMQ，请获取对应云主机数据！"
        req_data['success'] = True
        req_data['timeout'] = 120
        rsp['data'] = req_data
        fin_rsp = json.dumps(rsp)

        for q in range(quantity):
            port_info = []
            port_id = self.create_port()
            print "+++++ PORT INFO: %(port_id)s +++++" % locals()
            acl = self.create_acl(port_id)
            print "+++++ ACL INFO: %(acl)s +++++" % locals()
            port_info.append({"uuid": "%s" % FLAG.NETWORK_ID, "port": "%s" % port_id})
            port_info = json.dumps(port_info)

            imageRef = "http://%s%s/images/%s" % (FLAG.NOVA_IP, self.nova_path, image_id)
            flavorRef = "http://%s%s/flavors/%s" % (FLAG.NOVA_IP, self.nova_path, flavor_id)
            params = """{"os:scheduler_hints": {"disk_dir": "%s"},
                            "server": {"name": "%s", "imageRef": "%s",
                            "availability_zone": "nova:%s", "flavorRef": "%s", "max_count": 1,
                            "min_count": 1, "networks": %s}}""" % \
                (FLAG.DISK_DIR, FLAG.SERVER_NAME_MAP[appkey], 
                    imageRef, fin_node[0], flavorRef, port_info)
            print "+++++" + params + "+++++"
            headers = {"X-Auth-Token": self.token,
                                "Content-type": "application/json"}

            req = {"flag": "createServer",
                       "url": FLAG.NOVA_IP,
                       "method": "POST",
                       "path": FLAG.SERVICE_PATH_TEMP['createServer'] % self.nova_path,
                       "params": params,
                       "headers": headers}

            rreq = json.dumps(req)
            rsp_from_iaas = json.loads(self.knock_iaas(rreq))
            delay_rsp.append(rsp_from_iaas)

        return fin_rsp, delay_rsp

    def start_server(self, server_id):
        params = '{"os-start": null}'
        headers = {"X-Auth-Token": self.token,
                   "Content-type": "application/json"}
        req = {"flag": "startServer",
               "url": FLAG.NOVA_IP,
               "method": "POST",
               "path": FLAG.SERVICE_PATH_TEMP['startServer'] % (self.nova_path, server_id),
               "params": params,
               "headers": headers}

        rsp = {}
        data = {}
        data['message'] = ""
        exist = self.check_server(server_id, 'normal')
        status = self.check_server(server_id, 'check_status')
        status = json.loads(status)
        if json.loads(exist)['data']['active'] == None:
            data['success'] = False
            data['message'] = "server %s is not exist" % server_id
        elif status['data']['status'] in ['ACTIVE']:
            data['message'] = "Cannot 'start' while instance is in vm_state %s" % status[
                'data']['status']
            data['success'] = False
        else:
            rreq = json.dumps(req)
            rsp_from_iaas = json.loads(self.knock_iaas(rreq))
            data['success'] = rsp_from_iaas['data']['success']
        rsp['data'] = data
        fin_rsp = json.dumps(rsp)
        return fin_rsp

    def stop_server(self, server_id):
        params = '{"os-stop": null}'
        headers = {"X-Auth-Token": self.token,
                   "Content-type": "application/json"}
        req = {"flag": "stopServer",
               "url": FLAG.NOVA_IP,
               "method": "POST",
               "path": FLAG.SERVICE_PATH_TEMP['stopServer'] % (self.nova_path, server_id),
               "params": params,
               "headers": headers}

        rsp = {}
        data = {}
        data['message'] = ""
        exist = self.check_server(server_id, 'normal')
        status = self.check_server(server_id, 'check_status')
        status = json.loads(status)
        if json.loads(exist)['data']['active'] == None:
            data['success'] = False
            data['message'] = "server %s is not exist" % server_id
        elif status['data']['status'] in ['SHUTOFF']:
            data['message'] = "Cannot 'stop' while instance is in vm_state %s" % status[
                'data']['status']
            data['success'] = False
        else:
            rreq = json.dumps(req)
            rsp_from_iaas = json.loads(self.knock_iaas(rreq))
            data['success'] = rsp_from_iaas['data']['success']
        rsp['data'] = data
        fin_rsp = json.dumps(rsp)
        return fin_rsp

    def release_server(self, server_id):
        headers = {"X-Auth-Token": self.token,
                   "Content-type": "application/json"}
        req = {"flag": "releaseServer",
               "url": FLAG.NOVA_IP,
               "method": "DELETE",
               "path": FLAG.SERVICE_PATH_TEMP['releaseServer'] % (self.nova_path, server_id),
               "params": urllib.urlencode({}),
               "headers": headers}

        rsp = {}
        data = {}
        data['message'] = ""
        exist = self.check_server(server_id, 'normal')
        status = self.check_server(server_id, 'check_status')
        if json.loads(exist)['data']['active'] == None:
            data['success'] = False
            data['message'] = "server %s is not exist" % server_id
        elif status in ['PAUSE', 'UNPAUSE', 'BUILD']:
            data[
                'message'] = "Cannot 'delete' while instance is in vm_state %s" % status
            data['success'] = False
        else:
            rreq = json.dumps(req)
            rsp_from_iaas = json.loads(self.knock_iaas(rreq))
            data['success'] = rsp_from_iaas['data']['success']
        rsp['data'] = data
        fin_rsp = json.dumps(rsp)
        return fin_rsp

    def check_server(self, server_id, _type='normal'):
        headers = {"X-Auth-Token": self.token,
                   "Content-type": "application/json"}
        req = {"flag": "checkServer",
               "url": FLAG.NOVA_IP,
               "method": "GET",
               "path": FLAG.SERVICE_PATH_TEMP['checkServer'] % (self.nova_path, server_id),
               "params": urllib.urlencode({}),
               "headers": headers}

        rsp = {}
        data = {}
        ip_data = []
        data['message'] = ""
        rreq = json.dumps(req)
        rsp_from_iaas = json.loads(self.knock_iaas(rreq))
        '''
        {u'flag': u'checkServer', u'data': {u'itemNotFound': {u'message': u'The resource could not be found.', u'code': 404}}}
        '''
        if rsp_from_iaas['data'].get('itemNotFound', None):
            data['success'] = False
            data['active'] = None
            data['message'] = rsp_from_iaas['data']['itemNotFound']['message']
        elif rsp_from_iaas['data'].get('server', None):
            data['success'] = True
            if _type == 'check_status':
                data['status'] = rsp_from_iaas['data']['server']['status']
                data['message'] = "云主机状态已查处"
            elif _type == 'get_ip_info':
                ip_name = rsp_from_iaas['data'][
                    'server']['addresses'].keys()[0]
                ip_data.append({"network": ip_name,
                                "version": rsp_from_iaas['data']['server']['addresses'][ip_name][0]['version'],
                                "addr": rsp_from_iaas['data']['server']['addresses'][ip_name][0]['addr']})
                return ip_data
            elif _type == 'normal':
                if rsp_from_iaas['data']['server']['status'] != 'ACTIVE':
                    data['active'] = False
                else:
                    data['active'] = True

        rsp['data'] = data
        fin_rsp = json.dumps(rsp)
        return fin_rsp

    def get_images(self):
        headers = {"X-Auth-Token": self.token,
                   "Content-type": "application/json"}
        req = {"flag": "getImages",
               "url": FLAG.NOVA_IP,
               "method": "GET",
               "path": FLAG.SERVICE_PATH_TEMP['getImages'] % self.nova_path,
               "params": urllib.urlencode({}),
               "headers": headers}

        rreq = json.dumps(req)
        rsp_from_iaas = json.loads(self.knock_iaas(rreq))
        return rsp_from_iaas

    def get_flavors(self):
        headers = {"X-Auth-Token": self.token,
                   "Content-type": "application/json"}
        req = {"flag": "getFlavors",
               "url": FLAG.NOVA_IP,
               "method": "GET",
               "path": FLAG.SERVICE_PATH_TEMP['getFlavors'] % self.nova_path,
               "params": urllib.urlencode({}),
               "headers": headers}

        rreq = json.dumps(req)
        rsp_from_iaas = json.loads(self.knock_iaas(rreq))
        return rsp_from_iaas
