#!/usr/bin/env python

# ec2:
# os:
#     centos
#     amazon
#     atomic
#     coreos
#     ubuntu
# disk:
#     single
#     multi
# role:
#     base
# python packer-new.py --type ec2 --tag latest --region us-west-2 --public-ip True --application ops --role base --env dev --os centos --vpc-id vpc-b08b6fd6 --subnet-id subnet-11b4674a --instance-type t2.micro --virt hvm --prefix packer --disk single --dry-run --clean
# python packer-new.py --type ec2 --tag latest --region us-west-2 --public-ip True --application ops --role base --env dev --os centos --vpc-id vpc-b08b6fd6 --subnet-id subnet-11b4674a --instance-type t2.micro --virt hvm --prefix packer --disk multi  --dry-run --clean
# python packer-new.py --type ec2 --tag latest --region us-west-2 --public-ip True --application ops --role base --env dev --os amazon --vpc-id vpc-b08b6fd6 --subnet-id subnet-11b4674a --instance-type t2.micro --virt hvm --prefix packer --disk single --dry-run --clean
# python packer-new.py --type ec2 --tag latest --region us-west-2 --public-ip True --application ops --role base --env dev --os amazon --vpc-id vpc-b08b6fd6 --subnet-id subnet-11b4674a --instance-type t2.micro --virt hvm --prefix packer --disk multi  --dry-run --clean
# python packer-new.py --type ec2 --tag latest --region us-west-2 --public-ip True --application ops --role base --env dev --os atomic --vpc-id vpc-b08b6fd6 --subnet-id subnet-11b4674a --instance-type t2.micro --virt hvm --prefix packer --disk single --dry-run --clean
# python packer-new.py --type ec2 --tag latest --region us-west-2 --public-ip True --application ops --role base --env dev --os atomic --vpc-id vpc-b08b6fd6 --subnet-id subnet-11b4674a --instance-type t2.micro --virt hvm --prefix packer --disk multi  --dry-run --clean
# python packer-new.py --type ec2 --tag latest --region us-west-2 --public-ip True --application ops --role base --env dev --os coreos --vpc-id vpc-b08b6fd6 --subnet-id subnet-11b4674a --instance-type t2.micro --virt hvm --prefix packer --disk single --dry-run --clean
# python packer-new.py --type ec2 --tag latest --region us-west-2 --public-ip True --application ops --role base --env dev --os coreos --vpc-id vpc-b08b6fd6 --subnet-id subnet-11b4674a --instance-type t2.micro --virt hvm --prefix packer --disk multi  --dry-run --clean

# docker
# image: centos:7
# application:
#    ops
#    shared
#    platform
# os:
#    centos
# role
#    base
#    web
#    redis
#    varnish
# template:
#    base
# python packer-new.py  --type docker --tag centos --image centos:7 --env dev --os centos --template base --repo wileyj/ops --region us-west-2 --application ops --role base --clean --dry-run

import argparse
import logging
from datetime import datetime
import time
import os
import sys
import jinja2
import boto3

epoch = time.time()
user = os.getlogin()
secs = 10
elapsed = 0
timeout = 300
timestamp = datetime.utcnow().isoformat()
today = datetime.now()
current_time = int(round(time.time()))
short_date = str('{:04d}'.format(today.year))+str('{:02d}'.format(today.month))+str('{:02d}'.format(today.day))
short_hour = str('{:04d}'.format(today.year))+str('{:02d}'.format(today.month))+str('{:02d}'.format(today.day))+"_"+str(current_time)

