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

def create_volume(project_name, instance, size, token):
    project_id = None
    for project in user_map:
        if project_name == project.get('project_name'):
            project_id = project['project_id']
            break
    url = "http://%(manage_ip)s:8776/v1/%(project_id)s/volumes" % {'manage_ip': manage_ip, 'project_id': project_id}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    node_name = instance.get('OS-EXT-SRV-ATTR:host', 'miss')
    instance_name = instance['name']
    volume_name = project_name + '_' + node_name + '_' + instance_name
    params = {"volume": {"status": "creating", "availability_zone": None, "source_volid": None, "display_description": None, "snapshot_id": None, "user_id": None, "size": size, "display_name": volume_name, "imageRef": None, "multiattach": False, "attach_status": "detached", "volume_type": None, "project_id": None, "metadata": {}}}
    data = json.dumps(params)
    res = requests.post(url, data=data, headers = headers)
    volume = res.json()['volume']
    return volume

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
        if 'HA' in instance['name'] and 'rec' in instance['name']:
            HA_instances.append(instance)
    return HA_instances

def volume_list(project_name, token):
    project_id = None
    for project in user_map:
        if project_name == project.get('project_name'):
            project_id = project['project_id']
            break
    url = "http://%(manage_ip)s:8776/v1/%(project_id)s/volumes/detail" % {'manage_ip': manage_ip, 'project_id': project_id}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    res = requests.get(url, headers = headers)
    volumes = res.json()['volumes']
    return volumes
 
def volume_show(project_name, volume, token):
    project_id = None
    for project in user_map:
        if project_name == project.get('project_name'):
            project_id = project['project_id']
            break
    url = "http://%(manage_ip)s:8776/v1/%(project_id)s/volumes/%(volume_id)s" % {'manage_ip': manage_ip, 'project_id': project_id, 'volume_id': volume['id']}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    res = requests.get(url, headers = headers)
    return res.json()['volume']

def attach_volume(instance, volume, token):
    url = "http://%(manage_ip)s:8774/v2/%(project_id)s/servers/%(instance_id)s/os-volume_attachments" % {'manage_ip': manage_ip, 'project_id': instance['tenant_id'], 'instance_id': instance['id']}
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    params = {"volumeAttachment": {"device": None, "disk_bus": None, "volumeId": volume['id']}}
    data = json.dumps(params)
    res = requests.post(url, data = data, headers=headers)
    return res.status_code
 
tokens = get_token()
print tokens

vdc = None
token = None

for vdc in tokens.keys():
    token = tokens[vdc][0]['token']
    print "Preparing instance for project %s" % vdc
    ins_vol = []
    HA_instances = instance_list(vdc, token)
    for instance in HA_instances:
        if instance['status'] == 'ACTIVE':
           size = 20
           volume = create_volume(vdc, instance, size, token)
           while volume_show(vdc, volume, token)['status'] != 'available':
               print "Creating volume for %s" % instance['name']
               time.sleep(2)
           attach_volume(instance, volume, token)
