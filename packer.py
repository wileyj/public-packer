from lib.ec2 import ec2
from lib.aws_conn import conn
from lib.args import Args
from lib.config import Global
import logging
from lib.logger import Logger
from lib.template import Template
from lib.exec_binary import Exec
import os
import sys
import time

if __name__ == "__main__":
    logger = Logger()
    args = Args().args
    ec2_client = conn().boto3('ec2', args.region)
    image = ec2(ec2_client).get_image(Global.centos_ami, Global.centos_owner_id, '', args.type)
    logging.error("Image: %s" % (image))

    args.type.lower()
    args.prefix_platform = ""
    args.prefix_app = ""

    if args.type != "base" and args.type != "ec2" and args.type != "docker":
        args.type = "ec2"
    if args.type == "docker":
        container_name = args.repo + args.prefix_platform + args.prefix_app + args.tag
        print "container_name: %s" % (container_name)
        image_tag = args.os + "." + args.role + "." + args.tag
        # sys.exit(0)
        template_name = args.template
        image_name = args.repo + args.prefix_app
        Global.packer_values['tag'] = image_tag
    if args.type == "ec2":
        template_name = args.role + "_" + args.disk
        image_name = "wileyj." + args.os + "_" + args.role + "." + args.type + "_" + args.virt + "_" + args.disk + "." + args.prefix.replace(" ", "-") + "_" + Global.short_date
    Global.salt_grains_values['prefix'] = image_name
    Global.packer_values['prefix'] = image_name
    if args.clean:
        try:
            os.system('rm /var/tmp/*[0-9]*')
        except OSError as e:
            logging.exception("IO Exception occurred: %s" % (e))
    logging.critical("userdate vaulues: %s" % (Global.userdata_values))
    if args.type == "Docker" or args.os == "atomic" or args.os == "coreos":
        Global.userdata_values['quay_auth'] = Global.quay_auth
        Global.userdata_values['quay_email'] = Global.quay_email
        Global.userdata_values['quay_url'] = Global.quay_url
        Global.userdata_values['docker_auth'] = Global.docker_auth
        Global.userdata_values['docker_email'] = Global.docker_email
        Global.userdata_values['docker_url'] = Global.docker_url
        Global.userdata_values['etcd_cluster'] = Global.etcd_cluster
        Global.userdata_values['log_disk'] = Global.log_disk
        Global.userdata_values['log_mount'] = Global.log_mount

    packer_template_path = "templates/" + args.type + "/"
    salt_template_path = "templates/salt/"
    scripts_template_path = "templates/scripts/"
    os_template_path = "templates/userdata/"
    services_template_path = "templates/runit_services/"

    if args.os == "amazon":
        owner_id = Global.amazon_owner_id
        owner_alias = Global.amazon_owner_alias
        Global.default_packages.append("python27-pip python27-setuptools python27-boto3 python27-botocore python27-pycrypto python27-pyzmq salt27-minion")
        Global.default_packages.append("aws-apitools-common aws-cli zeromq vim-enhanced openssh openssh-clients openssh-server")
        Global.default_modules.append("salt")
        if args.virt != "pv":
            logging.error("Using Amazon OS %s" % (args.os))
            ami = Global.amazon_ami
        else:
            ami = Global.amazon_pv
        if not args.ssh_user:
            args.ssh_user = Global.amazon_user
    elif args.os == "ubuntu" or args.os == "debian":
        Global.owner_id = Global.ubuntu_owner_id
        Global.owner_alias = Global.ubuntu_owner_alias
        Global.default_packages.append("vim openssh-client openssh-server python-pip salt-minion")
        if args.virt != "pv":
            logging.error("Using Ubuntu OS %s" % (args.os))
            ami = Global.ubuntu_ami
        else:
            logging.error("PV not allowed for Ubuntu")
            exit(3)
        if not args.ssh_user:
            args.ssh_user = Global.ubuntu_user
    elif args.os == "coreos":
        Global.owner_id = Global.coreos_owner_id
        Global.owner_alias = Global.coreos_owner_alias
        if args.virt != "pv":
            logging.error("Using coreos OS %s" % (args.os))
            ami = Global.coreos_ami
        else:
            logging.error("PV not allowed for Coreos")
            exit(3)
        if not args.ssh_user:
            args.ssh_user = Global.coreos_user
    elif args.os == "centos":
        Global.owner_id = Global.centos_owner_id
        Global.owner_alias = Global.centos_owner_alias
        Global.default_modules.remove("boto3")
        Global.default_modules.remove("awscli")
        Global.default_modules.remove("botocore")
        Global.default_packages.append("python-pip python-setuptools python-boto3 python-botocore salt-minion")
        if args.type != "docker":
            Global.default_packages.append("vim-enhanced openssh openssh-clients openssh-server")
        if args.virt != "pv":
            logging.error("Using centos OS %s" % (args.os))
            ami = Global.centos_ami
        else:
            logging.error("PV not allowed for Centos")
            exit(3)
        if not args.ssh_user:
            args.ssh_user = Global.centos_user
    elif args.os == "atomic":
        Global.owner_id = Global.atomic_owner_id
        Global.owner_alias = Global.atomic_owner_alias
        Global.default_modules.remove("boto3")
        Global.default_modules.remove("awscli")
        Global.default_modules.remove("botocore")
        Global.default_packages.append("python-pip python-setuptools python-boto3 python-botocore")
        Global.default_packages.append("salt-minion")
        if args.virt != "pv":
            logging.error("Using centos OS %s" % (args.os))
            ami = Global.atomic_ami
        else:
            logging.error("PV not allowed for Centos Atomic")
            exit(3)
        if not args.ssh_user:
            args.ssh_user = Global.atomic_user
    else:
        logging.error("OS not recognized %s" % (args.os))
    logging.critical("Using ssh_user: %s" % (args.ssh_user))
    logging.critical("Using defined value (owner_id): %s" % (Global.owner_id))
    logging.critical("Using defined value (owner_alias): %s" % (Global.owner_alias))
    logging.critical("Using defined value (ami): %s" % (ami))

    Global.packer_values['source_ami'] = image
    Global.packer_values['template'] = template_name
    if args.type == "ecs":
        Template().write_template('', "create_users.jinja2", Global.createuser_dest, Global.scripts_template_path, "create_users")
    else:
        Global.packer_values['create_user_script'] = ""
    if args.role == "sumologic":
        Template().write_template(Global.Global.services_values, "services.jinja2", Global.services_script, services_template_path, "services")
    else:
        Template().write_template(Global.salt_grains_values, "instance_grains.jinja2", Global.salt_grains_template, salt_template_path, "salt grains")
    Template().write_template(Global.packer_values, template_name + ".jinja2", Global.packer_template, packer_template_path + args.os + "/", "packer")
    Template().write_template(Global.userdata_values, args.os + ".jinja2", Global.userdata_dest, os_template_path, "userdata")
    Template().write_template(Global.shell_values, 'shell.jinja2', Global.shell_dest, scripts_template_path, "shell")

    if not args.dry_run:
        if args.type != "docker":
            if ec2(ec2_client).find_image(Global.packer_values['prefix']) != 100:
                ec2(ec2_client).delete_image(ec2(ec2_client).find_image(Global.packer_values['prefix']), args.dry_run)
                elapsed = Global.elapsed
                while ec2(ec2_client).find_image(Global.packer_values['prefix']) != 100:
                    status = ec2(ec2_client).find_image(Global.packer_values['prefix'])
                    elapsed = elapsed + Global.secs
                    sys.stdout.write("Waiting for ami %s to delete ( Elapsed %s secs)%s" % (Global.packer_values['prefix'], elapsed, "\r"))
                    sys.stdout.flush()
                    time.sleep(Global.secs)
                    if Global.elapsed == Global.timeout:
                        logging.critical("Timeout %s Reached. Exiting..." % (Global.timeout))
                        exit(Global.timeout)

    if not args.dry_run:
        Exec().Packer(Global.packer_binary, Global.packer_template, Global.shell_dest, Global.salt_grains_template, Global.userdata_dest)

    exit(0)
