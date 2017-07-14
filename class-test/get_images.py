from datetime import datetime
from aws_conn import conn
# import boto3

# ec2_client = boto3.client('ec2', region_name='us-west-2')
ec2_client = conn().ec2("us-west-2")


class get_images(object):
    def find_ami(self, ami, owner_id, owner_alias, exec_type):
        """ docstring """
        print "filtering ami based on: "
        print "\t ami: %s" % (ami)
        print "\t owner_id: %s" % (owner_id)
        print "\t owner_alias: %s" % (owner_alias)
        print "\t exec_type: %s" % (exec_type)
        print ""
        if exec_type != "docker":
            if owner_alias:
                images = ec2_client.describe_images(
                    Filters=[
                        {'Name': 'root-device-type', 'Values': ['ebs']},
                        {'Name': 'name', 'Values': [ami]},
                        {'Name': 'owner-alias', 'Values': [owner_alias]},
                        {'Name': 'virtualization-type', 'Values': ['hvm']},
                        {'Name': 'owner-id', 'Values': [owner_id]}
                    ]
                )
            else:
                images = ec2_client.describe_images(
                    Filters=[
                        {'Name': 'root-device-type', 'Values': ['ebs']},
                        {'Name': 'name', 'Values': [ami]},
                        {'Name': 'virtualization-type', 'Values': ['hvm']},
                        {'Name': 'owner-id', 'Values': [owner_id]}
                    ]
                )
            image_list = []
            for image in images['Images']:
                image_list.append(image)
                image_list.sort(
                    key=lambda x: datetime.strptime(
                        x['CreationDate'],
                        '%Y-%m-%dT%H:%M:%S.000Z'
                    ),
                    reverse=True
                )
                image_id = image_list[0]['ImageId']
            return image_id
        else:
            print "Skipping get_ec2_images since we're doing %s" % (exec_type)
            return False

    def return_ami(self, image_name):
        try:
            images = ec2_client.describe_images(Filters=[{'Name': 'name', 'Values': [image_name]}])
            return images
        except:
            pass
