import openstack
from openstack.config import loader
from openstack import utils


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
  
print (read_identity())

def create_connection():
    return openstack.connect(
    auth=read_identity(),
    region_name = "RegionOne",
    interface =  "public",
    identity_api_version='3'
    )
print (dict(
      auth_url='http://vlad-mgmt.ncsa.illinois.edu:5000/v3/',
      username = "rc5",
      password = '8473ccead8bb92673865',
      project_id =  '4b6b08facc2e45c896ebb00e69e4774e',
      project_name = "DL",
      user_domain_name = "Default"))
conn = create_connection() 
much = conn.create_server('testserver4',
                    image='d8a9f636-5776-4c8f-94f0-ab0a19113762',
                    flavor = 'm1.small',
                    key_name = 'ruiyanghp',
                    userdata = '#!/bin/sh\n' 
                          +'apt-get update \n ' +
                          'echo heyhye'+
                          'apt-get install -y python3-pip \n'+
                          'pip3 install torch \n' +
                          'pip3 install torchvision\n'
                          'pip3 install scipy'
                    )
# print(conn.available_floating_ip())
