#!/usr/bin/env python
#*-*coding:utf-8*-*
#

from __future__ import absolute_import
from celery import Celery
import time
import config as FLAG
import utils
import pika
import json

celery = Celery("tasks",
                broker='amqp://guest:guest@192.168.81.128:5672',
                backend='amqp')

g_iaas = utils.DoAsIAAS()


def send_message_callback(msg):
    print("send_message_callback")
    sp_msg = json.dumps(msg)

    try:
        credentials = pika.PlainCredentials(
            FLAG.RABBITMQ_USER, FLAG.RABBITMQ_PASSWORD)
        params = pika.ConnectionParameters(
            host=FLAG.RABBITMQ_IP, port=FLAG.RABBITMQ_PORT, credentials=credentials)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.exchange_declare(
            exchange=FLAG.RABBITMQ_EXCHANGE, exchange_type='fanout')
        channel.basic_publish(
            exchange=FLAG.RABBITMQ_EXCHANGE, routing_key='', body=sp_msg)
        connection.close()
    except Exception, e:
        print("send message failed:", str(e))
    print("send msg over.")


@celery.task(name="tasks.checkserver")
def checkserver(quantity, delay_req, server_id, _type='check_status'):
    act = 0
    for i in range(24):
        time.sleep(5)
        vm_info = []
        for x in range(quantity):
            server_id = delay_req[x]['data']['server']['id']
            passwd = delay_req[x]['data']['server']['adminPass']
            try:
                status = json.loads(g_iaas.check_server(server_id, 'check_status'))

                status = status['data']['status']
            except:
                status['data']['status'] = 'ERROR'

            vm_info.append({'id': server_id,
                            'passwd': passwd,
                            'status': status['data']['status']})
            if status['data']['status'] != 'ACTIVE':
                if status == 'ERROR':
                    continue
            else:
                act += 1
                continue

        if act == quantity:
            break

    data = {}
    data['success'] = True
    data['servers'] = []

    print vm_info, len(vm_info)

    for vm in vm_info:
        data_server = {}
        print vm
        print "++"
        server_id = vm['id']
        ip = g_iaas.check_server(server_id, 'get_ip_info')
        data_server['id'] = server_id
        data_server['passwd'] = vm['passwd']
        data_server['ip'] = ip
        data_server['status'] = vm['status']
        data['servers'].append(data_server)

    data['message'] = "云主机创建成功"
    data['seq'] = t
    rsp = data
    send_message_callback(rsp)
    send_message_callback(status)
    return

if __name__ == "__main__":
    celery.start()
            
