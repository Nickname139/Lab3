from datetime import datetime
from abc import ABC, abstractmethod
from Logger import Logger

class VehiclePass(ABC):
    """Базовый класс для всех транспортных средств"""
    
    VALID_COLORS = {
        "Черный", "Белый", "Красный", "Оранжевый", "Желтый",
        "Зеленый", "Голубой", "Синий", "Фиолетовый", "Коричневый",
        "Розовый", "Серый", "Серебристый", "Золотой", "Бежевый"
    }
    
    VALID_BRANDS = {
        "Toyota", "Volvo", "Mercedes", "Haval", "BMW", "Isuzu",
        "Audi", "Ford", "Chevrolet", "Hyundai", "Kia", "Nissan",
        "Mazda", "Lexus", "Honda", "Subaru", "Volkswagen", "Skoda",
        "Renault", "Peugeot", "Citroen", "Porsche", "Jeep", "Land Rover"
    }
    
    def __init__(self, date: datetime, number: str, color: str, brand: str):
        self.logger = Logger()
        
        try:
            if not isinstance(date, datetime):
                self.logger.log_message("ERROR", f"Некорректный тип даты: {type(date)}")
                raise TypeError("Дата должна быть типа datetime")
            
            if not isinstance(number, str) or not number.strip():
                self.logger.log_message("ERROR", f"Некорректный номер: '{number}'")
                raise TypeError("Номер должен быть непустой строкой")
                
            if not isinstance(color, str) or color.strip() not in self.VALID_COLORS:
                self.logger.log_message("ERROR", f"Недопустимый цвет: '{color}'")
                raise ValueError(f"Недопустимый цвет. Допустимые цвета: {', '.join(sorted(self.VALID_COLORS))}")
                
            if not isinstance(brand, str) or brand.strip() not in self.VALID_BRANDS:
                self.logger.log_message("ERROR", f"Недопустимая марка: '{brand}'")
                raise ValueError(f"Недопустимая марка. Допустимые марки: {', '.join(sorted(self.VALID_BRANDS))}")
                
            self.date = date
            self.number = number.strip().upper()
            self.color = color.strip()
            self.brand = brand.strip()
            
        except Exception as e:
            self.logger.log_message("ERROR", f"Ошибка создания транспортного средства: {str(e)}")
            raise

    @property
    def pass_date(self) -> datetime:
        return self.date

    @abstractmethod
    def __str__(self) -> str:
        pass