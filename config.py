#RABBITMQ
RABBITMQ_IP = '192.168.0.55'
RABBITMQ_USER = 'guest'
RABBITMQ_PASSWORD = 'openstack'
RABBITMQ_EXCHANGE = 'createCloudHost'

#OPENSTACK
OPSTACK_IP = '192.168.0.55'
ADMIN_TENANT = 'admin'
ADMIN_TENANT_ID = 'e6442e3d73cc4a848d5acb44b618c144'
ADMIN_TENANT_PASSWORD = 'admin_pass'
ADMIN_TOKEN = 'admin'
USER_NAME = 'admin'
NOVA_IP = OPSTACK_IP + ':8774'
KEYSTONE_IP = OPSTACK_IP + ':35357'

#QUANTUM
QUANTUM_IP = '192.168.0.56:9696'
ACL_NAME = 'ACLNAME'
NETWORK_ID = 'f8aff156-7e5b-4286-8883-67b1e7aa7c8d'
IFACE = 'eth1'

#COMPUTE
INSTANCE_NAME = 'INSTANCE'
DISK_DIR = '/ft_storage'

#NODE
NODE_MAP = {'NN2': '192.168.0.57',
            'NN3': '192.168.0.58'}

#IAASAPI
SERVER_IP = '172.18.1.17'
SERVER_PORT = '8080'

SERVICE_PATH_TEMP = {'getToken': "/v2.0/tokens",
                     'createTenant': "/v2.0/tenants",
                     'releaseTenant': "/v2.0/tenants/%s",
                     'getQuota': "/%s/os-quota-sets/%s",
                     'createPort': "/v2.0/ports",
                     'createServer': "/%s/servers",
                     'startServer': "/%s/servers/%s/action",
                     'stopServer': "/%s/servers/%s/action",
                     'releaseServer': "/%s/servers/%s",
                     'checkServer': "/%s/servers/%s",
                     'startServer': "/%s/servers/%s/action",
                     'stopServer': "/%s/servers/%s/action",
                     'getImages': "/%s/images/detail",
                     'getFlavors': "/%s/flavors/detail",
                     'createAcl': "/v2.0/acls"}