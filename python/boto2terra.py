import sys, os, subprocess
import boto3_response as boto3_resp
import boto3_response_generator as boto3_resp_gen


class Boto3TerraformConverter():

    def __init__(self,responses=None,terraform_file=None):
        self.responses = responses
        if self.responses is None:
            raise Exception('Need responses from boto3!')
        
        self.terraform_file = terraform_file
        if self.terraform_file is None:
            self.terraform_file = os.path.join(os.getcwd(),'terraform_converted.tf')

        self.blocks = dict()

    def vpc2terra(self):
        """"
        Converts boto3 VPC to terraform format

        Inputs:
        resp_vpcs - AWS response from describe_vpcs()
        resp_tags - AWS response from describe_tags()

        Outputs:
        List of terraform formatted vpcs
        """    
        vpcs_response = self.responses.vpcs['vpcs_response']
        vpcs_tags = self.responses.vpcs['vpcs_tags_response']

        vpcs = []
        for jvpc in vpcs_response['Vpcs']:
            cidrblock = jvpc['CidrBlock']
            instance_tenancy = jvpc['InstanceTenancy']
            vpc_string  = f'resource \"aws_vpc\" \"main\" {{ \n'
            vpc_string += f'  cidr_block = \"{cidrblock}\"\n'
            vpc_string += f'  instance_tenancy = \"{instance_tenancy}\"\n'
            vpc_string += f'  tags = {{\n'
            for jtag in vpcs_tags['Tags']:
                key = jtag['Key']
                val = jtag['Value']
                vpc_string += f'    {key} = \"{val}\"\n'
            vpc_string += f'  }}\n}}'

            vpcs.append(vpc_string)

        self.blocks['vpcs'] = vpcs

        return vpcs
    
    def validate_conversion(self):

        dir_path = os.path.dirname(os.path.realpath(self.terraform_file))
        print(f'Locating terraform file...')
        os.chdir(dir_path)
        print(f'Located terraform file in {dir_path}')

        print(f'{os.getcwd()}')

        print(f'Initializing terraform...')
        subprocess.run(["terraform","init"])

        print(f'Linting converted terraform file...')
        subprocess.run(["terraform","fmt"])

        print(f'Validating terraform file...')
        subprocess.run(["terraform","validate"])

        print(f'Validating existing cloud state...')
        subprocess.run(["terraform","plan"])

    def write(self):
        """
        Write terraform file
        
        """

        # Write vpcs to file
        with open(self.terraform_file,'w') as f:
            for jvpc in self.blocks['vpcs']:
                f.write(jvpc)


def main(out_file):
    """"
    Convert boto3 JSON from AWS to terraform format

    Inputs:

    Outputs:
    """

    if len(sys.argv) > 1: # User input AWS client
        raise NotImplemented('Need to decide how user can input AWSResponse')
    
    else: # Create AWS resources from example if none is provided
        responses = boto3_resp_gen.main()

    converter = Boto3TerraformConverter(responses,terraform_file=out_file)

    vpcs = converter.vpc2terra()    

    with open(out_file,'w') as f:
        for jvpc in vpcs:
            f.write(jvpc)

    # Validate configuration
    converter.validate_conversion()

    return


if __name__ == "__main__":

    # Assume boto3 response generator is given as first argument
    # python boto2terra.py boto3_response_generator.py boto3_input.json
    # boto3_json = sys.argv[0]
    out_file = '/home/jlaser/code/terraform_tools/data/terraform_converted.tf'
    main(out_file)

