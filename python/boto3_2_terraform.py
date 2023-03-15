import os, sys, subprocess
from boto3_response import *

class Converter():

    def __init__(self,Boto3_Response):
        self.Response = Boto3_Response
        self.tf_file  = ''
        self.blocks   = [] 

    def convert(self):

        self.init_block()
        self.convert_vpc()
        self.convert_instance()
        # self.convert_subnet()
        pass

    def init_block(self):
        profile = "default"
        region  = self.Response.region
        init_block_str  = f'provider "aws" {{\n'
        init_block_str += f'profile = {profile}\n'
        init_block_str += f'region  = {region}\n'

        self.blocks.append(init_block_str)

    def convert_vpc(self):

        for jvpc in self.Response.ec2_responses['vpcs']['Vpcs']:
             # Find vpcs name
            tags = self.Response.ec2_responses['tags']['image']
            for jtag in tags:
                if jtag['Key'] == 'Name':
                    name = jtag['Value']
                    break
                     
            cidr_block       = jvpc['CidrBlock']
            instance_tenancy = jvpc['InstanceTenancy']

            vpc_string = f'resource \"aws_vpc\" \"{name}\" {{ \n'

            vpc_string += f'  cidr_block       = \"{cidr_block}\"\n'
            vpc_string += f'  instance_tenancy = \"{instance_tenancy}\"\n\n'

            vpc_string += f'  tags = {{\n'
            for ktag in tags:
                key = ktag['Key']
                val = ktag['Value']
                vpc_string += f'    {key} = \"{val}\"\n'

            vpc_string += '  '
            vpc_string += f'}}\n '
            vpc_string += f'}}\n\n'

            self.blocks.append(vpc_string)
                 
    def convert_instance(self):
        for jinst in self.Response.ec2_responses['instances']['Reservations']:
             # Find instance name
            tags = self.Response.ec2_responses['tags']['image']
            for jtag in tags:
                if jtag['Key'] == 'Name':
                    name = jtag['Value']
                    break
                     
            cidr_block       = jvpc['CidrBlock']
            instance_tenancy = jvpc['InstanceTenancy']

            vpc_string = f'resource \"aws_vpc\" \"{name}\" {{ \n'

            vpc_string += f'  cidr_block       = \"{cidr_block}\"\n'
            vpc_string += f'  instance_tenancy = \"{instance_tenancy}\"\n\n'

            vpc_string += f'  tags = {{\n'
            for ktag in tags:
                key = ktag['Key']
                val = ktag['Value']
                vpc_string += f'    {key} = \"{val}\"\n'

            vpc_string += '  '
            vpc_string += f'}}\n '
            vpc_string += f'}}\n\n'

            self.blocks.append(vpc_string)

    def convert_subnet(self):
        pass

    def write(self):

        with open(self.tf_file,'w') as f:
            for jblock in self.blocks:
                f.write(jblock)

    def validate(self):

        # cd into where terraform is output
        dir = os.path.dirname(os.path.realpath(self.tf_file))
        os.chdir(dir) 

        # terraform init 
        print(f'Initializing...')
        subprocess.run(["terraform","init"])

        # terraform fmt
        print(f'Validating Terraform format...')
        subprocess.run(["terraform","fmt"])

        # terraform validate
        print(f'Validating Terraform config...')
        subprocess.run(["terraform","validate"])

        # terraform plan 
        print(f'Validating Terraform plan...')
        subprocess.run(["terraform","plan"])   

def main():

    if len(sys.argv) > 1:
        raise NotImplemented
    else:
        # Generate boto3 responses from image
        response = Boto3Response()
        response.ami = 'ami-005f9685cb30f234b'
        response.gen_all_responses()

        # Convert responses to terraform config file
        converter = Converter(response)
        converter.tf_file = '/home/jlaser/code/terraform_tools/data/dev_file.tf'
        converter.convert()
        converter.write()
        converter.validate()

if __name__ == '__main__':
    main()