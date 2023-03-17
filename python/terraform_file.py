import os, subprocess

class TerraformFile():

    def __init__(self):
        self.file  = ''
        self.Blocks   = [] 

    def create_block_string(self):
        """
        Add dictionary to block string line by line
        """

        file_string = ''
        for jBlk in self.Blocks:
            depth = 0
            file_string += jBlk.block_str
            for key in jBlk.args:  
                val = jBlk.args[key]        

                if type(val) is not dict:
                    if val is True:  val = "true"
                    if val is False: val = "false"                    
                    file_string += f'{key}       = \"{val}\"\n'.rjust(2,' ')
                else:
                    depth += 1
                    file_string += f'{key}       = {{\n'.rjust(2,' ')
                    file_string = self.create_block_string(val,2+2*depth)
                    file_string += f'}}\n'
                    depth -= 1 

            file_string += f'}}\n'

        return file_string

    def write(self):

        file_string = self.create_block_string()

        with open(self.file,'w') as f:
            f.write(file_string)  

    def validate(self):

        # cd into where terraform is output
        dir = os.path.dirname(os.path.realpath(self.file))
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
