from datetime import datetime
import logging
from logger import Logger

logger = Logger()


class ec2(object):
    def __init__(self, client):
        self.client = client

    def get_image(self, ami, owner_id, owner_alias, exec_type):
        '''
            Method to find details about an image from provided filters of name, owner and owner id
        '''
        logging.warn("filtering ami based on: ")
        logging.warn("\t ami: %s" % (ami))
        logging.warn("\t owner_id: %s" % (owner_id))
        logging.warn("\t owner_alias: %s" % (owner_alias))
        logging.warn("\t exec_type: %s" % (exec_type))
        logging.warn("")
        if exec_type != "docker":
            if owner_alias:
                images = self.client.describe_images(
                    Filters=[
                        {'Name': 'root-device-type', 'Values': ['ebs']},
                        {'Name': 'name', 'Values': [ami]},
                        {'Name': 'owner-alias', 'Values': [owner_alias]},
                        {'Name': 'virtualization-type', 'Values': ['hvm']},
                        {'Name': 'owner-id', 'Values': [owner_id]}
                    ]
                )
            else:
                images = self.client.describe_images(
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
            logging.warn("Skipping get_ec2_images since we're doing %s" % (exec_type))
            return False

    def find_image(self, image_name):
        '''
            Method to retrieve the image ID from a supplied name
        '''
        logging.critical("Checking for existing image named: %s" % (image_name))
        try:
            images = self.client.describe_images(Filters=[{'Name': 'name', 'Values': [image_name]}])
            if len(images['Images']) > 0:
                logging.critical("Found images: %s" % (images))
                return images
            else:
                logging.critical("No existing images found. Continuing")
                return 100
        except:
            pass

    def copy_image(self, image, region):
        '''
            Method to copy created image to new region
        '''
        logging.critical("Copying Image (%s) to Region: %s" % (image, region))
        return True

    def delete_image(self, images, dry_run):
        '''
            Deletes an image from provided image id
        '''
        try:
            if len(images) > 0:
                logging.error("Renaming Image before deregistering...")
                logging.critical("Deregistering Image %s" % (images['Images'][0]['ImageId']))
                if not dry_run:
                    self.client.deregister_image(ImageId=images['Images'][0]['ImageId'])
                # implement this soon
                #
                # https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Waiter.ImageExists
                # not working, to implement later
                # waiter = client.get_waiter('image_available')
                # waiter.wait(ImageIds=[images['Images'][0]['ImageId']])
                # logging.info("Image %s is Deregistered " % (images['Images'][0]['ImageId']))
            return 0
        except:
            return -1