current_time = int(round(time.time()))
full_day = 86400
today = datetime.now()
short_date = str('{:04d}'.format(today.year))+str('{:02d}'.format(today.month))+str('{:02d}'.format(today.day))
short_hour = str('{:04d}'.format(today.year))+str('{:02d}'.format(today.month))+str('{:02d}'.format(today.day))+"_"+str(current_time)
sumo_access_id = "<sumo_access_id>"
sumo_access_key = "<sumo_access_key>"
quay_auth = "<quay_auth_key>"
quay_email = ""
quay_url = "https://quay.io"
docker_auth ="<docker_auth_key>"
docker_email ="<docker_auth_email>"
docker_url = "https://index.docker.io/v1/"
etcd_cluster = "http://local.com:2380"
log_disk = "xvdf"
log_mount = "/srv/log"
inline = []
enhanced_networking = ""
extra_script = ""
packer_template = "/var/tmp/packer-"+str(epoch)+".json"
userdata_dest = "/var/tmp/user_data-"+str(epoch)
salt_grains_template = "/var/tmp/salt_grains-"+str(epoch)
shell_dest = "/var/tmp/shell-"+str(epoch)+".sh"
createuser_dest = "/var/tmp/create_users-"+str(epoch)+".py"
services_script = "/var/tmp/services-"+str(epoch)+".sh"
packer_binary = "~/go-workspace/bin/packer"
curl_binary = "/usr/bin/curl"
inline = []

userdata_source = "user_data.jinja2"
default_packages = [
    "sudo",
    "git",
    "curl",
    "telnet",
    "nmap",
    "lsof",
    "strace",
    "tcpdump",
    "traceroute",
    "rsync"
]

services_packages = [
    "runit",
    "cronie"
]

default_services = [
    "runit",
    "crond"
]

default_modules = [
    "boto3",
    "awscli",
    "botocore",
    "python-dateutil",
    "jmespath",
    "pyasn1",
    "colorama",
    "s3transfer",
    "request",
    "rsa"
]

exclude_list = [
    "fipscheck*"
]

# Amazon Linux ami
amazon_owner_id='137112412989'
amazon_owner_alias='amazon'
amazon_hvm_minimal = 'amzn-ami-minimal-hvm*'
amazon_pv_minimal = 'amzn-ami-minimal-pv*'
amazon_user = "ec2-user"

# Centos
centos_owner_id = '679593333241'
centos_owner_alias = ''
centos_hvm_minimal ='CentOS*7*64*'
centos_user="centos"

# ubuntu ami
ubuntu_owner_id = '099720109477'
ubuntu_owner_alias = ''
ubuntu_hvm_minimal ='ubuntu*16*amd64*server*'
ubuntu_user = "ubuntu"

# coreos ami
coreos_owner_id = '595879546273'
coreos_owner_alias = ''
coreos_hvm_minimal ='CoreOS*stable*hvm'
coreos_user = "core"

# atomic ami
atomic_owner_id =  '410186602215'
atomic_owner_alias = ''
atomic_hvm_minimal = 'CentOS*Atomic*Host*x86_64*HVM*'
atomic_user = "centos"

repo_address = "yumrepo.moil.io" # if not in main VPC, use the local address of xxxx
repo_dns = "yumrepo.moil.io"

def check_and_delete_file(filename):
    """ docstring """
    if os.path.isfile(filename) and os.access(filename, os.R_OK):
        logging.error("Found Existing file: %s" % (filename))
        logging.error("Deleting: %s" % (filename))
        os.remove(filename)
    return 0

def find_image(image_name):
    """ docstring """
    images = ec2_client.describe_images(Filters=[{'Name': 'name', 'Values': [image_name]}])
    if len(images['Images']) > 0:
        return images
    else:
        return 100

def get_ec2_images(ami, owner_id, owner_alias, exec_type):
    """ docstring """
    print "filtering ami based on :"
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
                    {'Name': 'virtualization-type', 'Values': [args.virt]},
                    {'Name': 'owner-id', 'Values': [owner_id]}
                ]
            )
        else:
            images = ec2_client.describe_images(
                Filters=[
                    {'Name': 'root-device-type', 'Values': ['ebs']},
                    {'Name': 'name', 'Values': [ami]},
                    {'Name': 'virtualization-type', 'Values': [args.virt]},
                    {'Name': 'owner-id', 'Values': [owner_id]}
                ]
            )
        image_list = []
        for image in images['Images']:
            # print "image: %s" % (image)
            image_list.append(image)
            #   image_list.sort( key=lambda x:datetime.datetime.strptime(x['CreationDate'], '%Y-%m-%dT%H:%M:%S.000Z'))
            image_list.sort( key=lambda x:datetime.strptime(x['CreationDate'], '%Y-%m-%dT%H:%M:%S.000Z'))
        image_id = image_list[len(image_list)-1]['ImageId']
        return image_id
    else:
        print "Skipping get_ec2_images since we're doing %s" % (exec_type)
        return False

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

