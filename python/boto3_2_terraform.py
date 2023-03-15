import os, sys, subprocess
from boto3_response import *

class Converter():

    def __init__(self,Boto3_Response):
        self.Response = Boto3_Response
        self.tf_file  = ''
        self.blocks   = [] 

        
    def convert(self):


       
        for jvpc in self.Response.ec2_responses['vpcs']['Vpcs']:
             name = 'main'
             cidr_block = jvpc['CidrBlock']
             instance_tenancy = jvpc['InstanceTenancy']

             vpc_string = f'\"resource\" \"aws_vpc\" \"{name}\" {{ \n'

             vpc_string += f'cidr_block = \"{cidr_block}\"\n'
             vpc_string += f'cidr_block = \"{instance_tenancy}\"\n'

             vpc_string += f'tags = {{\"{instance_tenancy}\"\n'
            #  for pair in self.Response.ec2_responses['tags']


        pass

    def write(self):
        pass

    def validate(self):

        # cd into where terraform is output
        # 
        # terraform init 
        # 
        # terraform fmt
        # 
        # terraform validate
        # 
        # terraform plan 
        pass       

def main():

    if len(sys.argv) > 1:
        raise NotImplemented
    else:
        response = Boto3Response()
        response.gen_vpc_response()

        converter = Converter(response)
        converter.convert()
        converter.write()
        converter.validate()

if __name__ == '__main__':
    main()