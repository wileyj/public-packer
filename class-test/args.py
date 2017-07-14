import argparse


class Args:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--type',
            default="ec2",
            help="Container Type [default 'base': shouldn't be changed ]"
        )
        parser.add_argument(
            '--region',
            default="us-west-2",
            help="AWS Region ( Default: us-west-2 )"
        )
        self.args = parser.parse_args()

    def __repr__(self):
        return repr((self.args))