def write_userdata_template(userdata_template_source, userdata_template_dest):
    """ docstring """
    check_and_delete_file(userdata_template_dest)
    result = ""
    logging.info("[ EXEC  ] - Writing UserData Template %s" % (userdata_template_dest))
    template = env.get_template(userdata_template_source+".jinja2")
    result = template.render()
    os.open(userdata_template_dest, os.O_CREAT)
    fd = os.open(userdata_template_dest, os.O_RDWR)
    os.write(fd, result)
    file_stat = os.stat(userdata_template_dest)
    file_size = file_stat.st_size
    logging.info("\tCreated userdata file %s ( %s )" % (userdata_template_dest, file_size))
    os.close(fd)
    return 0

def write_template(template_values, template_source, template_dest, template_path, template_type):
    """ docstring """
    check_and_delete_file(template_dest)
    result = ""
    logging.error("[ EXEC  ] - Writing Template %s: %s:" % (template_type, template_source))
    logging.error("\tLooking for template (%s%s) to write %s" % (template_path, template_source, template_dest))
    print "\ttemplate_values: %s" % (template_values)
    print "\ttemplate_source: %s" % (template_source)
    print "\ttemplate_dest: %s" % (template_dest)
    print "\ttemplate_path: %s" % (template_path)
    packer_env = jinja2.Environment(loader=jinja2.FileSystemLoader([template_path]))
    template = packer_env.get_template(template_source)
    result = template.render(template_values)
    os.open(template_dest, os.O_CREAT)
    fd = os.open(template_dest, os.O_RDWR)
    os.write(fd, result)
    file_stat = os.stat(template_dest)
    file_size = file_stat.st_size
    logging.error("\tCreated Packer Template: %s ( %s )" % (template_dest, file_size))
    os.close(fd)
    return 0

def write_services_template(template_values, template_source, template_dest, template_path):
    """ docstring """
    check_and_delete_file(template_dest)
    result = ""
    print "[ EXEC  ] - Writing Services Template %s" % (template_source)
    print "looking for %s%s to write %s" % (template_path, template_source, template_dest)
    jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader([template_path]))
    template = jinja2_env.get_template(template_source)
    result = template.render(template_values)
    with open(template_dest, 'w') as output:
    # os.open(template_dest, os.O_CREAT)
    # fd = os.open(template_dest, os.O_RDWR)
    # os.write(fd, result)
        output.write(result)
        print "\t Adding default_services to %s" % (template_dest)
        for service in default_services:
            filename = services_template_path+service+".service"
            print "\t  Read filename: %s" % (filename)
            with open(filename, 'r') as f:
                for line in f:
                    # os.write(fd, f)
                    output.write(line)
                f.closed
    output.closed
    file_stat = os.stat(template_dest)
    file_size = file_stat.st_size
    print "\tCreated Services Script: %s ( %s )" % (template_dest, file_size)
    # os.close(fd)
    return 0

def launch_packer(launch_binary, launch_template):
    """ docstring """
    logging.warning("\tLaunching: %s" % (launch_binary))
    logging.warning("\tUsing Template: %s" % (launch_template))
    try:
        os.system(launch_binary + ' build ' + launch_template)
    except:
        logging.exception("Packer exception occurred")
    logging.error("Removing Packer template: %s" %(packer_template))
    os.remove(packer_template)
    logging.error("Removing Shell template: %s" % (shell_dest))
    os.remove(shell_dest)
    logging.error("Removing Salt Grains template: %s" % (shell_dest))
    os.remove(salt_grains_template)
    return 0


