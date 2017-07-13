#!/usr/bin/python

import pdb as xuao
import json
import requests
import commands
import time
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

def image_list(token):
    url = "http://%(manage_ip)s:9292/v1/images/detail" % {'manage_ip': manage_ip}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    res = requests.get(url, headers = headers)
    images = res.json()
    return images['images']

def flavor_list(project_name, token):
    project_id = None
    for project in user_map:
        if project_name == project.get('project_name'):
            project_id = project['project_id']
            break
    url = "http://%(manage_ip)s:8774/v2/%(project_id)s/flavors/detail" % {'manage_ip': manage_ip, 'project_id': project_id}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    res = requests.get(url, headers = headers)
    flavors = res.json()
    return flavors['flavors']
    
def get_nodes(tokens):
    url = "http://%(manage_ip)s:8774/v2/%(project_id)s/os-services" % {'manage_ip': manage_ip, 'project_id': project_admin_id}
    for user in tokens['admin']:
        if user['user_name'] == 'admin':
            token = user['token']
            break
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    res = requests.get(url, headers = headers)
    services = res.json()
    nodes = []
    for service in services['services']:
        if service['binary'] == 'nova-compute' and service['status'] == 'enabled' and service['state'] == 'up':
            node = service['zone'] + ':' + service['host']
            nodes.append(node)
    return nodes

def create_instance(project_name, user_name, node_name, network, image, flavor, token, type='rec'):
    project_id = None
    for project in user_map:
        if project_name == project.get('project_name'):
            project_id = project['project_id']
            break
    url = "http://%(manage_ip)s:8774/v2/%(project_id)s/os-volumes_boot" % {'manage_ip': manage_ip, 'project_id': project_id}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    instance_name = project_name + '_' + user_name + '_' + node_name.split(':')[1] + '_' + network['name'] + '_' + image['name'] + '_' + type
    vol_size = images[0]['properties']['vol_size']
    flavor_id = flavor.get('id', "11")
    params = {"server": {"name": instance_name, "imageRef": image['id'], "availability_zone": node_name, "key_name": "nova-key", "block_device_mapping_v2": [{"source_type": "image", "uuid": image['id'], "boot_index": "0", "volume_size": vol_size, "destination_type": "volume"}], "flavorRef": flavor_id, "max_count": 1, "min_count": 1, "networks": [{"uuid": network['id']}]}}
    data = json.dumps(params)
    res = requests.post(url, data = data, headers = headers)
    result = res.json()
    return result
 
tokens = get_token()
print tokens

vdc = None
token = None

print "Getting nodes"
nodes = get_nodes(tokens)
print nodes

for vdc in tokens.keys():
    token = tokens[vdc][0]['token']

    nets = net_list(token)
    sel_net = None
    ext_net = None
    for net in nets:
        if net['name'] == (vdc + '-net'):
            sel_net = net
        if 'ext' in net['name']:
            ext_net = net


    images = image_list(token)
    sel_images = []
    for image in images:
        if (image['name'] == 'CentOS-HA'):
            sel_images.append(image)

    flavors = flavor_list(vdc, token)
    sel_flavor = None
    for flavor in flavors:
        if flavor['name'] == '1C2G0G':
            sel_flavor = flavor
            break 

    for user in tokens[vdc]:
        print "Preparing instance for project %s, user %s" % (vdc, user['user_name'])
        token = user['token']
        for node in nodes:
            for image in sel_images:
                print "Creating %s %s %s %s" % (vdc, user['user_name'], node, image['name'])
                output = create_instance(vdc, user['user_name'], node, sel_net, image, sel_flavor, token)
                print output
            time.sleep(20)
