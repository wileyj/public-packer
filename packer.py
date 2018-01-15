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
    image = ec2(ec2_client).get_image(Global.config['default']['ami'][args.os][args.virt], Global.config['default']['ami'][args.os]['id'], Global.config['default']['ami'][args.os]['alias'], args.type)
    logging.error("Image: %s" % (image))
    args.type.lower()
    args.prefix_platform = ""
    args.prefix_app = ""
    if args.type != "base" and args.type != "ec2" and args.type != "docker":
        args.type = "ec2"
    if args.type == "docker":
        image_tag = args.os + "." + args.role + "." + args.tag
        template_name = args.template
        packer_template_path = "templates/" + args.type + "/" + args.os + "/"
        image_name = args.repo + args.prefix_app
        Global.packer_values['tag'] = image_tag
    if args.type == "ec2":
        template_name = args.role
        packer_template_path = "templates/" + args.type + "/" + args.os + "/" + args.disk + "/"
        image_name = Global.config['default']['name_prefix'] + "." + args.os + "_" + args.role + "." + args.type + "_" + args.virt + "_" + args.disk + "." + args.prefix.replace(" ", "-") + "_" + Global.short_date
    Global.salt_grains_values['prefix'] = image_name
    Global.packer_values['prefix'] = image_name
    if args.clean:
        try:
            os.system('rm /var/tmp/*[0-9]*')
        except OSError as e:
            logging.exception("IO Exception occurred: %s" % (e))
    logging.critical("userdata values: %s" % (Global.userdata_values))
    if args.os == "atomic" or args.os == "coreos":
        Global.userdata_values['quay_auth'] = Global.config['default']['quay_auth']
        Global.userdata_values['quay_email'] = Global.config['default']['quay_email']
        Global.userdata_values['quay_url'] = Global.config['default']['quay_url']
        Global.userdata_values['docker_auth'] = Global.config['default']['docker_auth']
        Global.userdata_values['docker_email'] = Global.config['default']['docker_email']
        Global.userdata_values['docker_url'] = Global.config['default']['docker_url']
        Global.userdata_values['etcd_cluster'] = Global.config['default']['etcd_cluster']
        Global.userdata_values['log_disk'] = Global.config['default']['log_disk']
        Global.userdata_values['log_mount'] = Global.config['default']['log_mount']

    salt_template_path = "templates/salt/"
    scripts_template_path = "templates/scripts/"
    os_template_path = "templates/userdata/"
    services_template_path = "templates/runit_services/"

    logging.error("Using ec2_owner id: %s" % (Global.config['default']['ami'][args.os]['id']))
    logging.error("Using ec2_owner alias: %s" % (Global.config['default']['ami'][args.os]['alias']))
    logging.error("Using ec2_owner virt: %s" % (Global.config['default']['ami'][args.os][args.virt]))
    logging.error("Using ec2_owner login: %s" % (Global.config['default']['ami'][args.os]['login']))

    logging.error("Using %s OS" % (args.os))
    if args.ssh_user:
        Global.packer_values['ssh_user'] = args.ssh_user
    if args.virt == "pv" and args.os != "amazon":
        logging.error("Virt of PV not allowed for %s" % (args.os))
        exit(3)
    # if args.os == "amazon":
    #     Global.default_packages.append("ppython27-setuptools python27-boto3 python27-botocore python27-pycrypto python27-pyzmq salt27-minion")
    #     # Global.default_packages.append("python27-pip python27-setuptools python27-boto3 python27-botocore python27-pycrypto python27-pyzmq salt27-minion")
    #     Global.default_packages.append("aws-apitools-common aws-cli zeromq vim-enhanced openssh openssh-clients openssh-server")
    #     Global.default_modules.append("salt")
    # elif args.os == "ubuntu" or args.os == "debian":
    #     Global.default_packages.append("vim openssh-client openssh-server python-pip salt-minion")
    # elif args.os == "centos":
    #     Global.pip_modules.remove("boto3")
    #     Global.pip_modules.remove("awscli")
    #     Global.pip_modules.remove("botocore")
    #     Global.packages.append("python-pip python-setuptools python-boto3 python-botocore salt-minion")
    #     if args.type != "docker":
    #         Global.packages.append("vim-enhanced openssh openssh-clients openssh-server")
    # elif args.os == "atomic":
    #     Global.default_modules.remove("boto3")
    #     Global.default_modules.remove("awscli")
    #     Global.default_modules.remove("botocore")
    #     Global.default_packages.append("python-pip python-setuptools python-boto3 python-botocore")
    #     Global.default_packages.append("salt-minion")

    logging.critical("Using ssh_user: %s" % (Global.config['default']['ami'][args.os]['login']))
    logging.critical("Using defined value (owner_id): %s" % (Global.config['default']['ami'][args.os]['id']))
    logging.critical("Using defined value (owner_alias): %s" % (Global.config['default']['ami'][args.os]['alias']))
    logging.critical("Using defined value (ami): %s" % (Global.config['default']['ami'][args.os][args.virt]))
    Global.packer_values['source_ami'] = image
    Global.packer_values['template'] = template_name
    if args.type == "ecs":
        Template().write_template('', "create_users.jinja2", Global.createuser_dest, Global.scripts_template_path, "create_users")
    else:
        Global.packer_values['create_user_script'] = ""
    Template().write_template(Global.salt_grains_values, args.type + ".jinja2", Global.salt_grains_template, salt_template_path, "salt grains")
    Template().write_template(Global.packer_values, args.role + ".jinja2", Global.packer_template, packer_template_path, "packer")
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
        Exec().Packer(Global.config['default']['packer_binary'], Global.packer_template, Global.shell_dest, Global.salt_grains_template, Global.userdata_dest)

    exit(0)
