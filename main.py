#!/usr/bin/env python3

import yaml
from src.factory import get_provider

def main():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    provider_name = config['provider']
    name = config.get('name', 'default')
    size = config.get('size', 't2.micro')
    quantity = config.get('quantity', 1)
    if quantity < 1 or quantity > 5:  # Limit to 5 for safety
        raise ValueError("Quantity must be between 1 and 5")
    provider = get_provider('config.yaml')
    instance_ids = []
    for i in range(1, quantity + 1):
        instance_name = f"{provider_name}_instance_{name}_{i:02d}"
        instance_id = provider.create_instance(size, instance_name)
        instance_ids.append(instance_id)
        print(f"Created instance: {instance_name} ({instance_id})")
    for instance_id in instance_ids:
        success = provider.delete_instance(instance_id)
        print(f"Deletion successful for {instance_id}: {success}")

if __name__ == '__main__':
    main()