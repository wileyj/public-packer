from ec2 import ec2
from aws_conn import conn
from args import Args
from config import Global
import logging
from logger import Logger

args = Args().args
print "Type: %s" % (args.type)
print "Region: %s" % (args.region)
print "verbose: %s" % (args.verbose)
print Global.centos_ami

ec2_client = conn().boto3('ec2', args.region)
image = ec2(ec2_client).get_image(Global.centos_ami, Global.centos_owner_id, '', 'ec2')
print "Image: %s" % (image)
print ec2(ec2_client).find_image('')

logger = Logger()
logging.debug('debug message')
logging.info('info message')
logging.warn('warn message')
logging.error('error message')
logging.critical('critical message')
