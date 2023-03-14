import boto3
from boto3_response import AWSResponse

def gen_vpc_tags(responses,tags):

    response = responses.ec2.create_tags(
            Resources=[
                responses.ami_id,
            ],
            Tags=tags
            )
    

def gen_instance_resp(responses):
    """"
    Creates ec2 instance response

    Inputs:
    None

    Outputs:
    instance reponse
    
    """

    # Create basic EC2 VPC through resource
    resp = responses.ec2.create_instances(ImageId=responses.ami_id,
                                InstanceType='t2.micro',
                                MinCount=1,
                                MaxCount=1)
    

def clean_instances(responses):
    """
    Tool to terminate all ec2 instances
    """

    resp = responses.ec2.describe_instances()
    for jres in resp['Reservations']:
        for jinst in jres['Instances']:
            id = jinst['InstanceId']
            responses.ec2.terminate_instances(
                InstanceIds=[id]
            )    

def main():
    """"
    Creates AWS environment using boto3

    Inputs:

    Outputs:
    boto3 reponse
    
    """

    responses = AWSResponse()
    responses.ami_id   = 'ami-005f9685cb30f234b'
    responses.region   = boto3.session.Session().region_name

    gen_vpc_tags(responses, [{'Key': 'Name','Value': 'Bob'}])

    responses.gen_vpc_resp()

    return responses

if __name__ == "__main__":

    # Assume path to boto3 input json is given as argument
    # boto3_json = sys.argv[0]
    main()
