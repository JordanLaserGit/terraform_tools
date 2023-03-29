import os, subprocess, re
from attributes import *

class TerraformFile():

    def __init__(self):
        self.terra_dir   = ''
        self.file_str    = ''
        self.config_file = ''
        self.attrs       = get_attrs()
        self.Blocks      = []  
        self.resources   = {}

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
        ii_route   = False
        ii_id      = False
        ii_ingress_egress = False
        for j in range(len(tf_lines)):
            line = tf_lines[j]
            split_eq   = line.split('=')
            split_brac = line.split('{')
            variable_name = split_eq[0].strip()
            context_name = split_brac[0].strip()

            ii_contains_pound            = line.find('#') >= 0
            ii_contains_only_right_brace = (line.find('}\n') >= 0 or line.find('},') >= 0) and not line.find('{}') >= 0
            ii_contains_only_left_brace  = line.find('{\n') >= 0 and not line.find('{}') >= 0
            ii_contains_right_bracket    = line.find(']\n') >= 0 and not line.find('[]') >= 0
            ii_lineskip_close_context    = line == '\n' or line == '}\n'

            # Exclude line         
            if ii_contains_pound:
                continue

            if not ii_list and ii_contains_right_bracket: 
                attrs = self.attrs['aws_route_table']  
                ii_route = False
                continue # Edge case to handle route formatting difference            

            if ii_context and not ii_list: 
                if ii_route:
                    if ii_contains_only_left_brace:
                        continue
                    elif ii_contains_only_right_brace:
                        out += '    }\n'
                        continue
                if not ii_skip:
                    if context in self.attrs.keys(): 
                        out = self.check_for_ref(out,line,resource_name, attrs)
                    else: # For contexts that don't have attributes filled out
                        out = self.check_for_ref(out,line,resource_name)
                    if line.find('= [\n') >= 0:
                        ii_list = True
                if ii_contains_only_right_brace:
                    ii_context = False  
                    ii_skip    = False
                    # Switch attrs back to resource attrs from context
                    if ii_ingress_egress:
                        attrs = self.attrs['aws_security_group']  
                        ii_ingress_egress = False 
                        ii_list = True                                 
                continue

            if ii_list:
                if ii_contains_right_bracket:
                    ii_list     = False  
                    ii_id       = False
                    out += line
                elif ii_id:
                    out = self.check_for_ref(out,line,resource_name,attrs) 
                else:
                    out += line
                continue

            if ii_lineskip_close_context:
                out += line
                continue
            
            # Set attrs
            if line.find('resource ') >= 0:
                split = line.split('\"')
                resource_type = split[1]
                resource_name = split[3]
                context = resource_type
                attrs = self.attrs[resource_type]                 
                out += line
                continue    

            if line.find('egress') >= 0 or line.find('ingress') >= 0:
                context = 'ingress/egress'
                attrs = self.attrs[context] 
                ii_list    = False
                ii_context = True
                ii_ingress_egress = True
                out += line
                continue    

            if line.find('route ') >= 0:
                context = 'route'
                attrs = self.attrs[context] 
                ii_list    = False
                ii_context = True
                ii_route   = True
                out += 'route {\n'
                continue         


            ii_in_attr = variable_name in attrs or context_name in attrs              

            # Within the resource. Decide to include attr
            if ii_contains_only_left_brace and not ii_ingress_egress and not ii_route:
                ii_context = True
                context = context_name
                if not ii_in_attr: 
                        ii_skip = True                  

            if ii_in_attr: # include only if in attrs                
                if line.find('= [\n') >= 0:
                    ii_list = True
                if line.find('_id') >= 0 or ii_id: # Opportunity to replace id with reference
                    if ii_list: # Sometimes the id's are in lists
                        ii_id = True
                        out += line
                    else:
                        out = self.check_for_ref(out,line,resource_name,attrs)                  
                else:
                    out += line
                
        self.file_str += out  
        self.write_file_str()  

    def check_for_ref(self,out,line,resource_name,attrs=None):
        """
        Often a variable can be replaced by a reference to a resource's variables. 
        Check to see if we should make that switch here

        Inputs:
        out  - string to be written to file
        line - current line of tf show
        resource_name - the current resource block the line is in

        Outputs:
        out - string to be written to file
        """ 
        ii_has_eq = line.find('=') >= 0
        if ii_has_eq:
            split_eq = line.split('=')
            if attrs is not None:
                if not split_eq[0].strip() in attrs: # Must be in attrs to be included
                    return out

        # Allow what we can reference
        if not line.find('_id') >= 0: # This isn't a line that we can reference            
            out += line
            return out

        # Pull id from line
        ii_list   = not ii_has_eq
        if ii_list: # We are inside a list of id's
            id = line.split('"')[1]        
        else:            
            id = split_eq[1][2:-2] # indexing is to leave off the _" and \n             

        if not id in self.resources.keys(): # We don't have a reference for this
            out += line
            return out
               
        # Find resrouce from id
        ref = self.resources[id][0]             
        ref_type = self.resources[id][1]
            
        if ref == resource_name: # within resource's own block, add the id verbatim
            out += line
        else: # outside of resource's own block, replace with reference
            if ii_list:
                out += f'{ref_type}.{ref}.id\n'   
            else:
                out += split_eq[0] + f'= {ref_type}.{ref}.id\n'

        return out                    


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
