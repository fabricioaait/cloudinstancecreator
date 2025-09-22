from .cloud_provider import CloudProvider

class AzureProvider(CloudProvider):
    """
    Implementation of CloudProvider for Azure.
    """
    def create_instance(self, instance_type: str) -> str:
        # Simulate creating an Azure instance
        instance_id = f"azure-instance-{instance_type}-{hash(instance_type)}"
        print(f"Created Azure instance: {instance_id}")
        return instance_id

    def delete_instance(self, instance_id: str) -> bool:
        # Simulate deleting an Azure instance
        print(f"Deleted Azure instance: {instance_id}")
        return True