import openstack
from openstack.config import loader
from openstack import utils
import cinderclient as cinder 
import novaclient as nova
import glanceclient as glance
import swiftclient as swift
import time

def read_identity():
  identity = open('identity.txt')
  identity_dict = {}
  while True:
    line = identity.readline()
    if len(line)==0:
      return identity_dict
    else:
      line = line.split(',')
      if len(line)==2:
          identity_dict[line[0].lstrip(' ')]=line[-1].lstrip(' ').replace('\n','')
  
def create_connection():
    return openstack.connect(
    auth=read_identity(),
    region_name = "RegionOne",
    interface =  "public",
    identity_api_version='3'
    )
conn = create_connection()

def create_server(connection):
    much = connection.create_server('testserver4',
                        image='d8a9f636-5776-4c8f-94f0-ab0a19113762',
                        #filename = './userdata',
                        flavor = 'm1.small',
                        key_name = 'ruiyanghp',
                        userdata = '#!/bin/sh\n' 
                              +'apt-get update \n ' +
                              'echo heyhye\n'+
                              'apt-get install -y python3-pip \n'+
                              'apt-get install git\n'+
                              'git clone https://github.com/dylanrchen/openstack_torchmodel /home/ubuntu/openstack_torchmodel \n'+
                              'pip3 install torch \n' +
                              'pip3 install torchvision\n'
                              'pip3 install scipy\n'+
                              'cd /home/ubuntu/openstack_torchmodel\n'+
                              'python3 run.py'
                        )
    ips = connection.available_floating_ip()
    time.sleep(10)
    conn.add_ip_list(much,ips['floating_ip_address'])
    return much,ips['floating_ip_address']

def transfer_local_file(file_name,connection,server):
#     the best way to do this is to create a container using swift, and then upload the data into the 
#     container, But the swift server is currently not installed on the cluster. I guess we can just use git then
      return 


much = create_server(conn)
conn.delete_server('testserver4')

# print(conn.available_floating_ip())
