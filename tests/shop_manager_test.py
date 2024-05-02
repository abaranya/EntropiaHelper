import unittest
from manager.shop_manager import ShopManager

class ShopManagerTest(unittest.TestCase):
    def setUp(self):
        self.shop_manager = ShopManager()
        self.shop_manager.filename = 'test_shop_inventory.json'

    def load_shop_default_inventory(self):
        # Modify the shop inventory
        self.shop_manager.shop_inventory['Shop 2'].materials['Pyrite 1'] = {
            'name': 'Pyrite Ingot',
            'quantity': 18,
            'since_date': '2024-03-10',
            'price': 16.13,
            'sold_date': '2024-03-22'
        }
        self.shop_manager.shop_inventory['Shop 2'].materials['Garcen 1'] = {
            'name': 'Garcen Lubricant',
            'quantity': 216,
            'since_date': '2024-03-10',
            'price': 58.57,
            'sold_date': None
        }
    def test_load_save_shop_inventory(self):
        # Test loading the shop inventory from file
        self.shop_manager.load_shop_inventory()

        # Assert that the shop inventory was loaded successfully
        self.assertIsNotNone(self.shop_manager.shop_inventory)
        self.assertIn('Shop 2', self.shop_manager.shop_inventory)
        self.assertIn('Shop 3', self.shop_manager.shop_inventory)

        self.load_shop_default_inventory()

        # Save the modified shop inventory to file
        self.shop_manager.save_shop_inventory()

        # Reload the shop inventory from file
        self.shop_manager.load_shop_inventory()

        # Assert that the shop inventory was saved and reloaded successfully
        self.assertIn('Pyrite 1', self.shop_manager.shop_inventory['Shop 2'].materials)
        self.assertEqual(self.shop_manager.shop_inventory['Shop 2'].materials['Pyrite 1']['name'], 'Pyrite Ingot')
        self.assertEqual(self.shop_manager.shop_inventory['Shop 2'].materials['Pyrite 1']['quantity'], 18)
        self.assertEqual(self.shop_manager.shop_inventory['Shop 2'].materials['Pyrite 1']['price'], 16.13)
        self.assertEqual(self.shop_manager.shop_inventory['Shop 2'].materials['Pyrite 1']['sold_date'], '2024-03-22')

if __name__ == '__main__':
    unittest.main()