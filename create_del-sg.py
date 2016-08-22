#!/usr/bin/python
import jinja2
import os
import boto3
from boto3.session import Session

session = Session()
ec2 = session.resource('ec2', region_name="us-east-1")
client = boto3.client('ec2', region_name="us-east-1")


def del_sec_group(sg):
    """ Delete Ephemeral Security Group """
    print "Deleting SG: %s" % (sg)
    client.delete_security_group(
        GroupId=sg
    )
    return 0

def add_sec_group(sg):
    """ Add Ephemeral Security Group """
    print "Adding Temporary Security Group %s" % (sg)
    existing_id = get_sg_id(sg)
    if existing_id != "":
        del_sec_group(existing_id)
    client.create_security_group(
        GroupName=sg,
        Description=sg,
        VpcId=vpc
    )
    return 0

def add_sg_ingress(sg):
    """ Add the Temp SG """
    print "Adding Ingress Rule to %s" % (sg)
    client.authorize_security_group_ingress(
        GroupId=sg,
        IpProtocol="tcp",
        CidrIp="0.0.0.0/0",
        FromPort=22,
        ToPort=22
    )
    return 0

def get_sg_id(sg):
    """ Retrieve the Ephemeral SG """
    security_group_id = ""
    print "Looking for id of SG %s" % (sg)
    group = ec2.security_groups.filter(
        Filters=[{
            'Name': 'group-name',
            'Values': [sg]
        }]
    )
    for item in group:
        print "Found SG id: %s" % (item.id)
        security_group_id = item.id
    return security_group_id

#sg_string = "Temp-Packer-SSH-Ephemeral_ssc_amzn-singledisk_packer-beanstalk"
sg_string = "Temp-Packer-SSH-Ephemeral_ssc_amzn-singledisk_packer-base"

print get_sg_id(sg_string)

