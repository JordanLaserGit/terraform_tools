from boto3_response import *

class ProviderBlock():

    def __init__(self,Response):
        self.attrs = dict()

        profile = "default"
        region  = Response.region
        self.block_str  = f'provider "aws" {{\n  '
        self.block_str += f'profile = \"{profile}\"\n  '
        self.block_str += f'region  = \"{region}\"\n\n'

class ResourceBlock():

    def __init__(self, name, local_name):
        self.attrs       = dict()        
        self.block_str   = f'resource \"{local_name}\" \"{name}\" {{ \n'

class AWSVPC(ResourceBlock):  

    def __init__(self,Response,tags):
        
        self.response = Response
        self.attrs_required = {
            'cidr_block'                       :''
        }
        self.attrs_optional = {
            'arn'                              :'',
            'assign_generated_ipv6_cidr_block ':'',
            'id'                               :'',
            'instance_tenancy'                 :'',
            'enable_dns_support'               :'',
            'enable_dns_hostnames'             :'',
            'enable_classiclink'               :'',
            'enable_classiclink_dns_support'   :'',            
            'main_route_table_id'              :'',
            'default_network_acl_id'           :'',
            'default_security_group_id'        :'',
            'default_route_table_id'           :'',
            'ipv6_association_id'              :'',
            'ipv6_cidr_block'                  :'',
            'owner_id'                         :'',
            'tags_all'                         :'',
            'tags'                             :''
        }

        self.attrs_computed : dict

        for jtag in tags:
            if jtag['Key'] == 'Name':
                name = jtag['Value']
                break 

        self.Block  = ResourceBlock(name,'aws_vpc')

    def get_mapping(self,attr):
        """
        Mapping to where a terraform attribute can be found within the boto3 response

        attrs[attr] in the block class is set with the mapping based on the attr provided.
        """

        if attr == 'arn':
            mapping = '' # Boto3 response mapping
        elif attr ==  'assign_generated_ipv6_cidr_block':
            mapping = '' # Boto3 response mapping
        elif attr ==  'cidr_block':
            mapping =  self.response['CidrBlock']       
        elif attr ==  'id':
            mapping = '' # Boto3 response mapping
        elif attr ==  'instance_tenancy':
            mapping = '' # Boto3 response mapping
        elif attr ==  'enable_dns_support':
            mapping = ''
        elif attr ==  'enable_dns_hostnames':
            mapping = '' 
        elif attr ==  'enable_classiclink':
            mapping = ''                                                        
        elif attr ==  'enable_classiclink_dns_support':
            mapping = ''          
        elif attr ==  'main_route_table_id':
            mapping = '' 
        elif attr ==  'default_network_acl_id':
            mapping = '' 
        elif attr ==  'default_security_group_id':
            mapping = ''  
        elif attr ==  'default_route_table_id':
            mapping = ''     
        elif attr ==  'ipv6_association_id':
            mapping = ''  
        elif attr ==  'ipv6_cidr_block':
            mapping = ''
        elif attr ==  'owner_id':
            mapping = ''
        elif attr ==  'tags_all':
            mapping = ''
        elif attr ==  'tags':
            mapping = self.response['Tags']                                                
        else:
            raise Exception(f'{attr} not found in {self.resource} class!')

        self.Block.attrs[attr] = mapping

    def include_attrs(self):
        """
        Decide which attrs to include in the terraform block
        """

        for attr in self.attrs_required:
            self.get_mapping(attr)

        if False:
            self.get_mapping('arn')
        if False:
            self.get_mapping('assign_generated_ipv6_cidr_block')
        if False:
            self.get_mapping('id')
        if False:
            self.get_mapping('instance_tenancy')
        if False:
            self.get_mapping('enable_dns_support')
        if False:
            self.get_mapping('enable_dns_hostnames')                                                            
        if False:
            self.get_mapping('enable_classiclink')            
        if False:
            self.get_mapping('enable_classiclink_dns_support')
        if False:
            self.get_mapping('main_route_table_id')                        
        if False:
            self.get_mapping('default_network_acl_id')            
        if False:
            self.get_mapping('default_security_group_id')            
        if False:
            self.get_mapping('default_route_table_id')
        if False:
            self.get_mapping('ipv6_association_id')
        if False:
            self.get_mapping('ipv6_cidr_block')
        if False:
            self.get_mapping('owner_id')                                                
        if False:
            self.get_mapping('tags_all')
        if False:
            self.get_mapping('tags')


