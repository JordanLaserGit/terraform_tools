import os, subprocess

class TerraformFile():

    def __init__(self):
        self.config_file = ''
        self.Blocks   = [] 

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

    def state2config(self):
        pass


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
