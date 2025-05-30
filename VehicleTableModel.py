from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex

class VehicleTableModel(QAbstractTableModel):
    """Модель данных для отображения транспорта в таблице"""
    
    def __init__(self, manager, parent=None):
        super().__init__(parent)
        self.__manager = manager
        self.__headers = ["Дата", "Номер", "Цвет", "Марка", "Характеристика"]

    def rowCount(self, parent=None) -> int:
        return len(self.__manager.vehicles)

    def columnCount(self, parent=None) -> int:
        return len(self.__headers)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        
        vehicle = self.__manager.vehicles[index.row()]
        
        if index.column() == 0:
            return vehicle.pass_date.strftime("%d.%m.%Y")
        elif index.column() == 1:
            return vehicle.number
        elif index.column() == 2:
            return vehicle.color
        elif index.column() == 3:
            return vehicle.brand
        elif index.column() == 4:
            if hasattr(vehicle, 'speed'):
                return f"Скорость: {vehicle.speed} км/ч"
            elif hasattr(vehicle, 'weight'):
                return f"Вес: {vehicle.weight} кг"
            elif hasattr(vehicle, 'passengers'):
                return f"Пассажиры: {vehicle.passengers}"
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.__headers[section]
        return None