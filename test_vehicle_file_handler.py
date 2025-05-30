import unittest
import os
from datetime import datetime
from VehicleFileHandler import VehicleFileHandler

class TestVehicleFileHandler(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_vehicles.txt"
        with open(self.test_file, "w") as f:
            f.write('PersonalCar(15.05.2023, "A123BC", "Red", "Toyota", 120)\n')
            f.write('Truck(16.05.2023, "X987YZ", "Blue", "Volvo", 5000)\n')
        
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
            
    def test_load_valid_file(self):
        vehicles = VehicleFileHandler.load_vehicles(self.test_file)
        self.assertEqual(len(vehicles), 2)
        
    def test_load_invalid_file(self):
        with self.assertRaises(IOError):
            VehicleFileHandler.load_vehicles("nonexistent_file.txt")
            
    def test_load_invalid_format(self):
        with open("invalid.txt", "w") as f:
            f.write("Invalid data format")
        with self.assertRaises(ValueError):
            VehicleFileHandler.load_vehicles("invalid.txt")
        os.remove("invalid.txt")

if __name__ == '__main__':
    unittest.main()