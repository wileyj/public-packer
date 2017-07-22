import time
import os
from datetime import datetime


class Global:
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
    salt_state_tree = cwd + "/../salt/srv/salt"
    salt_pillar_root = cwd + "/../salt/srv/pillar"
    bootstrap_args = "-d -M -N -X -q -Z -c /tmp"
    repo_address = "yumrepo.moil.io"
    repo_dns = "yumrepo.moil.io"

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
