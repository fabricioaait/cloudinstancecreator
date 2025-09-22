from abc import ABC, abstractmethod

class CloudProvider(ABC):
    """
    Abstract base class for cloud providers.
    Defines the interface for creating and deleting instances.

    SOLID Principles:
    - Single Responsibility (S): This class is responsible only for defining the cloud provider interface.
    - Open/Closed (O): The interface is open for extension (new providers can implement it) but closed for modification.
    - Liskov Substitution (L): Any subclass can be substituted for CloudProvider without affecting correctness.
    - Interface Segregation (I): The interface is minimal and focused on cloud instance management.
    - Dependency Inversion (D): High-level modules depend on this abstraction, not on concretions.
    """
    @abstractmethod
    def create_instance(self, instance_type: str) -> str:
        """
        Create a new instance of the given type.
        Returns the instance ID.
        """
        pass

    @abstractmethod
    def delete_instance(self, instance_id: str) -> bool:
        """
        Delete the instance with the given ID.
        Returns True if successful, False otherwise.
        """
        pass