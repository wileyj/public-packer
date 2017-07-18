
class delete_images(object):
    def __init__(self, client):
        self.ec2_client = client

    def find_ami(self, ami, owner_id, owner_alias, exec_type):
        '''
            replaces function "get_ec2_images"
        '''

def delete_image(images):
    """ docstring """
    if len(images) > 0:
        logging.info("Renaming Image before deregistering...")
        logging.info("Deregistering Image %s" % (images['Images'][0]['ImageId']))
        ec2_client.deregister_image(ImageId=images['Images'][0]['ImageId'])
         #
         #  https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Waiter.ImageExists
         #
    #     # not working, to implement later
    #     # waiter = client.get_waiter('image_available')
    #     # waiter.wait(ImageIds=[images['Images'][0]['ImageId']])
    #     # logging.info("Image %s is Deregistered " % (images['Images'][0]['ImageId']))
    return 0

    # exit(0)
    # return image_id
