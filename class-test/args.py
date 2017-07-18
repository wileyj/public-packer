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
            default="us-west-2",
            help="AWS Region ( Default: us-west-2 )"
        )
        parser.add_argument(
            '-v',
            nargs='?',
            default=3,
            action=VAction,
            dest='verbose'
        )
        self.args = parser.parse_args()

    def __repr__(self):
        return repr((self.args))
