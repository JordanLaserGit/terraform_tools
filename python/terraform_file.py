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
        
        # Create the string that will be written to file
        # Algorithm is to 
        # 1) copy paste the show output 
        # 2) remove fields we don't want 
        # 3) make variable references where appropriate
        out = ''
        ii_tags = False
        for line in tf_lines:
            # Exclude line         
            if line.find('#') >= 0:
                continue

            # Include line
            if ii_tags: 
                if line .find('}') > 0:
                    ii_tags = False                    
                out += line
                continue
            if line == '\n' or line == '}\n':
                out += line
                pass
            if line.find('resource ') >= 0:
                split = line.split('\"')
                resource_type = split[1]
                resource_name = split[3]
                if resource_type == 'aws_vpc':
                    attrs = vpc_attrs
                elif resource_type == 'aws_subnet':
                    attrs = subnet_attrs
                out += line
                pass               

            split = line.split('=')
            if split[0].strip() in attrs: # include only if in attrs
                if split[0].strip() == 'tags': 
                    ii_tags = True
                if line.find('vpc_id') >= 0 and resource_type != 'aws_vpc': # replace with reference
                    out += split[0] + f'= aws_vpc.vpc0.id\n' #TODO unhard code this
                else:
                    out += line

        self.file_str += out  
        self.write_file_str()  

    def write_file_str(self):
        """
        Write the string created in state2config()
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
