from Logger import Logger
import datetime

class VehicleFileHandler:
    """Обработчик файлов транспортных данных"""
    
    @staticmethod
    def load_vehicles(filename: str):
        """Загрузка данных из файла с обработкой ошибок"""
        vehicles = []
        logger = Logger()
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    try:
                        line = line.strip()
                        if not line:
                            continue
                            
                        if '(' not in line or not line.endswith(')'):
                            raise ValueError("Некорректный формат строки")
                            
                        vehicle_type, params = line.split('(', 1)
                        params = params.rstrip(')').split(', ')
                        
                        if len(params) != 5:
                            raise ValueError("Неверное количество параметров")
                            
                        date = datetime.datetime.strptime(params[0], "%d.%m.%Y")
                        number = params[1].strip('"')
                        color = params[2].strip('"')
                        brand = params[3].strip('"')
                        param = int(params[4])
                            
                        if vehicle_type == "PersonalCar":
                            from PersonalCar import PersonalCar
                            vehicles.append(PersonalCar(date, number, color, brand, param))
                        elif vehicle_type == "Truck":
                            from Truck import Truck
                            vehicles.append(Truck(date, number, color, brand, param))
                        elif vehicle_type == "Bus":
                            from Bus import Bus
                            vehicles.append(Bus(date, number, color, brand, param))
                        else:
                            raise ValueError(f"Неизвестный тип транспорта: {vehicle_type}")
                            
                    except Exception as e:
                        logger.log_message("ERROR", f"Строка {line_num}: {str(e)} | Содержимое: {line}")
                        continue
                        
        except Exception as e:
            logger.log_message("ERROR", f"Ошибка чтения файла: {str(e)}")
            raise
            
        return vehicles

    @staticmethod
    def save_vehicles(vehicles: list, filename: str) -> None:
        """Сохранение данных в файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for vehicle in vehicles:
                    file.write(str(vehicle) + "\n")
        except Exception as e:
            Logger().log_message("ERROR", f"Ошибка сохранения: {str(e)}")
            raise