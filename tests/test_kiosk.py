import unittest
import json
import os
from datetime import datetime

# Импортируем классы из основного модуля
import sys
sys.path.append("..")
from kiosk import DataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_orders.json"
        self.dm = DataManager()
        self.dm.orders_file = self.test_file

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_order(self):
        order = {"id": 1, "date": "2026-06-18", "phone": "+79111234567", "total": 1000}
        self.dm.add_order(order)
        orders = self.dm.get_orders()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["id"], 1)

    def test_save_orders(self):
        self.dm.orders = [{"id": 2, "date": "2026-06-18", "total": 2000}]
        self.dm.save_orders()
        with open(self.test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 2)

if __name__ == "__main__":
    unittest.main()
