import boto3
import os
from .cloud_provider import CloudProvider

class AWSProvider(CloudProvider):
    """
    Implementation of CloudProvider for AWS using boto3.
    """
    def __init__(self, config: dict):
        super().__init__(config)
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.client = boto3.client('ec2', region_name=self.region)
        self.ami = self.config.get('ami', 'ami-0c02fb55956c7d316')

    def create_instance(self, instance_type: str, instance_name: str = None) -> str:
        tags = [{'Key': 'Name', 'Value': instance_name}] if instance_name else []
        response = self.client.run_instances(
            ImageId=self.ami,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': tags
            }]
        )
        instance_id = response['Instances'][0]['InstanceId']
        print(f"Created real AWS instance: {instance_id} with name: {instance_name}")
        return instance_id

    def delete_instance(self, instance_id: str) -> bool:
        self.client.terminate_instances(InstanceIds=[instance_id])
        print(f"Terminated AWS instance: {instance_id}")
        return True