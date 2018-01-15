import time
import os
import json
from datetime import datetime
from args import Args

dirs = []
files = []
packages = []
pip_modules = []


class Global:
    def get_vals(object):
        # dirs
        for dir in object.get('dirs', None):
            dirs.append(dir)
        for package in object.get('packages', None):
            packages.append(package)
        for file in object.get('files', None):
            print "Found files: %s" % (object.get('files', None))
            files.append(file)
        for module_type in object['modules']:
            # print "module_type; %s" % (module_type)
            # print "module: %s" % (module_type['pip'])
            if module_type.get('pip', None) is not None:
                for module in module_type.get('pip', None):
                    pip_modules.append(module)
        return True
    args = Args().args
    epoch = time.time()
    user = os.getlogin()
    secs = 10
    elapsed = 0
    timeout = 300
    timestamp = datetime.utcnow().isoformat()
    today = datetime.now()
    current_time = int(round(time.time()))
    short_date = str('{:04d}'.format(today.year)) + str('{:02d}'.format(today.month)) + str('{:02d}'.format(today.day))
    short_hour = str('{:04d}'.format(today.year)) + str('{:02d}'.format(today.month)) + str('{:02d}'.format(today.day)) + "_" + str(current_time)
    cwd = os.getcwd()
    # parent = os.path.abspath(os.path.join(cwd, os.pardir))
    config = json.load(open(args.config))
    packer_template = "/var/tmp/packer-" + str(epoch) + ".json"
    userdata_dest = "/var/tmp/user_data-" + str(epoch)
    salt_grains_template = "/var/tmp/salt_grains-" + str(epoch)
    shell_dest = "/var/tmp/shell-" + str(epoch) + ".sh"
    createuser_dest = "/var/tmp/create_users-" + str(epoch) + ".py"
    services_script = "/var/tmp/services-" + str(epoch) + ".sh"
    enhanced_networking = ""
    extra_script = ""
    if args.os == "debian" or args.os == "ubuntu":
        os_family = "debian"
    elif args.os == "centos" or args.os == "amazon":
        os_family = "redhat"
    else:
        os_family = "generic"
    if args.os == "amazon":
        config['default']['packages'].append("ppython27-setuptools python27-boto3 python27-botocore python27-pycrypto python27-pyzmq salt27-minion")
        config['default']['packages'].append("aws-apitools-common aws-cli zeromq vim-enhanced openssh openssh-clients openssh-server")
        config['default']['pip_modules'].append("salt")
    elif args.os == "ubuntu" or args.os == "debian":
        config['default']['packages'].append("vim openssh-client openssh-server python-pip salt-minion")
    elif args.os == "centos":
        config['default']['pip_modules'].remove("boto3")
        config['default']['pip_modules'].remove("awscli")
        config['default']['pip_modules'].remove("botocore")
        config['default']['packages'].append("python-pip python-setuptools python-boto3 python-botocore salt-minion")
        if args.type != "docker":
            config['default']['packages'].append("vim-enhanced openssh openssh-clients openssh-server")
    elif args.os == "atomic":
        config['default']['pip_modules'].remove("boto3")
        config['default']['pip_modules'].remove("awscli")
        config['default']['pip_modules'].remove("botocore")
        config['default']['packages'].append("python-pip python-setuptools python-boto3 python-botocore")
        config['default']['packages'].append("salt-minion")

    if config.get('cleanup', None):
        if config['cleanup'].get('global', None) is not None:
            print "cleanup global: %s" % (config['cleanup'][os_family][args.type].get(args.os, None))
            get_vals(config['cleanup']['global'])
        else:
            print "no global cleanup data in config.json"

        if config['cleanup'][os_family].get(args.type, None):
            print "cleanup os_family/type/os: %s" % (config['cleanup'][os_family][args.type].get(args.os, None))
            get_vals(config['cleanup'][os_family][args.type][args.os])
            print "cleanup os_family/type/global: %s" % (config['cleanup'][os_family][args.type].get(args.os, None))
            get_vals(config['cleanup'][os_family][args.type]['global'])
        else:
            print "no os_family/type"
        if config['cleanup'][os_family][args.type].get(args.os, None):
            print "cleanup os_family/type/os: %s" % (config['cleanup'][os_family][args.type].get(args.os, None))
            get_vals(config['cleanup'][os_family]['global'])
            # get_vals(config['cleanup'][os_family][type]['global'])
            # get_vals(config['cleanup'][os_family][type][os])
        else:
            print "no os_family/global"
    else:
        print "no cleanup in config.json"

    shell_values = {
        'os': args.os,
        'type': args.type,
        'tagname': args.tag,
        'role': args.role,
        'dirs': ' '.join(dirs),
        'files': files,
        'packages': ' '.join(packages),
        'pip_modules': ' '.join(pip_modules)
    }
    userdata_values = {
        'os': args.os,
        'repo_address': config['default']['repo_address'],
        'exclude_list': ' '.join(config['default']['exclude_list'])
    }
    if args.role == 'base':
        args.cleanup = "true"
    else:
        args.cleanup = ""
    salt_grains_values = {
        'region': args.region,
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
        'type': args.type,
        'build_type': 'Packer'
    }
    packer_values = {
        'source_ami': '',
        'instance_type': args.instance_type,
        'instance_profile': args.iam_profile,
        'ssh_user': config['default']['ami'][args.os]['login'],
        'vpc_id': args.vpc_id,
        'subnet_id': args.subnet_id,
        'region': args.region,
        'default_packages': ' '.join(config['default']['packages']),
        'pip_modules': ' '.join(config['default']['pip_modules']),
        'user_data_file': userdata_dest,
        'create_user_script': createuser_dest,
        'platform': args.platform,
        'prefix': args.prefix,
        'tag': args.tag,
        'type': args.type,
        'release': args.release,
        'os': args.os,
        'application': args.application,
        'role': args.role,
        'environment': args.env,
        'script': shell_dest,
        'services_script': services_script,
        'template': '',
        'sudo': "{{ .Path }}",
        'timestamp': timestamp,
        'extra_script': args.script,
        'extra_script_args': args.script_args,
        'inline': config['default']['inline'],
        'image': args.image,
        'salt_grains_file': salt_grains_template,
        'salt_state_tree': cwd + config['default']['salt_state_tree_suffix'],
        'salt_pillar_root': cwd + config['default']['salt_pillar_root_suffix'],
        'bootstrap_args': config['default']['bootstrap_args'],
        'docker_push': args.push,
        'public_ip': args.public_ip,
        'primary_disk': config['default']['primary_disk_size'],
        'secondary_disk': config['default']['secondary_disk_size'],
        'quay_url': config['default']['quay_url'],
        'quay_auth': config['default']['quay_auth'],
        'quay_email': config['default']['quay_email'],
        'docker_url': config['default']['docker_url'],
        'docker_auth': config['default']['docker_auth'],
        'docker_email': config['default']['docker_email'],
        'sumo_access_id': config['default']['sumo_access_id'],
        'sumo_access_key': config['default']['sumo_access_key']
    }
