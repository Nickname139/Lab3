import re
from datetime import datetime
from VehiclePass import VehiclePass
from Logger import Logger

class Bus(VehiclePass):
    def __init__(self, date, number, color, brand, passengers):
        self.logger = Logger()
        try:
            super().__init__(date, number, color, brand)
            
            if not isinstance(passengers, int) or passengers <= 0 or passengers > 200:
                self.logger.log_message("ERROR", f"Некорректное число пассажиров: {passengers}")
                raise ValueError("Количество пассажиров должно быть положительным целым числом (1-200)")
                
            if not self._validate_number(number):
                self.logger.log_message("ERROR", f"Неверный формат номера: {number}")
                raise ValueError(f"Неверный формат номера: {number}")

            self.passengers = passengers
            
        except Exception as e:
            self.logger.log_message("ERROR", f"Ошибка создания автобуса: {str(e)}")
            raise

    def _validate_number(self, number):
        pattern = r"^[АAВBЕEКKМMНHОOРPСCТTУYХX]{1}\d{3}[АAВBЕEКKМMНHОOРPСCТTУYХX]{2}\d{2,3}$"
        return re.match(pattern, number.upper()) is not None

    def __str__(self):
        return f"Bus({self.date.strftime('%d.%m.%Y')}, \"{self.number}\", \"{self.color}\", \"{self.brand}\", {self.passengers})"