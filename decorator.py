#!/usr/bin/env python
#*-*coding:utf-8*-*
#

import json

class ResponseDecorator():
    def __init__(self):
        self.data = {}
        self.fin_rsp = {}
        self.fin_rsp_j = None

    def get_images_deco(self, func):
        def get_image_rsp_deco():
            rsp = func()
            self.fin_rsp = {}
            self.data = {}
            self.data['images'] = []
            for i in range(len(rsp['data']['images'])):
                self.data['images'].append({"id": rsp['data']['images'][i]['id'], 
                                                                "name": rsp['data']['images'][i]['name']})
            self.fin_rsp['data'] = self.data
            self.fin_rsp_j = json.dumps(self.fin_rsp)
            return self.fin_rsp_j
        return get_image_rsp_deco

    def get_flavors_deco(self, func):
        def get_flavors_rsp_deco():
            rsp = func()
            self.data['success'] = True
            self.data['message'] = ""
            self.data['flavors'] = []
            for i in range(len(rsp['data']['flavors'])):
                self.data['flavors'].append({"id": rsp['data']['flavors'][i]['id'],
                                                               "name": rsp['data']['flavors'][i]['name'],
                                                               "vcpus": rsp['data']['flavors'][i]['vcpus'],
                                                               "memory": rsp['data']['flavors'][i]['ram'],
                                                               "disk": rsp['data']['flavors'][i]['disk']})
            self.fin_rsp['data'] = self.data
            self.fin_rsp_j = json.dumps(self.fin_rsp)
            return self.fin_rsp_j
        return get_flavors_rsp_deco

    def create_tenant_deco(self, func):
        def create_tenant_rsp_deco():
            rsp = func()
            self.data['success'] = True
            self.data['message'] = ""
            tenant_id = rsp['data']['tenant']['id']
            self.data['tenantId'] = tenant_id
            self.fin_rsp['data'] = self.data
            self.fin_rsp_j = json.dumps(self.fin_rsp)
            return self.fin_rsp_j
        return create_tenant_rsp_deco

    def get_quota_deco(self, func):
        def get_quota_rsp_deco():
            rsp = func()
            quota = {}
            self.data['message'] = ""
            self.data['quotas'] = {}
            self.data['success'] = True

            iaas_quota = rsp['data']['quota_set']
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
            self.data['quotas'] = quota

            if self.data['quotas']:
                self.data['message'] = "获取配额成功"

            self.fin_rsp['data'] = self.data
            self.fin_rsp_j = json.dumps(self.fin_rsp)
            return self.fin_rsp_j
        return get_quota_rsp_deco

    def  release_tenant_deco(self, func):
        def release_tenant_rsp_deco():
            rsp = func()
            self.data['message'] = ""
            self.data['success'] = rsp['data']['success']
            self.fin_rsp['data'] = self.data
            self.fin_rsp_j = json.dumps(self.fin_rsp)
            return self.fin_rsp_j
        return release_tenant_rsp_deco