import os, sys, subprocess, pickle
from boto3_response import *

class Converter():

    def __init__(self,Boto3_Response):
        self.Response = Boto3_Response
        self.tf_file  = ''
        self.blocks   = [] 

    def convert(self):

        self.init_block()
        self.convert_vpc()

        # TODO: will need to detect if there is a aws_launch_template field
        # and switch to a convert function to handle that block
        self.convert_instance()
        # self.convert_subnet()
        pass

    def init_block(self):
        profile = "default"
        region  = self.Response.region
        init_block_str  = f'provider "aws" {{\n  '
        init_block_str += f'profile = \"{profile}\"\n  '
        init_block_str += f'region  = \"{region}\"\n}}\n\n'

        self.blocks.append(init_block_str)

    def pascal2snake(self,pascal_dict):
        """
        Convert variable name case convention
        """
        snake_dict = dict()
        for var in pascal_dict:
            res = [var[0].lower()]
            for c in var[1:]:
                if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                    res.append('_')
                    res.append(c.lower())
                else:
                    res.append(c)
            snake_dict[''.join(res)] = pascal_dict[var]

        return snake_dict
    
    def adddict(self,dict_write,ignore,switch,block_string,indent):
        """
        Add dictionary to block string line by line
        """

        depth = 0
        for key in dict_write:
            
            if key not in ignore:
                val = dict_write[key]
                if type(val) is not dict:
                    if val == "True":  val = "true"
                    if val == "False": val = "false"
                    if key in switch:
                        key = switch[key]
                    block_string += f'{key}       = \"{val}\"\n'.rjust(indent,' ')
                else:
                    depth += 1
                    block_string += f'{key}       = {{\n'.rjust(indent,' ')
                    block_string = self.adddict(self.pascal2snake(val),[],switch,block_string,indent+2*depth)
                    block_string += f'}}\n'
                    depth -= 1

        return block_string


    def convert_vpc(self):

        keys_ignore = ['state',
                'vpc_id',
                'cidr_block_association_set',
                'is_default',
                'dhcp_options_id',
                'tags'
                ]

        for jvpc in self.Response.ec2_responses['vpcs']['Vpcs']:
            tags = self.Response.ec2_responses['tags']['image']
            for jtag in tags:
                if jtag['Key'] == 'Name':
                    name = jtag['Value']
                    break                     

            jvpc_snake = self.pascal2snake(jvpc)

            vpc_string = f'resource \"aws_vpc\" \"{name}\" {{ \n'

            vpc_string = self.adddict(jvpc_snake,keys_ignore,{},vpc_string,2)
            vpc_string += f'  tags = {{\n'
            for ktag in tags:
                vpc_string = self.adddict(ktag,[],{},vpc_string,4)

            vpc_string += '  '
            vpc_string += f'}}\n ' 
            vpc_string += f'}}\n\n'

            self.blocks.append(vpc_string)
                 
    def convert_instance(self):
        """
        Creates the terraform block string for each instance
        """
        
        # TODO: root_block_device
        # security_groups - > need to get only string with GroupName
        # virtualization_type this may be in the filter block of the VPC
        keys_ignore = ['ami_launch_index',
                       'private_dns_name',
                       'instance_id',
                       'launch_time',
                       'product_codes',
                       'tags',
                       'placement',
                       'root_device_name',
                       'root_device_type',
                       'security_groups',
                       'cpu_options',
                       'public_dns_name',
                       ]
        
        keys_switch = {"image_id":"ami",
                       "private_ip_address":"private_ip",
                       "public_ip_address":"associate_public_ip_address",
                       "network_interfaces":"network_interface",
                       "enable_resource_name_dns_a_a_a_a_record":"enable_resource_name_dns_a_record",
                       "image_id":"ami",
                       "image_id":"ami",
                       "image_id":"ami",
                       "image_id":"ami",
                       }      

        for jinst in self.Response.ec2_responses['instances']['Reservations'][0]['Instances']:

            jinst_snake = self.pascal2snake(jinst)

            # Get security group names
            sec_grps = []
            for jgrp in jinst['SecurityGroups']:
                sec_grps.append(jgrp['GroupName'])

            # Get placement group names
            place_grps = []
            place_grps = jinst['Placement']['GroupName']
            
            keys_adjust = {'security_groups':sec_grps,
                        'cpu_core_count':jinst_snake['cpu_options']['CoreCount'],
                        'placement_group':place_grps,
                        }  
        
            tags = jinst['Tags']
            for jtag in tags:
                if jtag['Key'] == 'Name':
                    name = jtag['Value']
                    break                     

            

            jinst_string = f'resource \"aws_instance\" \"{name}\" {{ \n'

            jinst_string = self.adddict(jinst_snake,keys_ignore,keys_switch,jinst_string,2)
            jinst_string += f'  tags = {{\n'
            for ktag in tags:
                jinst_string = self.adddict(ktag,[],{},jinst_string,4)

            jinst_string += '  '
            jinst_string += f'}}\n ' 
            jinst_string += f'}}\n\n'

            self.blocks.append(jinst_string)

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
        # # Generate boto3 responses from image
        # response = Boto3Response()
        # response.ami = 'ami-005f9685cb30f234b'
        # response.gen_all_responses()
        # response.tag_split()
        # with open('/home/jlaser/code/terraform_tools/AWS_response.obj','wb') as f:
        #     pickle.dump(response.ec2_responses,f)

        # Read response dictionary from file and refill class
        response_new = Boto3Response()
        response_new.ami = 'ami-005f9685cb30f234b'
        with open('/home/jlaser/code/terraform_tools/AWS_response.obj','rb') as f:
            new_thing = pickle.load(f)

        response_new.ec2_responses = new_thing

        # Convert responses to terraform config file
        converter = Converter(response_new)
        converter.tf_file = '/home/jlaser/code/terraform_tools/data/dev_file.tf'
        converter.convert()
        converter.write()
        converter.validate()

if __name__ == '__main__':
    main(),