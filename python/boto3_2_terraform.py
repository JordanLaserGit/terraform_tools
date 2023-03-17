import  sys, pickle
from boto3_response import *
from terra_blocks import ProviderBlock, ResourceBlock
from terraform_file import TerraformFile

def main():

    if len(sys.argv) > 1:
        raise NotImplemented
    else:
        # # Generate boto3 responses from image
        response = Boto3Response()
        response.ami = 'ami-005f9685cb30f234b'
        response.gen_all_responses()
        response.tag_split()
        with open('/home/jlaser/code/terraform_tools/AWS_response.obj','wb') as f:
            pickle.dump(response.ec2_responses,f)

        # # Read response dictionary from file and refill class
        # response = Boto3Response()
        # response.ami = 'ami-005f9685cb30f234b'
        # with open('/home/jlaser/code/terraform_tools/AWS_response.obj','rb') as f:
        #     response = pickle.load(f)

        # response.ec2_responses = response

        boto3_response = response

        # Convert responses to terraform config file
        TF = TerraformFile()
        TF.file = '/home/jlaser/code/terraform_tools/data/dev_file.tf'

        # Here lies the logic of how to decide which blocks are placed in the TF file
        # Once this decision is made, the logic baked into the block classes will 
        # build their block strings with mapping logic built in. TF will write each
        # of the block strings to file and then validate against the existing infrastructure

        ii_provider = True
        ii_vpc      = len(boto3_response.ec2_responses['vpcs']['Vpcs']) > 0

        
        if ii_provider:
            PB = ProviderBlock(boto3_response)
            TF.Blocks.append(PB)

        
        if ii_vpc:
            for jvpc in range(len(boto3_response.ec2_responses['vpcs']['Vpcs'])): 

                # Maybe this response packaging should be done in boto3_response?
                vpc_response = {}
                vpc_response['vpc']                              = boto3_response.ec2_responses['vpcs']['Vpcs'][jvpc]
                vpc_response['enableDnsSupport']                 = boto3_response.ec2_responses['enableDnsSupport'][jvpc]
                vpc_response['enableDnsHostnamespc']             = boto3_response.ec2_responses['enableDnsHostnames'][jvpc]
                vpc_response['enableNetworkAddressUsageMetrics'] = boto3_response.ec2_responses['enableNetworkAddressUsageMetrics'][jvpc]
                VPC = ResourceBlock('aws_vpc',vpc_response)
                TF.Blocks.append(VPC)

        # TODO: Do all the other blocks


        # Write the file and validate it matches the existing infrastructure
        TF.write()
        TF.validate()

if __name__ == '__main__':
    main(),