import re
from datetime import datetime
from VehiclePass import VehiclePass
from Logger import Logger

class PersonalCar(VehiclePass):
    def __init__(self, date, number, color, brand, speed):
        self.logger = Logger()
        try:
            super().__init__(date, number, color, brand)
            
            if not isinstance(speed, int) or speed <= 0 or speed > 300:
                self.logger.log_message("ERROR", f"Некорректная скорость: {speed}")
                raise ValueError("Скорость должна быть положительным целым числом (1-300 км/ч)")
                
            if not self._validate_number(number):
                self.logger.log_message("ERROR", f"Неверный формат номера: {number}")
                raise ValueError(f"Неверный формат номера: {number}")

            self.speed = speed
            
        except Exception as e:
            self.logger.log_message("ERROR", f"Ошибка создания легкового автомобиля: {str(e)}")
            raise

    def _validate_number(self, number):
        pattern = r"^[АAВBЕEКKМMНHОOРPСCТTУYХX]{1}\d{3}[АAВBЕEКKМMНHОOРPСCТTУYХX]{2}\d{2,3}$"
        return re.match(pattern, number.upper()) is not None

    def __str__(self):
        return f"PersonalCar({self.date.strftime('%d.%m.%Y')}, \"{self.number}\", \"{self.color}\", \"{self.brand}\", {self.speed})"