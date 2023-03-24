from random_word import RandomWords

class ProviderBlock():

    def __init__(self,Response):
        self.args = dict()

        profile = "default"
        region  = Response.region
        self.block_str  = f'provider "aws" {{\n  '
        self.block_str += f'profile = \"{profile}\"\n  '
        self.block_str += f'region  = \"{region}\"\n'

class ResourceBlock():

    def __init__(self, resource, Response,local_name=None):        
    
        if resource == 'aws_vpc':
            self.args = get_aws_vpc_mapping(Response)
        elif resource == 'aws_subnet':
            self.args = get_aws_subnet_mapping(Response)
        elif resource == 'aws_instance':
            self.args = get_aws_instance_mapping(Response)            
        else:
            raise Exception(f'{resource} is not within the built responses. Perhaps contact Jordan and ask him to build it.')
        
        # Note! Terraform local name and the tag 'Name" (from boto3) are not necessarily the same.
        # Buuuut we treat them as the same here. boto3 does not have a local_name for resources.
        if local_name is None:
            try:
                local_name = self.args['tags']['Name']
            except:
                local_name = RandomWords().get_random_word()
                print(f'Assigning random name to subnet: {local_name}')

        self.block_str   = f'resource \"{resource}\" \"{local_name}\" {{ \n'

############
# mapping #
############
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources

"""
TEMPLATE

def get_<>_mapping(response):
    # arguments   
    mapping = {} 

    # Conditions under which we want to include this arguement
    ii_arg1 = False
    ii_arg2 = False
    ii_arg3 = False

    if ii_arg1:
        mapping['arg1'] = init_val
    if ii_arg1:
        mapping['arg2'] = init_val
    if ii_arg3:
        mapping['arg3'] = init_val

    return mapping

"""
# aws_subnet
def get_aws_instance_mapping(response):

    init_val = None

    # Optional arguments   
    mapping = {} 

    if 'instance' not in response:
        # return required fields
        return mapping

    # TODO, create mapping if we still want to go that route. 
    # vpc_local_name = response['vpc_args']['tags']['Name']

    # # Give variable reference 
    # # vpc_id = response['vpc']['VpcId']
    # vpc_id = f'VARaws_vpc.{vpc_local_name}.id'

    # # Conditions under which we want to include this arguement
    # ii_availability_zone    = 'AvailabilityZone' in response['subnet']
    # # ii_availability_zone_id = 'AvailabilityZoneId' in response['subnet']
    # ii_cidr_block           = 'CidrBlock' in response['subnet']
    # # ii_default_for_az       = 'DefaultForAz' in response['subnet'] Terraform throws an error on state even though its specified in the docs?
    # ii_filter               = False # Need implementation
    # # ii_id                   = 'SubnetId' in response['subnet']
    # ii_ipv6_cidr_block      = False # Need implementation
    # # ii_state                = 'State' in response['subnet'] Terraform throws an error on state even though its specified in the docs?
    # ii_tags                 = 'tags' in response
    # ii_vpc_id               = True

    # # Include arguments if criteria is met   
    # if ii_availability_zone:
    #     mapping['availability_zone']    = response['subnet']['AvailabilityZone']    
    # # if ii_availability_zone_id:
    # #     mapping['availability_zone_id'] = response['subnet']['AvailabilityZoneId']
    # if ii_cidr_block:
    #     mapping['cidr_block']           = response['subnet']['CidrBlock']
    # # if ii_default_for_az: 
    # #     mapping['default_for_az']       = response['subnet']['DefaultForAz']
    # if ii_filter:
    #     raise NotImplementedError()
    #     mapping['filter' ]              = init_val      
    # # if ii_id:
    # #     mapping['id']                   = response['subnet']['SubnetId']     
    # if ii_ipv6_cidr_block:  
    #     raise NotImplementedError()
    #     mapping['ipv6_cidr_block']      = init_val
    # # if ii_state:
    # #     mapping['state']                = response['subnet']['State']   
    # if ii_tags:
    #     mapping['tags']                 = response['tags']
    # if ii_vpc_id:
    #      mapping['vpc_id']              = vpc_id                              

    return mapping

