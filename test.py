#!/usr/bin/python
#*-*coding:utf-8*-*
#
#IaaSapitest
#
import iaasapi as api

_host_ip = '192.168.1.15'
token_id, nova_url, keystone_adminurl, keystone_publicurl = api.iaas_get_token('192.168.1.15')
_nova_ip = _host_ip + ':8774'
_nova_path = nova_url[2]
_keystone_ip = _host_ip + ':35357'
_quantum_ip = '192.168.1.14:9696'
_image_id ='74bacf45-99a1-4f44-aee6-3ce5cc984c05'
_flavor_id = '1'
appkey = '3a754eb9-7689-4d9a-ab9a-g451sd124113'
_networ_id = '368f9765-9461-4ad7-94e2-97069b5c50d5'
_disk_dir = "/private_dev_sdb"
quantity = 1

#创建云租户
#rsp = api.iaas_create_tenant(_keystone_ip)

#释放云租户
#rsp = api.iaas_release_tenant(_keystone_ip, '4ec70537c2f14cf89c2faad630c5b99f')

#获取租户配额
#rsp = api.iaas_get_quota(token_id, _nova_ip, _nova_path, '10a2f70ecc53471d9b91f6b15a429e0a')

#查询云主机运行状态
#rsp = api.iaas_check_server(token_id, _nova_ip, _nova_path, 'a96bbfbb-ddca-430a-a765-619e48f6cc81', _type='normal')

#查询云主机当前状态
#rsp = api.iaas_check_server(token_id, _nova_ip, _nova_path, 'a96bbfbb-ddca-430a-a765-619e48f6cc81', _type='check_status')

#获取云主机网络信息
#rsp = api.iaas_check_server(token_id, _nova_ip, _nova_path, '7e5a209f-3f13-4b6e-a3be-84fb684e985a', _type='get_ip_info')

#获取image列表
#rsp = api.iaas_get_images(token_id, _nova_ip, _nova_path)

#获取flavor列表
#rsp = api.iaas_get_flavors(token_id, _nova_ip, _nova_path)

#创建云主机功能
rsp = api.iaas_create_server(token_id, _nova_ip, _nova_path, _image_id, _flavor_id, appkey, _networ_id, _disk_dir, _quantum_ip, quantity)

#启动云主机
#rsp = api.iaas_start_server(token_id, _nova_ip, _nova_path, '9cdeadac-6c6f-4f20-81ed-147cd2d4276a')
#关闭云主机
#rsp = api.iaas_stop_server(token_id, _nova_ip, _nova_path, '9cdeadac-6c6f-4f20-81ed-147cd2d4276a')

#释放云主机功能
#rsp = api.iaas_release_server(token_id, _nova_ip, _nova_path, '9cdeadac-6c6f-4f20-81ed-147cd2d4276a')

print rsp
