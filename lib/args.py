import argparse


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


class Args:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--type',
            # default="",
            # required=True,
            default="ec2",
            choices=[
                "docker",
                "ec2"
            ],
            help="Container Type [default 'base': shouldn't be changed ]"
        )
        parser.add_argument(
            '--region',
            # required=True,
            choices=[
                "us-east-1",
                "us-west-1",
                "us-west-2"
            ],
            default="us-west-2",
            help="AWS Region ( Default: us-west-2 )"
        )
        parser.add_argument(
            '-v',
            nargs='?',
            default=2,
            action=VAction,
            dest='verbose'
        )
        parser.add_argument(
            '--iam-profile',
            nargs='?',
            metavar='',
            default="",
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
            default="centos",
            help="EC2 SSH User ( Default: NULL )"
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
            default="centos",
            help="OS Type [ ubuntu, centos, amazon, etc ]"
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
            default="single",
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
            # required=True,
            default="latest",
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
            # required=True,
            help="Env of the build [ dev, staging, prod, etc ]"
        )
        parser.add_argument(
            '--application',
            default="ops",
            # required=True,
            help="App to run on container  (required if type is docker)"
        )
        parser.add_argument(
            '--role',
            default="base",
            # required=True,
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
            '--dry-run',
            action='store_true',
            # default=False,
            help="Don't run packer at script conclusion"
        )
        parser.add_argument(
            '--push',
            action='store_true',
            # default=False,
            help="Push to dockerhub"
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            default=True,
            help="clean all templates from /var/tmp"
        )

        self.args = parser.parse_args()

    def __repr__(self):
        return repr((self.args))
