import  sys, pickle
from boto3_response import *
from terraform_tools.python.terra_blocks import AWSVPC
from terraform_tools.python.terraform_file import TerraformFile

# class Converter():

#     def __init__(self,Boto3_Response):
#         self.Response = Boto3_Response
#         self.tf_file  = ''
#         self.blocks   = [] 

#     def convert(self):

#         self.init_block()
#         self.convert_vpc()

#         # TODO: will need to detect if there is a aws_launch_template field
#         # and switch to a convert function to handle that block
#         self.convert_instance()
#         # self.convert_subnet()
#         pass

#     def pascal2snake(self,pascal_dict):
#         """
#         Convert variable name case convention
#         """
#         snake_dict = dict()
#         for var in pascal_dict:
#             res = [var[0].lower()]
#             for c in var[1:]:
#                 if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
#                     res.append('_')
#                     res.append(c.lower())
#                 else:
#                     res.append(c)
#             snake_dict[''.join(res)] = pascal_dict[var]

#         return snake_dict


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

        boto3_response = response_new

        # Convert responses to terraform config file
        TF = TerraformFile()
        TF.file = '/home/jlaser/code/terraform_tools/data/dev_file.tf'

        # Here lies the logic of how to decide which blocks are placed in the TF file
        # Once this decision is made, the logic baked into the block classes will 
        # build their block strings with mapping logic built in. TF will write each
        # of the block strings to file and then validate against the existing infrastructure

        ii_provider = True
        if ii_provider:
            PB = ProviderBlock(boto3_response)
            TF.Blocks.append(PB)

        ii_vpc = len(boto3_response.ec2_responses['vpcs']['Vpcs']) > 0
        if ii_vpc:
            for jvpc in boto3_response.ec2_responses['vpcs']['Vpcs']:
                tags = boto3_response.ec2_responses['tags']['image']
                VPC = AWSVPC(jvpc,tags)
                VPC.include_attrs()
                TF.Blocks.append(VPC.Block)

        # TODO: Do all the other blocks


        # Write the file and validate it matches the existing infrastructure
        TF.write()
        TF.validate()

if __name__ == '__main__':
    main(),