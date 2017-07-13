#!/usr/bin/python

import pdb as xuao
import json
import requests
import commands
from config import *


def get_token():
    print "Getting token"
    auth_token = {}
    for project in user_map:
        project_id = project['project_id']
        project_name = project['project_name']
        auth_token[project_name] = []
        for user in project['user_info']:
            user_id = user['user_id']
            user_name = user['user_name']
            password = user['password']

            url = "http://%(manage_ip)s:5000/v3/auth/tokens" % {'manage_ip': manage_ip}
            params = {"auth": {"identity": { "methods": ["password"],
                      "password": {"user": {"id": user_id,
                      "password": password}}},
                      "scope": {"project": { "id": project_id}}}}
            headers = {'content-type': 'application/json'}
            data = json.dumps(params)
            res = requests.post(url, data = data, headers = headers)
            token = res.headers.get('x-subject-token')

            auth_token[project_name].append({'user_name': user_name, 'user_id': user_id, 'token': token})
    return auth_token


def net_list(token):
    url = "http://%(manage_ip)s:9696/v2.0/networks.json" % {'manage_ip': manage_ip}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    res = requests.get(url, headers = headers)
    nets = res.json()
    return nets['networks']

def create_fip(ext_net, token):
    url = "http://%(manage_ip)s:9696/v2.0/floatingips.json" % {'manage_ip': manage_ip}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    params = {"floatingip": {"floating_network_id": ext_net['id']}}
    data = json.dumps(params)
    res = requests.post(url, data=data, headers = headers)
    fip = res.json()['floatingip']
    return fip

def instance_list(project_name, token):
    project_id = None
    for project in user_map:
        if project_name == project.get('project_name'):
            project_id = project['project_id']
            break
    url = "http://%(manage_ip)s:8774/v2/%(project_id)s/servers/detail" % {'manage_ip': manage_ip, 'project_id': project_id}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    res = requests.get(url, headers = headers)
    instances = res.json()['servers']
    HA_instances = []
    for instance in instances:
        if 'HA' in instance['name']:
            HA_instances.append(instance)
    return HA_instances
        
def associate_fip(instance, fip, token):
    url = "http://%(manage_ip)s:8774/v2/%(project_id)s/servers/%(instance_id)s/action" % {'manage_ip': manage_ip, 'project_id': instance['tenant_id'], 'instance_id': instance['id']}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    params = {"addFloatingIp": {"address": fip['floating_ip_address']}}
    data = json.dumps(params)
    res = requests.post(url, data = data, headers = headers)
    return res.status_code
 
tokens = get_token()
print tokens

vdc = None
token = None

for vdc in tokens.keys():
    token = tokens[vdc][0]['token']
    print "Preparing instance for project %s" % vdc

    nets = net_list(token)
    ext_net = None
    for net in nets:
        if 'ext' in net['name']:
            ext_net = net
            break
    HA_instances = instance_list(vdc, token)
    for instance in HA_instances:
        if instance['status'] == 'ACTIVE':
            fip = create_fip(ext_net, token)
            output = associate_fip(instance, fip, token)
            print output
            
            
        