class VAction(argparse.Action):
    """ docstring """
    def __call__(self, argparser, cmdargs, values, option_string=None):
        if values is None:
            values = '1'
        try:
            values = int(values)
        except ValueError:
            values = values.count('v') + 1
        setattr(cmdargs, self.dest, values)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--type',
        default="",
        required=True,
        choices=[
            "docker",
            "ec2"
        ],
        help="Container Type [default 'base': shouldn't be changed ]"
    )
    parser.add_argument(
        '--region',
        required=True,
        choices=[
            "us-east-1",
            "us-west-1",
            "us-west-2"
        ],
        default="us-west-2",
        help="AWS Region ( Default: us-west-2 )"
    )
    parser.add_argument(
        '--iam-profile',
        nargs='?',
        metavar='',
        default="MOIL.Base",
        help="IAM Role"
    )
    parser.add_argument(
        '--public-ip',
        choices=[
            "True",
            "False"
        ],
        default="False",
        help="For ec2 builds, associates a public IP with the ec2 host"
    )
    parser.add_argument(
        '--release',
        nargs='?',
        metavar='',
        default="latest",
        help="Release Tag ( default: latest )"
    )
    parser.add_argument(
        '--instance-type',
        nargs='?',
        metavar='',
        default="t2.micro",
        choices=[
            "t2.micro",
            "t2.medium",
            "t1.micro",
            "t1.medium",
            "m3.medium",
            "m4.large"
        ],
        help="Instance type ( Default: t2.micro )"
    )
    parser.add_argument(
        '--ssh-user',
        nargs='?',
        metavar='',
        default="",
        help="EC2 SSH User ( Default: ec2-user )"
    )
    parser.add_argument(
        '--vpc-id',
        nargs='?',
        metavar='',
        help="VPC ID"
    )
    parser.add_argument(
        '--subnet-id',
        nargs='?',
        metavar='',
        help="Subnet ID"
    )
    parser.add_argument(
        '--prefix',
        nargs='?',
        metavar='',
        default="",
        help="AMI Name Prefix ( required )"
    )
    parser.add_argument(
        '--os',
        choices=[
            "centos",
            "ubuntu",
            "debian",
            "amazon",
            "coreos",
            "atomic",
            "Centos",
            "Ubuntu",
            "Debian",
            "Amazon",
            "CoreOS",
            "Atomic"
        ],
        default="ubuntu",
        help="Container OS Type [ ubuntu, centos, amazon, etc ]"
    )
    parser.add_argument(
        '--script',
        default="",
        nargs='?',
        help="Additional script to execute ( absolute path is required )"
    )
    parser.add_argument(
        '--script-args',
        default="",
        nargs='?',
        help="Additional script args for --script ( surrounded by single quotes )"
    )
    parser.add_argument(
        '--disk',
        nargs='?',
        metavar='',
        default="base",
        help="EC2 Disk Config[ singledisk, multidisk ] ( Default: singledisk )"
    )
    parser.add_argument(
        '--virt',
        nargs='?',
        metavar='',
        default="hvm",
        choices=[
            "hvm",
            "pv"
        ],
        help="Host Virtualization Type (hvm, pv, docker)"
    )
    parser.add_argument(
        '--user_data_file',
        nargs='?',
        metavar='',
        default="",
        help="UserData File ( Default: NULL )"
    )
    parser.add_argument(
        '--platform',
        nargs='?',
        metavar='',
        default="base",
        choices=[
            "base",
            "admin"
        ],
        help="Platform of the build [ base, admin ]"
    )
    parser.add_argument(
        '--tag',
        default="",
        required=True,
        help="Container Tag [ latest, 0.0.1, etc ] (required)"
    )
    parser.add_argument(
        '--image',
        default="",
        help="Container image to use  (required)"
    )
    parser.add_argument(
        '--env',
        choices=[
            "dev",
            "development"
            "staging",
            "stage",
            "qa",
            "QA",
            "prod",
            "production"
        ],
        default="dev",
        required=True,
        help="Env of the build [ dev, staging, prod, etc ]"
    )
    parser.add_argument(
        '--application',
        default="",
        # required=True,
        help="App to run on container  (required if type is docker)"
    )
    parser.add_argument(
        '--role',
        default="",
        required=True,
        help="Application Role [ web, bg, www, etc ]  (required if type is docker)"
    )
    parser.add_argument(
        '--template',
        default="base",
        help="Template to use [default: base]"
    )
    parser.add_argument(
        '--repo',
        default="local/base",
        help="Repo of container: eg. name/base"
    )
    parser.add_argument(
        '-v',
        nargs='?',
        action=VAction,
        dest='verbose'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Don't run packer at script conclusion"
    )
    parser.add_argument(
        '--push',
        action='store_true',
        help="Push to dockerhub"
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help="clean all templates from /var/tmp"
    )
    args = parser.parse_args()
    if args.verbose == 4:
        log_format = '%(lineno)-4s %(levelno)-4s %(asctime)-15s  %(message)-4s'
        logging.basicConfig(level=logging.DEBUG, format=log_format)
        os.environ["PACKER_LOG"] = "debug"
    elif args.verbose == 3:
        log_format = '%(lineno)-4s %(levelno)-4s %(message)-4s'
        logging.basicConfig(level=logging.INFO, format=log_format)
        os.environ["PACKER_LOG"] = "info"
    elif args.verbose == 2:
        log_format = '%(lineno)-4s %(levelno)-4s %(message)-4s'
        logging.basicConfig(level=logging.WARNING, format=log_format)
        os.environ["PACKER_LOG"] = "warning"
    else:
        log_format = '%(message)-4s'
        logging.basicConfig(level=logging.ERROR, format=log_format)
        os.environ["PACKER_LOG"] = "error"
    if args.tag:
        args.tag = args.role+"."+args.tag
    else:
        args.tag = args.role
    # convert args.type to lc
    args.type.lower()
    args.prefix_platform = ""
    args.prefix_app = ""
    packer_template_path = "templates/"+args.type+"/"
    salt_template_path = "templates/salt/"
    scripts_template_path = "templates/scripts/"
    os_template_path = "templates/userdata/"
    services_template_path = "templates/runit_services/"
    cwd = os.getcwd()
    env = jinja2.Environment(loader=jinja2.FileSystemLoader([cwd+"/templates"]))
    bootstrap_cmd   = "curl -L https://bootstrap.saltstack.com -o bootstrap_salt.sh && sh bootstrap_salt.sh -d -M -N -X && echo 'file_client: local' > /etc/salt/minion"
    bootstrap_run   = "salt-call --local  saltutil.sync_grains && salt-call --local  state.highstate"
    bootstrap = bootstrap_cmd+" && "+bootstrap_run
    salt_state_tree = cwd+"/salt/srv/salt"
    salt_pillar_root = cwd+"/salt/srv/pillar"
    bootstrap_args = "-d -M -N -X -q -Z -c /tmp"
    errors = []
    repo_address = "yumrepo.moil.io" # if not in main VPC, use the local address of xxxx
    repo_dns = "yumrepo.moil.io"
    user = os.getlogin()
    ec2_client = boto3.client('ec2', region_name=args.region)
    if args.platform:
        args.prefix_platform = "_"+args.platform
    if args.user_data_file:
        userdata_source = args.user_data_file
    # switch for now, we only want to support ec2, base, docker templates
    if args.type != "base" and args.type != "ec2" and args.type != "docker":
        args.type = "ec2"
    if args.type == "docker":
        args.prefix = args.repo+args.prefix_app
        container_name = args.repo+args.prefix_platform+args.prefix_app+args.tag
        template_name = args.template
        default_packages = []
        #check for required args. only these matter
        if not args.tag or not args.image or not args.application or not args.role or not args.env:
            print "Missing Docker Args...exit(-4)"
            print "\ttag: %s" % (args.tag)
            print "\timage: %s" % (args.image)
            print "\tapplication: %s" % (args.application)
            print "\trole: %s" % (args.role)
            print "\tenv: %s" % (args.env)
            sys.exit(-4)
    if args.type == "ec2":
        template_name = args.role+"_"+args.disk
        args.prefix = "wileyj."+args.os+"_"+args.role+"."+args.type+"_"+args.virt+"_"+args.disk+"."+args.prefix.replace(" ", "-")+"_"+short_date

        if not args.prefix:
            logging.info("Image Prefix is required")
            parser.print_help()
            exit(-1)
        if not args.os or not args.vpc_id or not args.subnet_id or not args.instance_type or not args.virt or not args.prefix or not args.disk or not args.env or not args.type or not args.region or not args.tag or not args.role:
            print "Missing EC2 Args...exit(-4)"
            print "\tos: %s" % (args.os)
            print "\tvpc_id: %s" % (args.vpc_id)
            print "\tsubnet_id: %s" % (args.subnet_id)
            print "\tinstance_type: %s" % (args.instance_type)
            print "\tvirt: %s" % (args.virt)
            print "\tprefix: %s" % (args.prefix)
            print "\tdisk: %s" % (args.disk)
            print "\tenv: %s" % (args.env)
            print "\ttype: %s" % (args.type)
            print "\tregion: %s" % (args.region)
            print "\ttag: %s" % (args.tag)
            print "\trole: %s" % (args.role)
            sys.exit(-4)
        else:
            logging.error("args.subnet_id: %s" % (args.subnet_id))
            logging.error("args.vpc_id: %s" % (args.vpc_id))
            if not args.subnet_id or not args.vpc_id:
                logging.error("\tsubnet and vpc id's are not defined....retrieving from api")
                logging.error("\tsubnet_id not defined, looking at metadata of calling host")
                i = os.popen(curl_binary+" -s http://169.254.169.254/latest/dynamic/instance-identity/document |/bin/grep instanceId | awk -F\\\" '{print $4}'")
                instance_id = i.read().rstrip()
                instances = ec2_client.describe_instances(
                    Filters=[{
                        'Name': 'instance-id',
                        'Values': [instance_id]
                    }]
                )['Reservations']
                for instance in instances:
                    args.vpc_id = instance['Instances'][0]['VpcId']
                    args.subnet_id = instance['Instances'][0]['NetworkInterfaces'][0]['SubnetId']
                    logging.error("Using retrieved value (vpc_id): %s" %(args.vpc_id))
                    logging.error("Using retrieved value (subnet_id): %s" %(args.subnet_id))
            logging.error("Using defined value (vpc): %s " %(args.vpc_id))
            logging.error("Using defined value (subnet): %s" %(args.subnet_id))


            if not args.region:
                logging.info("\tregion not defined, looking at metadata of calling host")
                r = os.popen(curl_binary+" -s http://169.254.169.254/latest/dynamic/instance-identity/document |/bin/grep region | awk -F\\\" '{print $4}'")
                args.region = r.read().rstrip()
            logging.error("Using defined value (region): %s" % (args.region))
            logging.error("Using defined value (clean): %s" % (args.clean))


    if args.clean:
        try:
            os.system('rm /var/tmp/*[0-9]*')
        except:
            logging.exception("Packer exception occurred")
    ssh_user = args.ssh_user
    args.os = args.os.lower()
    if args.os == "amazon":
        owner_id = amazon_owner_id
        owner_alias = amazon_owner_alias
        default_packages.append("python27-pip")
        default_packages.append("aws-apitools-common")
        default_packages.append("aws-cli")
        default_modules.append("salt")
        if args.virt != "pv":
            logging.error("Using Amazon OS %s" % (args.os))
            ami = amazon_hvm_minimal
        else:
            ami = amazon_pv_minimal
        if not args.ssh_user:
            ssh_user = amazon_user
    elif args.os == "ubuntu" or args.os == "debian":
        owner_id = ubuntu_owner_id
        owner_alias = ubuntu_owner_alias
        default_packages.append("vim openssh-client openssh-server python-pip salt-minion")
        if args.virt != "pv":
            logging.error("Using Ubuntu OS %s" % (args.os))
            ami = ubuntu_hvm_minimal
        else:
            logging.error("PV not allowed for Ubuntu")
            exit(3)
        if not args.ssh_user:
            ssh_user = ubuntu_user
    elif args.os == "coreos":
        owner_id = coreos_owner_id
        owner_alias = coreos_owner_alias
        if args.virt != "pv":
            logging.error("Using coreos OS %s" % (args.os))
            ami = coreos_hvm_minimal
        else:
            logging.error("PV not allowed for Coreos")
            exit(3)
        if not args.ssh_user:
            ssh_user = coreos_user
    elif args.os == "centos":
        owner_id = centos_owner_id
        owner_alias = centos_owner_alias
        default_modules.remove("boto3")
        default_modules.remove("awscli")
        default_modules.remove("botocore")
        default_packages.append("python-pip python-setuptools python-boto3 python-botocore salt-minion")
        if args.type != "docker":
            default_packages.append("vim-enhanced openssh openssh-clients openssh-server")
        #default_packages.append("python3 python3-pip python3-setuptools python3-boto3 python3-botocore")
        if args.virt != "pv":
            logging.error("Using centos OS %s" % (args.os))
            ami = centos_hvm_minimal
        else:
            logging.error("PV not allowed for Centos")
            exit(3)
        if not args.ssh_user:
            ssh_user = centos_user
    elif args.os == "atomic":
        owner_id = atomic_owner_id
        owner_alias = atomic_owner_alias
        default_modules.remove("boto3")
        default_modules.remove("awscli")
        default_modules.remove("botocore")
        default_packages.append("python-pip python-setuptools python-boto3 python-botocore")
        #default_packages.append("python3 python3-pip python3-setuptools python3-boto3 python3-botocore")
        default_packages.append("salt-minion")
        # default_packages.append("")
        if args.virt != "pv":
            logging.error("Using centos OS %s" % (args.os))
            ami = atomic_hvm_minimal
        else:
            logging.error("PV not allowed for Centos Atomic")
            exit(3)
        if not args.ssh_user:
            ssh_user = atomic_user
    else:
        logging.error("OS not recognized %s" % (args.os))
    print "Using ssh_user: %s" % (ssh_user)
    logging.error("Using defined value (owner_id): %s" % (owner_id))
    logging.error("Using defined value (owner_alias): %s" % (owner_alias))
    logging.error("Using defined value (ami): %s" % (ami))

    if args.type == 'docker' or args.type == 'Docker':
        defined_type = 'Docker'
    else:
        defined_type = 'EC2'

    packer_values = {
        'source_ami' : get_ec2_images(ami, owner_id, owner_alias, args.type),
        'instance_type': args.instance_type,
        'instance_profile': args.iam_profile,
        'ssh_user': ssh_user,
        'vpc_id': args.vpc_id,
        'subnet_id': args.subnet_id,
        'region': args.region,
        'packages': default_packages,
        'modules': default_modules,
        'user_data_file': userdata_dest,
        'create_user_script': createuser_dest,
        'platform': args.platform,
        'prefix' : args.prefix,
        'tag': args.tag,
        'type': defined_type,
        'release': args.release,
        'os': args.os,
        'application': args.application,
        'role': args.role,
        'environment': args.env,
        'script': shell_dest,
        'services_script': services_script,
        'template': template_name,
        'sudo': "{{ .Path }}",
        'timestamp': timestamp,
        'extra_script': args.script,
        'extra_script_args': args.script_args,
        'inline': inline,
        'cwd': cwd,
        'image': args.image,
        'salt_grains_file': salt_grains_template,
        'default_packages': default_packages,
        'salt_state_tree': salt_state_tree,
        'salt_pillar_root': salt_pillar_root,
        'bootstrap_args': bootstrap_args,
        'docker_push': args.push,
        'public_ip': args.public_ip
    }

    if args.role == 'base':
        args.cleanup = "true"
    else:
        args.cleanup = ""

    salt_grains_values = {
        'platform': args.platform,
        'prefix': args.prefix,
        'instance_profile': args.iam_profile,
        'vpc_id': args.vpc_id,
        'tag': args.tag,
        'release': args.release,
        'environment': args.env,
        'subnet_id': args.subnet_id,
        'cleanup': args.cleanup,
        'application': args.application,
        'role': args.role,
        'type': defined_type,
        'build_type': 'Packer'
    }

    userdata_values = {
        'os': args.os,
        'repo_address': repo_address,
        'exclude_list': exclude_list,
        # 'image_name': image_name,
        # 'image_tag': image_tag
        # 'sumo_access_id': sumo_access_id,
        # 'sumo_access_key': sumo_access_key
    }
    if defined_type == "Docker" or args.os == "atomic" or args.os == "coreos":
        userdata_values['quay_auth'] = quay_auth
        userdata_values['quay_email'] = quay_email
        userdata_values['quay_url'] = quay_url
        userdata_values['docker_auth'] = docker_auth
        userdata_values['docker_email'] = docker_email
        userdata_values['docker_url'] = docker_url
        userdata_values['etcd_cluster'] = etcd_cluster
        userdata_values['log_disk'] = log_disk
        userdata_values['log_mount'] = log_mount

    shell_values = {
        'os': args.os
    }

    services_values = {
        'runit_services': '',
        'services_packages': services_packages
    }

    logging.error("")
    logging.error("Arg Values:")
    logging.error("\tUsing defined value (tag):         %s" %(args.tag))
    logging.error("\tUsing defined value (type):        %s" %(args.type))
    logging.error("\tUsing defined value (defined_type):%s" %(defined_type))
    logging.error("\tUsing defined value (platform):    %s" %(args.platform))
    logging.error("\tUsing defined value (env):         %s" %(args.env))
    logging.error("\tUsing defined value (release):     %s" %(args.release))
    logging.error("\tUsing defined value (os):          %s" %(args.os))
    logging.error("\tUsing defined value (verbose):     %s" %(args.verbose))
    logging.error("\tUsing defined value (dry-run):     %s" %(args.dry_run))
    logging.error("\tUsing defined value (script):      %s" %(args.script))
    logging.error("\tUsing defined value (script_args): %s" %(args.script_args))

    logging.error("Using defined value (iam_profile): %s" %(args.iam_profile))
    logging.error("Using defined value (instance): %s" %(args.instance_type))
    logging.error("Using defined value (ssh_user): %s" %(args.ssh_user))
    logging.error("Using defined value (prefix): %s" %(args.prefix))
    logging.error("Using defined value (type): %s" %(args.type))
    logging.error("Using defined value (disk): %s" %(args.disk))
    logging.error("Using defined value (script): %s" %(args.script))
    logging.error("Using defined value (virt): %s" %(args.virt))
    logging.error("Using defined value (user_data_file): %s" %(args.user_data_file))
    logging.error("Using defined value (platform): %s" % (args.platform))
    logging.error("Defined Instance Type: %s" % (args.instance_type))
    logging.error("Defined Disk: %s" % (args.disk))
    logging.error("Defined Exclude: %s" % (exclude_list))
    logging.error("Defined Prefix: %s" % (args.prefix))
    logging.error("Defined Template Name: %s" % (template_name))

    logging.error("")
    logging.error("Prefix Values:")
    logging.error("\tDefined Prefix:                    %s" % (args.prefix))
    logging.error("\tDefined Prefix_platform:           %s" % (args.prefix_platform))
    logging.error("")
    logging.error("Template Values:")
    logging.error("\tDefined Template Name:             %s" % (template_name))
    logging.error("")
    logging.error("Jinja Values:")
    logging.error("\tPacker Build Values:")
    for val in packer_values:
        print "\t\t%s: %s" % (val, packer_values[val])
    logging.error("")
    logging.error("\tShell Script Values:")
    for val in userdata_values:
        print "\t\t%s: %s" % (val, userdata_values[val])
    logging.error("")
    logging.error("\tSalt Grains Values:")
    for val in salt_grains_values:
        print "\t\t%s: %s" % (val, salt_grains_values[val])
    logging.error("")
    logging.error("")
    if args.type == "ecs":
        write_template('', "create_users.jinja2", createuser_dest, scripts_template_path, "create_users")
    else:
        packer_values['create_user_script'] = ""

    if args.role == "sumologic":
        write_template(services_values, "services.jinja2", services_script, services_template_path, "services")
    else:
        write_template(salt_grains_values, args.type+"_grains.jinja2", salt_grains_template, salt_template_path, "salt grains")
    write_template(packer_values, template_name+".jinja2", packer_template, packer_template_path+args.os+"/", "packer")
    write_template(userdata_values, args.os+".jinja2", userdata_dest, os_template_path, "userdata")
    write_template(shell_values, 'shell.jinja2', shell_dest, scripts_template_path, "shell")
    if not args.dry_run:
        if args.type != "docker":
            if find_image(args.prefix) != 100:
                delete_image(find_image(args.prefix))
                while find_image(args.prefix) != 100:
                    status = find_image(args.prefix)
                    elapsed = elapsed + secs
                    sys.stdout.write("Waiting for ami %s to delete ( Elapsed %s secs)" % (args.prefix, elapsed))
                    sys.stdout.flush()
                    time.sleep(secs)
                    if elapsed == timeout:
                        logging.info("Timeout %s Reached. Exiting..." % (timeout))
                        exit(timeout)

        launch_packer(packer_binary, packer_template)
    exit(0)