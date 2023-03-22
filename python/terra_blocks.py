class ProviderBlock():

    def __init__(self,Response):
        self.args = dict()

        profile = "default"
        region  = Response.region
        self.block_str  = f'provider "aws" {{\n  '
        self.block_str += f'profile = \"{profile}\"\n  '
        self.block_str += f'region  = \"{region}\"\n\n'

class ResourceBlock():

    def __init__(self, resource, Response):        
    
        if resource == 'aws_vpc':
            self.args = get_aws_vpc_mapping(Response)
        else:
            raise Exception(f'{resource} is not within the built responses. Perhaps contact Jordan and ask him to build it.')
        
        try:
            name = self.args['tags']['Name']
        except:
            raise Exception('Resource needs \'Name\' as a tag')

        self.block_str   = f'resource \"{resource}\" \"{name}\" {{ \n'

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

# aws_vpc
def get_aws_vpc_mapping(response):

    init_val = None

    # Optional arguments   
    mapping = {} 

    vpc_id = response['vpc']['VpcId']

    # Conditions under which we want to include this arguement
    ii_cidr_block                           = 'CidrBlock' in response['vpc']
    ii_instance_tenancy                     = 'InstanceTenancy' in response['vpc']
    ii_enable_dns_support                   = 'enableDnsSupport' in response
    ii_enable_dns_hostnames                 = 'enableDnsHostnamespc' in response
    ii_enable_network_address_usage_metrics = 'enableNetworkAddressUsageMetrics' in response
    if ii_enable_network_address_usage_metrics:
        ii_enable_network_address_usage_metrics = vpc_id == response['enableNetworkAddressUsageMetrics']['VpcId']
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

# aws_vpc

def get_aws_vpc_mapping(response):

    init_val = None

    # Optional arguments   
    mapping = {} 

    vpc_id = response['vpc']['VpcId']

    # Conditions under which we want to include this arguement
    ii_cidr_block                           = 'CidrBlock' in response['vpc']
    ii_instance_tenancy                     = 'InstanceTenancy' in response['vpc']
    ii_enable_dns_support                   = 'enableDnsSupport' in response
    ii_enable_dns_hostnames                 = 'enableDnsHostnamespc' in response
    ii_enable_network_address_usage_metrics = 'enableNetworkAddressUsageMetrics' in response
    if ii_enable_network_address_usage_metrics:
        ii_enable_network_address_usage_metrics = vpc_id == response['enableNetworkAddressUsageMetrics']['VpcId']
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



