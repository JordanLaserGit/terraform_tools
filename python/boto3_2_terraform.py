import  sys, pickle, os, subprocess
import numpy as np
from boto3_response import *
from terra_blocks import ProviderBlock, ResourceBlock
from terraform_file import TerraformFile

def find_in_dict(nest,keyword,paths=None,location=None):
    """
    Generate path to value if key contains keyword
    """
    if paths is None:
        paths = []
    if location is None:
        location = 'response'
    for jkey in nest:
        val = nest[jkey]
        if type(val) is dict:
            location += f'[\'{jkey}\']'
            paths = find_in_dict(val,keyword,paths,location)
            location = location[:-len(f'[\'{jkey}\']')]
        elif type(val) is list:            
            nval = len(val)
            for jval in range(nval):
                list_val = val[jval]
                if type(list_val) is dict:
                    location += f'[{jval}]'                    
                    paths = find_in_dict(list_val,keyword,paths,location) 
                    location = location[:-len(f'[{jval}]')]               
        else:
            if jkey.find(keyword) >= 0:
                location += f'[\'{jkey}\']'
                paths.append([location,jkey,nest[jkey]])
                location = location[:-len(f'[\'{jkey}\']')]

    return paths

def get_resources(response):
        
    # all_recs      = find_in_dict(response,'Id')
    vpc_recs      = find_in_dict(response,'VpcId')
    subnet_recs   = find_in_dict(response,'SubnetId')
    # Add resources as needed
    # instance_recs = find_in_dict(response,'InstanceId')

    # Find all unique resources
    all_recs = vpc_recs + subnet_recs
    uni_recs = []
    uni_ids  = []
    for jrec in all_recs:
        id = jrec[2]
        rec = jrec[1]
        if id not in uni_ids:
            uni_recs.append(rec)
            uni_ids.append(id)

    return uni_recs,uni_ids

def main():
    mode = sys.argv[1]

    if mode == 'deconstruct':
        """
        In this mode, we 
        1) import all resources found in the existing architecture
        2) Create a config file (.tf) from the state file (.tfstate) that is created from the imports
        3) Ensure our config will match the state file
        4) Delete state file and build a new one from the config
        
        From this config file, we can reconstruct the existing arcitecture exactly. 
        The purpose of deleting the state file and creating a new one is terraform will create new resources (new IDs),
        but those resources should be identical to those which were imported originally.
        """

        # # Generate boto3 responses from image
        response = Boto3Response()
        response.ami = 'ami-005f9685cb30f234b'
        response.gen_all_responses()
        response.tag_split()

        # Obtain list of all resources and their IDs
        uni_recs, uni_ids = get_resources(response.ec2_responses)

        name_table = {"VpcId"   :"vpc",
                      "SubnetId":"subnet"
                    }        

            # Create basic config file that will be used to import the resources
        TF = TerraformFile()
        TF.config_file = '/home/jlaser/code/terraform_tools/data/dev_file.tf'
        PB = ProviderBlock(response)
        TF.Blocks.append(PB)
        TF.write()
        TF.Blocks = []

        # cd into where terraform is output
        dir = os.path.dirname(os.path.realpath(TF.config_file))
        os.chdir(dir)         
        subprocess.run(["terraform","init"])

        nrecs = len(uni_recs)
        for j in range(nrecs):
            jrec = uni_recs[j]
            resource_type = name_table[jrec]
            local_name = resource_type + f'{j}'
            if resource_type == 'vpc':
                VPC = ResourceBlock('aws_vpc',{},local_name)
                TF.Blocks.append(VPC)
            if resource_type == 'subnet':
                SUB = ResourceBlock('aws_subnet',{},local_name)   
                TF.Blocks.append(SUB)     

        TF.append_file()       
                     
                    
        # Now that we have all the resources, lets import them        
        for j in range(nrecs):
            jrec = uni_recs[j]
            jid = uni_ids[j]
            resource_type = name_table[jrec]
            local_name = resource_type + f'{j}'
            print(f'Importing Terraform resource {jrec}...')
            subprocess.run(["terraform","import",f"aws_{resource_type}.{local_name}",f"{jid}"])

        process = subprocess.Popen(["terraform","show"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        tf_str = out.decode() 

        with open(f'/home/jlaser/code/terraform_tools/data/tf_show.txt','w') as f:
            f.write(tf_str)

        with open(f'/home/jlaser/code/terraform_tools/data/tf_show.txt','r') as f:
            tf_lines = f.readlines()


        TF.state2config()                

    elif mode == 'clone':    
        # # Generate boto3 responses from image
        response = Boto3Response()
        response.ami = 'ami-005f9685cb30f234b'
        response.gen_all_responses()
        response.tag_split()
        # with open('/home/jlaser/code/terraform_tools/AWS_response.obj','wb') as f:
        #     pickle.dump(response.ec2_responses,f)

        # # Read response dictionary from file and refill class
        # response = Boto3Response()
        # response.ami = 'ami-005f9685cb30f234b'
        # with open('/home/jlaser/code/terraform_tools/AWS_response.obj','rb') as f:
        #     response = pickle.load(f)
        # response.ec2_responses = response

        boto3_response = response

        # Convert responses to terraform config file
        TF = TerraformFile()
        TF.config_file = '/home/jlaser/code/terraform_tools/data/dev_file.tf'

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

                # This response is built here because a block needs to be formed for each VPC                
                vpc    = boto3_response.ec2_responses['vpcs']['Vpcs'][jvpc]
                vpc_id = vpc['VpcId']

                vpc_response = {}
                vpc_response['vpc']                              = vpc
                vpc_response['enableDnsSupport']                 = boto3_response.ec2_responses['enableDnsSupport'][jvpc]
                vpc_response['enableDnsHostnamespc']             = boto3_response.ec2_responses['enableDnsHostnames'][jvpc]
                vpc_response['enableNetworkAddressUsageMetrics'] = boto3_response.ec2_responses['enableNetworkAddressUsageMetrics'][jvpc]
                
                VPC = ResourceBlock('aws_vpc',vpc_response)
                TF.Blocks.append(VPC)

                # Subnets        
                subnets = boto3_response.ec2_responses['subnets']['Subnets']
                subnet_in_vpc = np.where([vpc_id == jsubnet['VpcId'] for jsubnet in subnets])[0]
                ii_subnet = any(subnet_in_vpc)                
                if ii_subnet: # There are subnets associated with the vpc
                    subnet_subset = [jsubnet for jsubnet in subnets]
                    nsubnet_blocks = len(subnet_subset)

                    for jsubset in range(nsubnet_blocks): # create block for each subnet                        
                        subnet_response = {}
                        subnet_response['vpc']      = vpc
                        subnet_response['vpc_args'] = VPC.args                    
                        subnet_response['subnet']   = subnet_subset[jsubset]

                        ii_tags = [subnet_subset[jsubset]['SubnetId'] == jtag['ResourceId'] for jtag in boto3_response.ec2_responses['tags']['subnet']]
                        jtags_jsubset = np.where(ii_tags)[0]
                        if any(jtags_jsubset): subnet_response['tags']     = boto3_response.ec2_responses['tags']['subnet'][jtags_jsubset]
                        subnet = ResourceBlock('aws_subnet',subnet_response)
                        TF.Blocks.append(subnet)

        # TODO: Do all the other blocks



        # Write the file and validate it matches the existing infrastructure
        TF.write()
        TF.validate()
    else:
        raise Exception(f'Mode {mode} has not yet been implemented')

if __name__ == '__main__':
    main(),