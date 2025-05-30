import os
import datetime

class Logger:
    """Класс для логирования в файлы"""
    
    def __init__(self):
        self.logs_dir = "Logs"
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

    def log_message(self, level: str, message: str) -> None:
        log_file = f"{self.logs_dir}/{datetime.datetime.now().strftime('%d-%m-%Y')}.log"
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        
        with open(log_file, 'a', encoding='utf-8') as file:
            file.write(f"{timestamp} {level} {message}\n")