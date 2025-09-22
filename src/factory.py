import yaml
from .cloud_provider import CloudProvider
from .aws_provider import AWSProvider
from .azure_provider import AzureProvider

def get_provider(config_path: str) -> CloudProvider:
    """
    Factory function to create a cloud provider based on YAML configuration.

    DRY (Don't Repeat Yourself): This factory centralizes the provider selection logic,
    avoiding repetition in client code. Clients don't need to know about specific provider classes.
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    provider_name = config['provider']
    if provider_name == 'aws':
        return AWSProvider()
    elif provider_name == 'azure':
        return AzureProvider()
    else:
        raise ValueError(f"Unknown provider: {provider_name}")