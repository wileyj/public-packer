# import boto3
# from datetime import datetime
# aws ec2 describe-images --filter '[{ "Name":"name", "Values":["CentOS*7*64*"]}]'
from get_images import get_images
import args


# Amazon Linux ami
amazon_owner_id = '137112412989'
amazon_owner_alias = 'amazon'
amazon_ami = 'amzn-ami-hvm*'
amazon_ami_pv = 'amzn-ami-pv*'
amazon_user = "ec2-user"

# Centos
centos_owner_id = '679593333241'
centos_owner_alias = ''
centos_ami = 'CentOS*7*64*'
centos_user = "centos"

# ubuntu ami
ubuntu_owner_id = '099720109477'
ubuntu_owner_alias = ''
ubuntu_ami = 'ubuntu*16*amd64*server*'
ubuntu_user = "ubuntu"

# coreos ami
coreos_owner_id = '595879546273'
coreos_owner_alias = ''
coreos_ami = 'CoreOS*stable*hvm'
coreos_user = "core"

# atomic ami
atomic_owner_id = '410186602215'
atomic_owner_alias = ''
atomic_ami = 'CentOS*Atomic*Host*x86_64*HVM*'
atomic_user = "centos"


# image = get_images().find_ami(centos_ami, '679593333241', '', 'ec2')
image = get_images().find_ami(centos_ami, centos_owner_id, '', 'ec2')
print "Image: %s" % (image)
print get_images().return_ami('')
print args.Args()
