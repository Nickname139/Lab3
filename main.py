import sys
import logging
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableView, QPushButton, QLineEdit, QDateEdit, QSpinBox,
                             QLabel, QMessageBox, QFileDialog, QComboBox)
from PyQt6.QtCore import QDate

from VehicleManager import VehicleManager
from VehicleTableModel import VehicleTableModel
from VehicleFileHandler import VehicleFileHandler

# Настройка логгера
logger = logging.getLogger("vehicle_app")
logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи в файл
file_handler = logging.FileHandler("vehicle_app.log", encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Создаем обработчик для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

class VehicleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Инициализация главного окна приложения")
        self.setWindowTitle("Система фиксации проезда")
        self.setGeometry(100, 100, 900, 600)

        self.__manager = VehicleManager()
        self.__file_handler = VehicleFileHandler()

        self.__init_ui()
        logger.info("Главное окно успешно инициализировано")

    def __init_ui(self):
        logger.debug("Начало инициализации UI")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Таблица для отображения данных
        self.__table_view = QTableView()
        self.__model = VehicleTableModel(self.__manager)
        self.__table_view.setModel(self.__model)
        layout.addWidget(self.__table_view)

        # Форма для ввода данных
        form_layout = QHBoxLayout()

        # Выбор типа ТС
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("Тип:"))
        self.__type_combo = QComboBox()
        self.__type_combo.addItems(["PersonalCar", "Truck", "Bus"])
        type_layout.addWidget(self.__type_combo)
        form_layout.addLayout(type_layout)

        # Поле для даты
        date_layout = QVBoxLayout()
        date_layout.addWidget(QLabel("Дата:"))
        self.__date_edit = QDateEdit(QDate.currentDate())
        date_layout.addWidget(self.__date_edit)
        form_layout.addLayout(date_layout)

        # Поле для номера
        number_layout = QVBoxLayout()
        number_layout.addWidget(QLabel("Номер:"))
        self.__number_edit = QLineEdit()
        self.__number_edit.setPlaceholderText("Пример: А123БВ777")
        number_layout.addWidget(self.__number_edit)
        form_layout.addLayout(number_layout)

        # Поле для цвета
        color_layout = QVBoxLayout()
        color_layout.addWidget(QLabel("Цвет:"))
        self.__color_edit = QLineEdit()
        self.__color_edit.setPlaceholderText("Допустимые цвета: Черный, Белый, Красный...")
        color_layout.addWidget(self.__color_edit)
        form_layout.addLayout(color_layout)

        # Поле для марки
        brand_layout = QVBoxLayout()
        brand_layout.addWidget(QLabel("Марка:"))
        self.__brand_edit = QLineEdit()
        self.__brand_edit.setPlaceholderText("Допустимые марки: Toyota, Volvo, Mercedes...")
        brand_layout.addWidget(self.__brand_edit)
        form_layout.addLayout(brand_layout)

        # Поле для характеристик (динамическое)
        self.__param_layout = QHBoxLayout()
        self.__update_param_field()
        form_layout.addLayout(self.__param_layout)

        # Кнопка добавления
        self.__add_btn = QPushButton("Добавить")
        self.__add_btn.clicked.connect(self.__add_vehicle)
        form_layout.addWidget(self.__add_btn)

        layout.addLayout(form_layout)

        # Панель кнопок управления
        btn_layout = QHBoxLayout()

        # Кнопка загрузки
        self.__load_btn = QPushButton("Загрузить")
        self.__load_btn.clicked.connect(self.__load_vehicles)
        btn_layout.addWidget(self.__load_btn)

        # Кнопка сохранения
        self.__save_btn = QPushButton("Сохранить")
        self.__save_btn.clicked.connect(self.__save_vehicles)
        btn_layout.addWidget(self.__save_btn)

        # Кнопка удаления
        self.__del_btn = QPushButton("Удалить")
        self.__del_btn.clicked.connect(self.__delete_vehicle)
        btn_layout.addWidget(self.__del_btn)

        layout.addLayout(btn_layout)

        # Обработчик изменения типа ТС
        self.__type_combo.currentTextChanged.connect(self.__update_param_field)
        logger.debug("Инициализация UI завершена")

    def __update_param_field(self):
        vehicle_type = self.__type_combo.currentText()
        logger.debug(f"Обновление поля параметров для типа: {vehicle_type}")

        # Очищаем предыдущие виджеты
        for i in reversed(range(self.__param_layout.count())):
            widget = self.__param_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        label = QLabel()
        field = QSpinBox()

        if vehicle_type == "PersonalCar":
            label.setText("Скорость (км/ч):")
            field.setRange(1, 300)
            field.setValue(90)
        elif vehicle_type == "Truck":
            label.setText("Вес (кг):")
            field.setRange(1000, 100000)
            field.setValue(5000)
        else:
            label.setText("Пассажиры:")
            field.setRange(1, 200)
            field.setValue(50)

        self.__param_layout.addWidget(label)
        self.__param_layout.addWidget(field)
        self.__param_field = field

    def __add_vehicle(self):
        try:
            logger.info("Попытка добавления нового транспортного средства")
            
            # Получаем данные из полей ввода
            number = self.__number_edit.text().strip()
            color = self.__color_edit.text().strip()
            brand = self.__brand_edit.text().strip()
            param = self.__param_field.value()
            vehicle_type = self.__type_combo.currentText()

            logger.debug(f"Введенные данные: Тип={vehicle_type}, Номер={number}, "
                        f"Цвет={color}, Марка={brand}, Параметр={param}")

            # Проверка заполненности обязательных полей
            if not all([number, color, brand]):
                logger.warning("Не все обязательные поля заполнены")
                raise ValueError("Заполните все обязательные поля")

            # Получаем дату
            try:
                date = self.__date_edit.date().toPyDateTime()
            except AttributeError:
                qdate = self.__date_edit.date()
                date = datetime(qdate.year(), qdate.month(), qdate.day())

            logger.debug(f"Дата: {date.strftime('%d.%m.%Y')}")

            # Создаем объект транспортного средства
            if vehicle_type == "PersonalCar":
                from PersonalCar import PersonalCar
                vehicle = PersonalCar(date, number, color, brand, param)
            elif vehicle_type == "Truck":
                from Truck import Truck
                vehicle = Truck(date, number, color, brand, param)
            else:
                from Bus import Bus
                vehicle = Bus(date, number, color, brand, param)

            # Добавляем в менеджер
            self.__manager.add_vehicle(vehicle)
            self.__model.layoutChanged.emit()

            # Очищаем поля ввода
            self.__number_edit.clear()
            self.__color_edit.clear()
            self.__brand_edit.clear()
            self.__param_field.setValue(0)

            logger.info(f"Успешно добавлен транспорт: {vehicle_type} {number}")

        except Exception as e:
            logger.error(f"Ошибка при добавлении транспорта: {str(e)}", exc_info=True)
            QMessageBox.warning(self, "Ошибка", str(e))

    def __delete_vehicle(self):
        index = self.__table_view.currentIndex()
        if not index.isValid():
            logger.warning("Попытка удаления без выбора элемента")
            QMessageBox.warning(self, "Ошибка", "Выберите транспорт для удаления")
            return

        reply = QMessageBox.question(
            self, "Подтверждение",
            "Удалить выбранный транспорт?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                vehicle = self.__manager.vehicles[index.row()]
                logger.info(f"Попытка удаления транспорта: {vehicle.number}")
                
                self.__manager.delete_vehicle(index.row())
                self.__model.layoutChanged.emit()
                
                logger.info(f"Транспорт успешно удален: {vehicle.number}")
            except Exception as e:
                logger.error(f"Ошибка при удалении транспорта: {str(e)}", exc_info=True)
                QMessageBox.warning(self, "Ошибка", str(e))

    def __save_vehicles(self):
        try:
            logger.info("Попытка сохранения данных")
            filename, _ = QFileDialog.getSaveFileName(
                self, "Сохранить файл", "", "Текстовые файлы (*.txt);;Все файлы (*)"
            )

            if filename:
                self.__file_handler.save_vehicles(self.__manager.vehicles, filename)
                QMessageBox.information(self, "Успех", "Данные сохранены")
                logger.info(f"Данные успешно сохранены в файл: {filename}")

        except Exception as e:
            logger.error(f"Ошибка при сохранении данных: {str(e)}", exc_info=True)
            QMessageBox.critical(self, "Ошибка", str(e))

    def __load_vehicles(self):
        try:
            logger.info("Попытка загрузки данных")
            path, _ = QFileDialog.getOpenFileName(
                self, "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*)"
            )
            
            if not path:
                logger.info("Загрузка отменена пользователем")
                return
            
            logger.debug(f"Выбран файл для загрузки: {path}")
            
            self.__manager.clear_vehicles()
            vehicles = self.__file_handler.load_vehicles(path)
            
            for vehicle in vehicles:
                self.__manager.add_vehicle(vehicle)
                
            self.__model.layoutChanged.emit()
            QMessageBox.information(self, "Успех", "Данные загружены")
            logger.info(f"Успешно загружено {len(vehicles)} транспортных средств из файла: {path}")
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке файла: {str(e)}", exc_info=True)
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке файла: {str(e)}")

if __name__ == "__main__":
    try:
        logger.info("Запуск приложения")
        app = QApplication(sys.argv)
        window = VehicleWindow()
        window.show()
        logger.info("Приложение успешно запущено")
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске приложения: {str(e)}", exc_info=True)
        QMessageBox.critical(None, "Ошибка", f"Не удалось запустить приложение: {str(e)}")