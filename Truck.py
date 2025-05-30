import re
from datetime import datetime
from VehiclePass import VehiclePass
from Logger import Logger

class Truck(VehiclePass):
    def __init__(self, date, number, color, brand, weight):
        self.logger = Logger()
        try:
            super().__init__(date, number, color, brand)
            
            if not isinstance(weight, int) or weight <= 0 or weight > 100000:
                self.logger.log_message("ERROR", f"Некорректный вес: {weight}")
                raise ValueError("Вес должен быть положительным целым числом (1-100000 кг)")
                
            if not self._validate_number(number):
                self.logger.log_message("ERROR", f"Неверный формат номера: {number}")
                raise ValueError(f"Неверный формат номера: {number}")

            self.weight = weight
            
        except Exception as e:
            self.logger.log_message("ERROR", f"Ошибка создания грузовика: {str(e)}")
            raise

    def _validate_number(self, number):
        pattern = r"^[АAВBЕEКKМMНHОOРPСCТTУYХX]{1}\d{3}[АAВBЕEКKМMНHОOРPСCТTУYХX]{2}\d{2,3}$"
        return re.match(pattern, number.upper()) is not None

    def __str__(self):
        return f"Truck({self.date.strftime('%d.%m.%Y')}, \"{self.number}\", \"{self.color}\", \"{self.brand}\", {self.weight})"