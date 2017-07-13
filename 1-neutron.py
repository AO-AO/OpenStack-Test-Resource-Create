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

def create_net(project_name, token):
    print "Creating net"
    url = "http://%(manage_ip)s:9696/v2.0/networks.json" % {'manage_ip': manage_ip}
    params = {"network": {"name": project_name + '-net', "admin_state_up": 'true'}}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    data = json.dumps(params)
    res = requests.post(url, data = data, headers = headers)
    result = res.json()
    net = result['network']
    print "Net created"
    return net

def create_subnet(project_name, net, token):
    print "Creating subnet"
    url = "http://%(manage_ip)s:9696/v2.0/subnets.json" % {'manage_ip': manage_ip}
    params = {"subnet": {"network_id": net['id'], "ip_version": 4, "cidr": "192.168.11.0/24", "gateway_ip": "192.168.11.1", "name": project_name + '-subnet'}}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    data = json.dumps(params)
    res = requests.post(url, data = data, headers = headers)
    result = res.json()
    sub_net = result['subnet']
    print "Subnet created"
    return sub_net

def create_router(project_name, token):
    print "Creating router"
    url = "http://%(manage_ip)s:9696/v2.0/routers.json" % {'manage_ip': manage_ip}
    params = {"router": {"name": project_name + '-router', "admin_state_up": 'true'}}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    data = json.dumps(params)
    res = requests.post(url, data = data, headers = headers)
    result = res.json()
    router = result['router']
    print "Router created"
    return router

def router_interface_add(router, subnet, token):
    print "Adding subnet to router"
    url = "http://%(manage_ip)s:9696/v2.0/routers/%(router_id)s/add_router_interface.json" % {'manage_ip': manage_ip, 'router_id': router['id']}
    params = {"subnet_id": subnet['id']}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    data = json.dumps(params)
    res = requests.put(url, data = data, headers = headers)
    print "Subnet added to router"
    return res.status_code

def router_gw_set(router, token):
    """Useless"""
    print "Setting gateway for router %s" % router['name']
    nets = net_list(token)
    ext_net = None
    for net in nets:
        if 'ext' in net['name']:
            ext_net = net
            break
    url = "http://%(manage_ip)s:9696/v2.0/routers/%(router_id)s.json" % {'manage_ip': manage_ip, 'router_id': router['id']}
    params = {"router": {"external_gateway_info": {"network_id": ext_net['id']}}}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    data = json.dumps(params)
    res = requests.put(url, data = data, headers = headers)
    print "Router %s gateway setted" % router['name']
    return res.status_code

def net_list(token):
    url = "http://%(manage_ip)s:9696/v2.0/networks.json" % {'manage_ip': manage_ip}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    res = requests.get(url, headers = headers)
    nets = res.json()
    return nets['networks']
 
tokens = get_token()
print tokens
vdc = None
token = None
for vdc in tokens.keys():
    token = tokens[vdc][0]['token']
    print "Preparing project %s" % vdc
    net = create_net(vdc, token)
    subnet = create_subnet(vdc, net, token)
    router = create_router(vdc, token)
    router_interface_add(router, subnet, token)
    output = router_gw_set(router, token)
    print output
