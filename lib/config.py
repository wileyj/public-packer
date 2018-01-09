import time
import os
from datetime import datetime
from args import Args


class Global:
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
    name_prefix = "wileyj"
    cwd = os.getcwd()
    salt_state_tree = cwd + "/salt/srv/salt"
    salt_pillar_root = cwd + "/salt/srv/pillar"
    bootstrap_args = "-d -M -N -X -q -Z -c /tmp"
    repo_address = "yumrepo.moil.io"
    repo_dns = "yumrepo.moil.io"
    primary_disk_size = 50
    secondary_disk_size = 100

    ec2_owner = {
        'amazon': {
            'id': '137112412989',
            'alias': 'amazon',
            'hvm': 'amzn-ami-hvm*',
            'pv': 'amzn-ami-pv*',
            'login': 'ec2-user'
        },
        'centos': {
            'id': '679593333241',
            'alias': '',
            'hvm': 'CentOS*7*64*',
            'pv': '',
            'login': 'centos'

        },
        'ubuntu': {
            'id': '099720109477',
            'alias': '',
            'hvm': 'ubuntu*16*amd64*server*',
            'pv': '',
            'login': 'ubuntu'

        },
        'coreos': {
            'id': '595879546273',
            'alias': '',
            'hvm': 'CoreOS*stable*hvm',
            'pv': '',
            'login': 'core'

        },
        'atomic': {
            'id': '410186602215',
            'alias': '',
            'hvm': 'CentOS*Atomic*Host*x86_64*HVM*',
            'pv': '',
            'login': 'centos'
        }
    }
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

    sumo_access_id = "<sumo_access_id>"
    sumo_access_key = "<sumo_access_key>"
    quay_auth = "<quay_auth_key>"
    quay_email = ""
    quay_url = "https://quay.io"
    docker_auth = "<docker_auth_key>"
    docker_email = "<docker_auth_email>"
    docker_url = "https://index.docker.io/v1/"
    etcd_cluster = "http://local.com:2380"
    log_disk = "xvdf"
    log_mount = "/srv/log"
    enhanced_networking = ""
    extra_script = ""
    packer_template = "/var/tmp/packer-" + str(epoch) + ".json"
    userdata_dest = "/var/tmp/user_data-" + str(epoch)
    salt_grains_template = "/var/tmp/salt_grains-" + str(epoch)
    shell_dest = "/var/tmp/shell-" + str(epoch) + ".sh"
    createuser_dest = "/var/tmp/create_users-" + str(epoch) + ".py"
    services_script = "/var/tmp/services-" + str(epoch) + ".sh"
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
        "boto",
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
    shell_values = {
        'os': args.os,
        'type': args.type
    }

    services_values = {
        'runit_services': '',
        'services_packages': services_packages
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
        'ssh_user': ec2_owner[args.os]['login'],
        'vpc_id': args.vpc_id,
        'subnet_id': args.subnet_id,
        'region': args.region,
        'packages': default_packages,
        'modules': default_modules,
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
        'inline': inline,
        'cwd': cwd,
        'image': args.image,
        'salt_grains_file': salt_grains_template,
        'default_packages': default_packages,
        'salt_state_tree': salt_state_tree,
        'salt_pillar_root': salt_pillar_root,
        'bootstrap_args': bootstrap_args,
        'docker_push': args.push,
        'public_ip': args.public_ip,
        'primary_disk': primary_disk_size,
        'secondary_disk': secondary_disk_size
    }
