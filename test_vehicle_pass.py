import unittest
from datetime import datetime
from VehiclePass import VehiclePass
from PersonalCar import PersonalCar

class TestVehiclePass(unittest.TestCase):
    def test_valid_creation(self):
        date = datetime.now()
        car = PersonalCar(date, "A123BC", "Red", "Toyota", 120)
        self.assertEqual(car.number, "A123BC")
        
    def test_invalid_date_type(self):
        with self.assertRaises(TypeError):
            PersonalCar("2023-01-01", "A123BC", "Red", "Toyota", 120)
            
    def test_empty_number(self):
        with self.assertRaises(ValueError):
            PersonalCar(datetime.now(), "", "Red", "Toyota", 120)
            
    def test_invalid_color_type(self):
        with self.assertRaises(TypeError):
            PersonalCar(datetime.now(), "A123BC", 123, "Toyota", 120)

if __name__ == '__main__':
    unittest.main()