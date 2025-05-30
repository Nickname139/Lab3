import unittest
from datetime import datetime
from VehicleManager import VehicleManager
from PersonalCar import PersonalCar
from Truck import Truck

class TestVehicleManager(unittest.TestCase):
    def setUp(self):
        self.manager = VehicleManager()
        self.car = PersonalCar(datetime.now(), "A123BC", "Red", "Toyota", 120)
        self.truck = Truck(datetime.now(), "X987YZ", "Blue", "Volvo", 5000)

    def test_add_valid_vehicle(self):
        self.manager.add_vehicle(self.car)
        self.assertEqual(len(self.manager.vehicles), 1)
        
    def test_add_invalid_type(self):
        with self.assertRaises(TypeError):
            self.manager.add_vehicle("Not a vehicle")
            
    def test_delete_valid_index(self):
        self.manager.add_vehicle(self.car)
        self.manager.delete_vehicle(0)
        self.assertEqual(len(self.manager.vehicles), 0)
        
    def test_delete_invalid_index(self):
        with self.assertRaises(IndexError):
            self.manager.delete_vehicle(0)

if __name__ == '__main__':
    unittest.main()