# aws_subnet
def get_aws_subnet_mapping(response):

    init_val = None

    # Optional arguments   
    mapping = {} 

    if 'subnet' not in response:
        # return required fields
        return mapping

    vpc_local_name = response['vpc_args']['tags']['Name']

    # Give variable reference 
    # vpc_id = response['vpc']['VpcId']
    vpc_id = f'VARaws_vpc.{vpc_local_name}.id'

    # Conditions under which we want to include this arguement
    ii_availability_zone    = 'AvailabilityZone' in response['subnet']
    # ii_availability_zone_id = 'AvailabilityZoneId' in response['subnet']
    ii_cidr_block           = 'CidrBlock' in response['subnet']
    # ii_default_for_az       = 'DefaultForAz' in response['subnet'] Terraform throws an error on state even though its specified in the docs?
    ii_filter               = False # Need implementation
    # ii_id                   = 'SubnetId' in response['subnet']
    ii_ipv6_cidr_block      = False # Need implementation
    # ii_state                = 'State' in response['subnet'] Terraform throws an error on state even though its specified in the docs?
    ii_tags                 = 'tags' in response
    ii_vpc_id               = True

    # Include arguments if criteria is met   
    if ii_availability_zone:
        mapping['availability_zone']    = response['subnet']['AvailabilityZone']    
    # if ii_availability_zone_id:
    #     mapping['availability_zone_id'] = response['subnet']['AvailabilityZoneId']
    if ii_cidr_block:
        mapping['cidr_block']           = response['subnet']['CidrBlock']
    # if ii_default_for_az: 
    #     mapping['default_for_az']       = response['subnet']['DefaultForAz']
    if ii_filter:
        raise NotImplementedError()
        mapping['filter' ]              = init_val      
    # if ii_id:
    #     mapping['id']                   = response['subnet']['SubnetId']     
    if ii_ipv6_cidr_block:  
        raise NotImplementedError()
        mapping['ipv6_cidr_block']      = init_val
    # if ii_state:
    #     mapping['state']                = response['subnet']['State']   
    if ii_tags:
        mapping['tags']                 = response['tags']
    if ii_vpc_id:
         mapping['vpc_id']              = vpc_id                              

    return mapping

# aws_vpc
def get_aws_vpc_mapping(response):

    init_val = None

    # arguments   
    mapping = {} 

    if 'vpc' not in response:
        # return required fields
        return mapping

    # Conditions under which we want to include this arguement
    ii_cidr_block                           = 'CidrBlock' in response['vpc']
    ii_instance_tenancy                     = 'InstanceTenancy' in response['vpc']
    ii_enable_dns_support                   = 'enableDnsSupport' in response
    ii_enable_dns_hostnames                 = 'enableDnsHostnamespc' in response
    ii_enable_network_address_usage_metrics = 'enableNetworkAddressUsageMetrics' in response
    # if ii_enable_network_address_usage_metrics:
    #     ii_enable_network_address_usage_metrics = vpc_id == response['enableNetworkAddressUsageMetrics']['VpcId']
    ii_tags                                 = 'Tags' in response['vpc']
    
    ii_ipv6_ipam_pool_id                    = False
    ii_ipv6_netmask_length                  = False    
    ii_ipv6_cidr_block                      = False
    ii_assign_generated_ipv6_cidr_block     = False
    ii_ipv4_ipam_pool_id                    = False
    ii_ipv4_netmask_length                  = False

    # Include arguments if criteria is met   
    if ii_cidr_block:
        mapping['cidr_block']                           = response['vpc']['CidrBlock']    
    if ii_instance_tenancy:
        mapping['instance_tenancy']                     = response['vpc']['InstanceTenancy']
    if ii_enable_dns_support:
        mapping['enable_dns_support']                   = response['enableDnsSupport']['EnableDnsSupport']['Value']
    if ii_enable_dns_hostnames: 
        mapping['enable_dns_hostnames']                 = response['enableDnsHostnamespc']['EnableDnsHostnames']['Value']
    if ii_ipv4_ipam_pool_id:
        mapping['ipv4_ipam_pool_id' ]                   = init_val      
    if ii_ipv4_netmask_length:
        mapping['ipv4_netmask_length']                  = init_val     
    if ii_ipv6_ipam_pool_id:  
        mapping['ipv6_ipam_pool_id']                    = init_val
    if ii_ipv6_netmask_length:
        mapping['ipv6_netmask_length']                  = init_val
    if ii_ipv6_cidr_block: 
        mapping['ipv6_cidr_block']                      = init_val
    if ii_assign_generated_ipv6_cidr_block:
        mapping['assign_generated_ipv6_cidr_block']     = init_val        
    if ii_enable_network_address_usage_metrics:
        print(f'Be wary! enable_network_address_usage_metrics is hard coded to false due to boto3 response bug.') 
        # mapping['enable_network_address_usage_metrics'] = response['enableNetworkAddressUsageMetrics']['EnableNetworkAddressUsageMetrics']['Value']                                       
        mapping['enable_network_address_usage_metrics'] = 'false'                                    
    if ii_tags:
        tags = response['vpc']['Tags']
        tags_out = {}
        for jtag in tags:
            tags_out[jtag['Key']] = jtag['Value']
        mapping['tags']                                 = tags_out # Not sure why this is a list

    return mapping




