import boto3


class conn():
    def ec2(self, region):
        ec2_client = boto3.client('ec2', region_name=region)
        return ec2_client
