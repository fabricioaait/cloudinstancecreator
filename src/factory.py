import yaml
from .cloud_provider import CloudProvider
from .aws_provider import AWSProvider
from .azure_provider import AzureProvider

def get_provider(config_path: str = None, config: dict = None) -> CloudProvider:
    """
    Factory function to create a cloud provider based on YAML configuration.

    DRY (Don't Repeat Yourself): This factory centralizes the provider selection logic,
    avoiding repetition in client code. Clients don't need to know about specific provider classes.
    """
    if config_path:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    # config is now a dict
    provider_name = config['provider']
    if provider_name == 'aws':
        return AWSProvider(config)
    elif provider_name == 'azure':
        return AzureProvider(config)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")