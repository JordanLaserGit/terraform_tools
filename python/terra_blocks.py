from boto3_response import *

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

        for jtag in Response['tags']:
            if jtag['Key'] == 'Name':
                name = jtag['Value']
                break 
    
        self.block_str   = f'resource \"{resource}\" \"{name}\" {{ \n'
        if resource == 'aws_vpc':
            self.args = get_aws_vpc_mapping(Response)


############
# mapping #
############

"""
TEMPLATE

def get_<>_mapping(response):
    # Required arguments
    mapping_required = {
        arg0 : init_val
    },

    init_val = None

    # Optional arguments   
    mapping_optional = {} 

    # Conditions under which we want to include this arguement
    ii_arg1 = False
    ii_arg2 = False
    ii_arg3 = False

    # Where the valiable is accessed within the boto3 response
    arg1_map = init_val
    arg1_map = init_val
    arg3_map = init_val

        if ii_arg1:
            mapping_optional['arg1'] = arg1_map
        if ii_arg1:
            mapping_optional['arg2'] = arg2_map
        if ii_arg3:
            mapping_optional['arg3'] = arg3_map

"""

# aws_vpc
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc

def get_aws_vpc_mapping(response):

    init_val = None

    # Optional arguments   
    mapping = {} 

    # Conditions under which we want to include this arguement
    ii_cidr_block                           = True
    ii_assign_generated_ipv6_cidr_block     = False
    ii_instance_tenancy                     = False
    ii_enable_dns_support                   = False
    ii_enable_dns_hostnames                 = False
    ii_enable_classiclink                   = False
    ii_enable_classiclink_dns_support       = False
    ii_enable_network_address_usage_metrics = False
    ii_tags                                 = False
    
    ii_ipv6_ipam_pool_id                    = False
    ii_ipv6_netmask_length                  = False    
    ii_ipv6_cidr_block                      = False

    ii_ipv4_ipam_pool_id                    = False
    ii_ipv4_netmask_length                  = False
                    
    # Where the valiable is accessed within the boto3 response
    map_cidr_block                           = response['vpc']['CidrBlock']  
    map_assign_generated_ipv6_cidr_block     = init_val
    map_instance_tenancy                     = init_val # only options are 'default' and 'dedicated'
    map_enable_dns_support                   = init_val
    map_enable_dns_hostnames                 = init_val
    map_enable_classiclink                   = init_val
    map_enable_classiclink_dns_support       = init_val
    map_enable_network_address_usage_metrics = init_val
    map_tags                                 = response['tags']   

    map_ipv4_ipam_pool_id                    = init_val
    map_ipv4_netmask_length                  = init_val

    map_ipv6_cidr_block                      = init_val
    map_ipv6_ipam_pool_id                    = init_val
    map_ipv6_netmask_length                  = init_val    

    # Include arguments if criteria is met   
    if ii_cidr_block:
        mapping['cidr_block']                           = map_cidr_block    
    if ii_assign_generated_ipv6_cidr_block:
        mapping['assign_generated_ipv6_cidr_block']     = map_assign_generated_ipv6_cidr_block
    if ii_instance_tenancy:
        mapping['instance_tenancy']                     = map_instance_tenancy
    if ii_enable_dns_support:
        mapping['enable_dns_support']                   = map_enable_dns_support
    if ii_enable_dns_hostnames: 
        mapping['enable_dns_hostnames']                 = map_enable_dns_hostnames
    if ii_enable_classiclink:
        mapping['enable_classiclink']                   = map_enable_classiclink
    if ii_enable_classiclink_dns_support: 
        mapping['enable_classiclink_dns_support']       = map_enable_classiclink_dns_support          
    if ii_ipv4_ipam_pool_id:
        mapping['ipv4_ipam_pool_id' ]                   = map_ipv4_ipam_pool_id      
    if ii_ipv4_netmask_length:
        mapping['ipv4_netmask_length']                  = map_ipv4_netmask_length     
    if ii_ipv6_ipam_pool_id:  
        mapping['ipv6_ipam_pool_id']                    = map_ipv6_ipam_pool_id
    if ii_ipv6_netmask_length:
        mapping['ipv6_netmask_length']                  = map_ipv6_netmask_length
    if ii_ipv6_cidr_block: 
        mapping['ipv6_cidr_block']                      = map_ipv6_cidr_block
    if ii_enable_network_address_usage_metrics:
        mapping['enable_network_address_usage_metrics'] = map_enable_network_address_usage_metrics                                         
    if ii_tags:
        mapping['tags']                                 = map_tags

    return mapping



