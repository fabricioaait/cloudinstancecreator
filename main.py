#!/usr/bin/env python3

import yaml
from src.factory import get_provider

def main():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    provider_name = config['provider']
    quantity = config.get('quantity', 1)
    size = config.get('size', 't2.micro')
    if quantity != 1:
        raise ValueError("Quantity must be 1 for security reasons")
    provider = get_provider('config.yaml')
    instance_id = provider.create_instance(size)
    print(f"Created instance: {instance_id}")
    success = provider.delete_instance(instance_id)
    print(f"Deletion successful: {success}")

if __name__ == '__main__':
    main()