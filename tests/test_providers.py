import unittest
from unittest.mock import patch, MagicMock
from src.factory import get_provider
from src.aws_provider import AWSProvider
from src.azure_provider import AzureProvider

class TestProviders(unittest.TestCase):
    @patch('boto3.client')
    def test_factory_aws(self, mock_boto3):
        mock_client = MagicMock()
        mock_boto3.return_value = mock_client
        mock_client.run_instances.return_value = {'Instances': [{'InstanceId': 'i-123456'}]}
        provider = get_provider('tests/test_config_aws.yaml')
        self.assertIsInstance(provider, AWSProvider)
        instance_id = provider.create_instance('t2.micro', 'aws_instance_prod_01')
        self.assertEqual(instance_id, 'i-123456')
        mock_client.run_instances.assert_called_once()
        success = provider.delete_instance(instance_id)
        self.assertTrue(success)
        mock_client.terminate_instances.assert_called_once_with(InstanceIds=['i-123456'])

    def test_factory_azure(self):
        provider = get_provider('tests/test_config_azure.yaml')
        self.assertIsInstance(provider, AzureProvider)
        instance_id = provider.create_instance('Standard_B1s', 'azure_instance_prod_01')
        self.assertIn('azure-instance', instance_id)
        success = provider.delete_instance(instance_id)
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()