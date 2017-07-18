import boto3


class conn():
    def boto3(self, service, region):
        ec2_client = boto3.client(service, region_name=region)
        return ec2_client
