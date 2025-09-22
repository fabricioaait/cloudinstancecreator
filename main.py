#!/usr/bin/env python3

import yaml
from src.factory import get_provider

def main():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    instance_data = []
    for group_name, group in config['instance_groups'].items():
        provider = get_provider(config=group)
        for i in range(1, group['quantity'] + 1):
            name = group['name_pattern'].format(number=i)
            instance_id = provider.create_instance(group['size'], name)
            instance_data.append((provider, instance_id))
            print(f"Created instance: {name} ({instance_id})")
    for provider, instance_id in instance_data:
        success = provider.delete_instance(instance_id)
        print(f"Deletion successful for {instance_id}: {success}")

if __name__ == '__main__':
    main()