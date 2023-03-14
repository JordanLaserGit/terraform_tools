import boto3
from botocore.config import Config

class AWSResponse():

    def __init__(self):
        self.ec2      = boto3.client('ec2')
        self.ami_id   = ''
        self.region   = ''
        self.vpcs     = dict()

    def gen_vpc_resp(self):
        """"
        Creates ec2 vpc response

        Inputs:
        None

        Outputs:
        vpc reponse: dict()
        
        """

        self.vpcs['vpcs_response']      = self.ec2.describe_vpcs()
        self.vpcs['vpcs_tags_response'] = self.ec2.describe_tags()




