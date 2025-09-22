#!/usr/bin/env python3

import yaml
from src.factory import get_provider

def main():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    instance_data = []
    for group_name, group in config['instance_groups'].items():
        provider = get_provider(config=group)
        quantity = group.get('quantity', 1)
        if quantity < 0 or quantity > 5:  # Allow 0 for delete mode
            raise ValueError("Quantity must be between 0 and 5")
        group_instances = []
        if quantity > 0:
            for i in range(1, quantity + 1):
                name = group['name_pattern'].format(number=i)
                instance_id = provider.create_instance(group['size'], name)
                group_instances.append(instance_id)
                print(f"Created instance: {name} ({instance_id})")
        # Delete specified ids if any
        delete_ids = group.get('delete_ids', [])
        for instance_id in delete_ids:
            success = provider.delete_instance(instance_id)
            print(f"Deleted instance: {instance_id}, success: {success}")
        # Decide whether to clean up this group's instances
        cleanup = group.get('cleanup', True)
        if cleanup:
            for instance_id in group_instances:
                success = provider.delete_instance(instance_id)
                print(f"Deletion successful for {instance_id}: {success}")
        else:
            print(f"Keeping instances for group {group_name}: {group_instances}")
            instance_data.extend([(provider, instance_id) for instance_id in group_instances])  # In case of global cleanup, but for now, per group

if __name__ == '__main__':
    main()