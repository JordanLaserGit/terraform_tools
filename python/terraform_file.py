import os, subprocess, re
from attributes import *

class TerraformFile():

    def __init__(self):
        self.terra_dir   = ''
        self.file_str    = ''
        self.config_file = ''
        self.attrs       = get_attrs()
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

     
        # Might need to add logic about rejecting or modifying attributes based on values imported

        # Only add if ipv6_address_count > 0
        if False:
            instance_attrs.append('ipv6_address_count','ipv6_addresses') 
        
        # Create the string that will be written to file
        # Algorithm is to 
        # 1) copy paste the show output 
        # 2) remove fields we don't want 
        # 3) make variable references where appropriate
        out = ''
        ii_context = False
        ii_list    = False
        ii_skip    = False
        ii_ingress_egress = False
        for j in range(len(tf_lines)):
            line = tf_lines[j]

            if j == 105:
                print()

            ii_contains_pound            = line.find('#') >= 0
            ii_contains_only_right_brace = (line.find('}\n') >= 0 or line.find('},') >= 0) and not line.find('{}') >= 0
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
                    if ii_ingress_egress:
                        attrs = self.attrs['aws_security_group']  
                        ii_ingress_egress = False 
                        ii_list = True               
                continue

            if ii_list:
                if ii_contains_right_bracket:
                    ii_list     = False     
                out += line
                continue

            # This is for skipping lines internal to a context that we want to leave out
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
                attrs = self.attrs[resource_type]                 
                out += line
                continue       

            if line.find('egress') >= 0 or line.find('ingress') >= 0:
                attrs = self.attrs['ingress/egress'] 
                ii_list    = False
                ii_context = True
                ii_ingress_egress = True
                out += line
                continue                

            # Within the resource. Decide to include attr
            split_eq   = line.split('=')
            split_brac = line.split('{')
            if ii_contains_only_left_brace and not ii_ingress_egress:
                ii_context = True
                if  not (split_eq[0].strip() in attrs or split_brac[0].strip() in attrs): 
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
