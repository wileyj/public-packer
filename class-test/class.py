from ec2 import ec2
from aws_conn import conn
from args import Args
from config import Global
import logging
from logger import Logger
from template import Template

args = Args().args
print "Type: %s" % (args.type)
print "Region: %s" % (args.region)
print "verbose: %s" % (args.verbose)
print Global.centos_ami

ec2_client = conn().boto3('ec2', args.region)
image = ec2(ec2_client).get_image(Global.centos_ami, Global.centos_owner_id, '', args.type)
print "Image: %s" % (image)
print ec2(ec2_client).find_image('')

logger = Logger()
logging.debug('debug message')
logging.info('info message')
logging.warn('warn message')
logging.error('error message')
logging.critical('critical message')


#
# packer_values = {
#     'source_ami' : get_ec2_images(ami, owner_id, owner_alias, args.type),
#     'instance_type': args.instance_type,
#     'instance_profile': args.iam_profile,
#     'ssh_user': ssh_user,
#     'vpc_id': args.vpc_id,
#     'subnet_id': args.subnet_id,
#     'region': args.region,
#     'packages': default_packages,
#     'modules': default_modules,
#     'user_data_file': userdata_dest,
#     'create_user_script': createuser_dest,
#     'platform': args.platform,
#     'prefix' : args.prefix,
#     'tag': args.tag,
#     'type': defined_type,
#     'release': args.release,
#     'os': args.os,
#     'application': args.application,
#     'role': args.role,
#     'environment': args.env,
#     'script': shell_dest,
#     'services_script': services_script,
#     'template': template_name,
#     'sudo': "{{ .Path }}",
#     'timestamp': timestamp,
#     'extra_script': args.script,
#     'extra_script_args': args.script_args,
#     'inline': inline,
#     'cwd': cwd,
#     'image': args.image,
#     'salt_grains_file': salt_grains_template,
#     'default_packages': default_packages,
#     'salt_state_tree': salt_state_tree,
#     'salt_pillar_root': salt_pillar_root,
#     'bootstrap_args': bootstrap_args,
#     'docker_push': args.push,
#     'public_ip': args.public_ip
# }
#
# if args.role == 'base':
#     args.cleanup = "true"
# else:
#     args.cleanup = ""
#
# salt_grains_values = {
#     'platform': args.platform,
#     'prefix': args.prefix,
#     'instance_profile': args.iam_profile,
#     'vpc_id': args.vpc_id,
#     'tag': args.tag,
#     'release': args.release,
#     'environment': args.env,
#     'subnet_id': args.subnet_id,
#     'cleanup': args.cleanup,
#     'application': args.application,
#     'role': args.role,
#     'type': defined_type,
#     'build_type': 'Packer'
# }
#
# userdata_values = {
#     'os': args.os,
#     'repo_address': repo_address,
#     'exclude_list': exclude_list,
#     # 'image_name': image_name,
#     # 'image_tag': image_tag
#     # 'sumo_access_id': sumo_access_id,
#     # 'sumo_access_key': sumo_access_key
# }
# if defined_type == "Docker" or args.os == "atomic" or args.os == "coreos":
#     userdata_values['quay_auth'] = quay_auth
#     userdata_values['quay_email'] = quay_email
#     userdata_values['quay_url'] = quay_url
#     userdata_values['docker_auth'] = docker_auth
#     userdata_values['docker_email'] = docker_email
#     userdata_values['docker_url'] = docker_url
#     userdata_values['etcd_cluster'] = etcd_cluster
#     userdata_values['log_disk'] = log_disk
#     userdata_values['log_mount'] = log_mount
#
# shell_values = {
#     'os': args.os
# }
#
# services_values = {
#     'runit_services': '',
#     'services_packages': services_packages
# }
#
#
# if args.type == "ecs":
#     Template.write_template('', "create_users.jinja2", Global.createuser_dest, Global.scripts_template_path, "create_users")
# else:
#     Global.packer_values['create_user_script'] = ""
# if args.role == "sumologic":
#     Template.write_template(Global.services_values, "services.jinja2", Global.services_script, Global.services_template_path, "services")
# else:
#     Template.write_template(Global.salt_grains_values, args.type + "_grains.jinja2", Global.salt_grains_template, Global.salt_template_path, "salt grains")
# Template.write_template(Global.packer_values, Global.template_name + ".jinja2", Global.packer_template, Global.packer_template_path + args.os + "/", "packer")
# Template.write_template(Global.userdata_values, args.os + ".jinja2", Global.userdata_dest, Global.os_template_path, "userdata")
# Template.write_template(Global.shell_values, 'shell.jinja2', Global.shell_dest, Global.scripts_template_path, "shell")
