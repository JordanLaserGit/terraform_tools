import os, subprocess, re

class TerraformFile():

    def __init__(self):
        self.terra_dir  = ''
        self.file_str    = ''
        self.config_file = ''
        self.Blocks      = []  

    def set_wdir(self,terra_dir):
        if not os.path.exists(terra_dir):
            os.mkdir(terra_dir) 
        self.terra_dir = terra_dir
      
    def create_block_string(self,jBlk,depth=0):
        """
        Add dictionary to block string line by line
        """
        if type(jBlk) is dict:
            file_string = ''
            dict_loop = jBlk
        else:
            file_string = jBlk.block_str
            dict_loop = jBlk.args
        for key in dict_loop:  
            val = dict_loop[key]        

            if type(val) is not dict:
                if val is True:  val = "true"
                if val is False: val = "false"  
                if val[:3] == 'VAR': # code to recognize when val is a terraform variable reference
                    file_string += f'{key}       = {val[3:]}\n'.rjust(2,' ')
                else:
                    file_string += f'{key}       = \"{val}\"\n'.rjust(2,' ')
            else:
                depth += 1
                file_string += f'{key}       = {{\n'.rjust(2,' ')
                file_string += self.create_block_string(val,2+2*depth)
                file_string += f'}}\n'
                depth -= 1         

        return file_string

    def write(self):
        """
        Creates terraform file string and writes it to file
        """

        file_string = ''
        for jBlk in self.Blocks:
            file_string += self.create_block_string(jBlk)
            file_string += f'}}\n\n'

        with open(self.config_file,'w') as f:
            f.write(file_string)  

    def append_file(self):
        """
        Creates terraform file string and appends it to file
        """

        file_string = ''
        for jBlk in self.Blocks:
            file_string += self.create_block_string(jBlk)
            file_string += f'}}\n\n'

        with open(self.config_file,'a') as f:
            f.write(file_string)   

    def show2config(self):
        """
        Convert terraform show output into terraform config
        """

        # Terraform show to help build the config
        process = subprocess.Popen(["terraform","show"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        tf_str = out.decode()
        escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        tf_str = escape.sub('',tf_str)

        show = os.path.join(self.terra_dir,'tf_show.txt')

        with open(show,'w') as f:
            f.write(tf_str)

        with open(show,'r') as f:
            tf_lines = f.readlines()

        # Need to add: 
        vpc_attrs = [
            'cidr_block',
            'instance_tenancy',
            'enable_dns_support',
            'enable_dns_hostnames',
            'enable_network_address_usage_metrics',
            'tags',
            'ipv6_cidr_block',
            'assign_generated_ipv6_cidr_block',
            'ipv4_ipam_pool_id',
            'ipv4_netmask_length'
            ]
        
        subnet_attrs = [
            'availability_zone',
            'map_public_ip_on_launch',
            'cidr_block',
            'default_for_az',
            'filter',
            'ipv6_cidr_block',
            'state',
            'tags',
            'vpc_id'
            ]       
         
        instance_attrs = [
            'ami',
            'associate_public_ip_address',
            'availability_zone',
            'capacity_reservation_specification',
            'cpu_core_count',
            'cpu_threads_per_core',
            'credit_specification',
            'disable_api_stop',
            'disable_api_termination',
            'ebs_block_device',
            'ebs_optimized',
            'enclave_options',
            'ephemeral_block_device',
            'get_password_data',
            'hibernation',
            'host_id',
            'host_resource_group_arn',
            'iam_instance_profile',
            'instance_initiated_shutdown_behavior',
            'instance_type',
            'key_name',
            'launch_template',
            'maintenance_options',
            'metadata_options',
            'monitoring',
            'network_interface',
            'placement_group',
            'placement_partition_number',
            'private_dns_name_options',
            'private_ip',
            'secondary_private_ips',
            'security_groups',
            'subnet_id',
            'tags',
            'tenancy',
            'vpc_security_group_ids'
            ]  

        # Only add if ipv6_address_count > 0
        if False:
            instance_attrs.append('ipv6_address_count','ipv6_addresses')

        # List of attributes that are contexts (braced attributes)
        contexts = ['capacity_reservation_specification',
                    'credit_specification',
                    'enclave_options',
                    'maintenance_options',
                    'metadata_options',
                    'private_dns_name_options',
                    'tags'
                    ]       
        
        # Create the string that will be written to file
        # Algorithm is to 
        # 1) copy paste the show output 
        # 2) remove fields we don't want 
        # 3) make variable references where appropriate
        out = ''
        ii_context = False
        ii_list    = False
        ii_skip    = False
        for j in range(len(tf_lines)):
            line = tf_lines[j]

            ii_contains_pound            = line.find('#') >= 0
            ii_contains_only_right_brace = line.find('}\n') >= 0 and not line.find('{}') >= 0
            ii_contains_only_left_brace  = line.find('{\n') >= 0 and not line.find('{}') >= 0
            ii_contains_right_bracket    = line.find(']\n') >= 0
            ii_lineskip_close_context    = line == '\n' or line == '}\n'

            # Exclude line         
            if ii_contains_pound:
                continue

            # Include line
            if ii_context: 
                if not ii_skip:
                    out += line
                if ii_contains_only_right_brace:
                    ii_context = False  
                    ii_skip    = False                  
                continue

            if ii_list:
                if ii_contains_right_bracket:
                    ii_list = False  
                out += line
                continue

            if ii_skip:
                continue

            if ii_lineskip_close_context:
                out += line
                continue
            
            # New resource, set attrs and add line
            if line.find('resource ') >= 0:
                split = line.split('\"')
                resource_type = split[1]
                resource_name = split[3]
                if resource_type == 'aws_vpc':
                    attrs = vpc_attrs
                elif resource_type == 'aws_subnet':
                    attrs = subnet_attrs
                elif resource_type == 'aws_instance':
                    attrs = instance_attrs                    
                out += line
                continue               

            # Within the resource. Decide to include attr
            split_eq = line.split('=')
            split_brac = line.split('{')
            if ii_contains_only_left_brace:
                ii_context = True
                if  not (split_eq[0].strip() in contexts or split_brac[0].strip() in contexts): 
                        ii_skip = True                  

            if split_eq[0].strip() in attrs or split_brac[0].strip() in attrs: # include only if in attrs                
                if line.find('= [\n') >= 0:
                    ii_list = True
                if line.find('vpc_id') >= 0 and resource_type != 'aws_vpc': # replace with reference
                    out += split_eq[0] + f'= aws_vpc.vpc0.id\n' #TODO unhard code this
                else:
                    out += line
                

        self.file_str += out  
        self.write_file_str()  

    def write_file_str(self):
        """
        Write the string created in show2config()
        """
        with open(self.config_file,'w') as f:
            f.write(self.file_str)  

    def validate(self):
        """
        Validates that the automated terraform file builds the existing architecture
        """

        # cd into where terraform is output
        dir = os.path.dirname(os.path.realpath(self.config_file))
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
