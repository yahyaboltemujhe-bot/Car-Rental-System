from abc import ABC, abstractmethod

class VehicleFactory(ABC):

    @abstractmethod
    def create_car(self):
        pass

    @abstractmethod
    def create_tracker(self):
        pass

    @abstractmethod
    def create_access_system(self):
        pass

    @abstractmethod
    def create_maintenance_profile(self):
        pass
