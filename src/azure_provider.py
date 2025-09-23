import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from .cloud_provider import CloudProvider

class AzureProvider(CloudProvider):
    """
    Implementation of CloudProvider for Azure using Azure SDK.
    """
    def __init__(self, config: dict):
        super().__init__(config)
        self.image = self.config.get('image', 'Ubuntu2204')
        credential = DefaultAzureCredential()
        self.subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
        self.resource_client = ResourceManagementClient(credential, self.subscription_id)
        self.compute_client = ComputeManagementClient(credential, self.subscription_id)
        self.network_client = NetworkManagementClient(credential, self.subscription_id)
        self.resource_group = os.getenv('AZURE_RESOURCE_GROUP')
        self.location = os.getenv('AZURE_LOCATION')

    def create_instance(self, instance_type: str, instance_name: str = None) -> str:
        # Create resource group if not exists
        self.resource_client.resource_groups.create_or_update(
            self.resource_group, {'location': self.location}
        )

        # Create VNet
        vnet_name = f"{instance_name}-vnet"
        self.network_client.virtual_networks.begin_create_or_update(
            self.resource_group, vnet_name,
            {
                'location': self.location,
                'address_space': {'address_prefixes': ['10.0.0.0/16']}
            }
        ).result()

        # Create Subnet
        subnet_name = f"{instance_name}-subnet"
        subnet = self.network_client.subnets.begin_create_or_update(
            self.resource_group, vnet_name, subnet_name,
            {'address_prefix': '10.0.0.0/24'}
        ).result()

        # Create NIC
        nic_name = f"{instance_name}-nic"
        nic = self.network_client.network_interfaces.begin_create_or_update(
            self.resource_group, nic_name,
            {
                'location': self.location,
                'ip_configurations': [{
                    'name': 'ipconfig1',
                    'subnet': {'id': subnet.id}
                }]
            }
        ).result()

        # Resolve image reference (robust lookup) and create VM
        image_ref = self._resolve_image_reference()

        vm = self.compute_client.virtual_machines.begin_create_or_update(
            self.resource_group, instance_name,
            {
                'location': self.location,
                'hardware_profile': {'vm_size': instance_type},
                'storage_profile': {
                    'image_reference': image_ref
                },
                'os_profile': {
                    'computer_name': instance_name,
                    'admin_username': 'azureuser',
                    'admin_password': 'P@ssw0rd123!'
                },
                'network_profile': {
                    'network_interfaces': [{
                        'id': nic.id
                    }]
                }
            }
        ).result()

        print(f"Created real Azure VM: {vm.name}")
        return vm.name

    def delete_instance(self, instance_id: str) -> bool:
        self.compute_client.virtual_machines.begin_delete(self.resource_group, instance_id).result()
        print(f"Deleted Azure VM: {instance_id}")
        return True

    def _resolve_image_reference(self):
        # Attempt to find a valid image reference for the configured image name.
        # Support explicit 'Offer:SKU' syntax in `self.image`, e.g. 'UbuntuServer:18.10'
        if self.image and ':' in self.image:
            parts = self.image.split(':', 1)
            offer = parts[0]
            sku = parts[1]
            publisher = 'Canonical'
            try:
                versions = list(self.compute_client.virtual_machine_images.list(self.location, publisher, offer, sku))
                version = versions[0].name if versions else 'latest'
            except Exception:
                version = 'latest'
            return {
                'publisher': publisher,
                'offer': offer,
                'sku': sku,
                'version': version
            }

        # Supports simple names like 'Ubuntu2204' or full offers.
        # Strategy:
        # 1. List offers for the Canonical publisher in the region.
        # 2. Pick an offer that matches `self.image` (fuzzy) or contains 'ubuntu'.
        # 3. List SKUs for the chosen offer and pick the first available.
        # 4. List versions for the SKU and pick the newest available.
        publisher = 'Canonical'
        target = (self.image or 'ubuntu').lower()

        try:
            offers = list(self.compute_client.virtual_machine_images.list_offers(self.location, publisher))
            chosen_offer = None
            for o in offers:
                name = (o.name or '').lower()
                if target in name:
                    chosen_offer = o.name
                    break

            if not chosen_offer:
                # prefer any offer with 'ubuntu' in the name
                for o in offers:
                    if 'ubuntu' in (o.name or '').lower():
                        chosen_offer = o.name
                        break

            if not chosen_offer and offers:
                chosen_offer = offers[0].name

            if not chosen_offer:
                # fallback to known offer name
                chosen_offer = 'UbuntuServer'

            # pick a SKU
            skus = list(self.compute_client.virtual_machine_images.list_skus(self.location, publisher, chosen_offer))
            sku = skus[0].name if skus else '22_04-lts'

            # pick a version
            versions = list(self.compute_client.virtual_machine_images.list(self.location, publisher, chosen_offer, sku))
            version = versions[0].name if versions else 'latest'

            return {
                'publisher': publisher,
                'offer': chosen_offer,
                'sku': sku,
                'version': version
            }
        except Exception:
            # Conservative fallback
            return {
                'publisher': publisher,
                'offer': 'UbuntuServer',
                'sku': '18.04-LTS',
                'version': 'latest'
            }