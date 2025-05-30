from Logger import Logger
from typing import List
from VehiclePass import VehiclePass

class VehicleManager:
    """Менеджер транспортных средств"""
    
    def __init__(self):
        self.__vehicles = []
        self.__logger = Logger()

    @property
    def vehicles(self) -> List[VehiclePass]:
        return self.__vehicles.copy()

    def add_vehicle(self, vehicle: VehiclePass) -> None:
        """Добавление транспортного средства с валидацией"""
        self._validate_vehicle(vehicle)
        self.__vehicles.append(vehicle)
        self.__logger.log_message("INFO", f"Добавлен {vehicle.__class__.__name__}: {vehicle.number}")

    def _validate_vehicle(self, vehicle):
        """Валидация перед добавлением"""
        if not isinstance(vehicle, VehiclePass):
            error_msg = f"Ожидается VehiclePass, получено {type(vehicle)}"
            self.__logger.log_message("ERROR", error_msg)
            raise TypeError(error_msg)

    def delete_vehicle(self, index: int) -> None:
        if not 0 <= index < len(self.__vehicles):
            raise IndexError("Неверный индекс для удаления")
        del self.__vehicles[index]

    def clear_vehicles(self) -> None:
        self.__vehicles = []