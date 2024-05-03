import datetime
import unittest

from entity.item_pack import ItemPack
from entity.material_pack import MaterialPack
from manager.shop_manager import ShopManager


class ShopManagerTest(unittest.TestCase):
    def setUp(self):
        self.shop_manager = ShopManager()
        self.shop_manager.filename = 'test_shop_inventory.json'

    def load_shop_default_inventory(self):
        # Modify the shop inventory
        self.shop_manager.add_material('Shop 2',
                                       'Pyrite 1',
                                       MaterialPack('Pyrite Ingot',
                                                    18,
                                                    16.13,
                                                    '2024-03-10',
                                                    16.13,
                                                    '2024-03-22')
                                       )
        self.shop_manager.add_material('Shop 2', 'Garcen 1',
                                       MaterialPack('Garcen Lubricant',
                                                    216,
                                                    58.57,
                                                    '2024-03-10')
                                       )
        self.shop_manager.add_item('Shop 3', 'Sollomate Opalo 1',
                                   ItemPack('Sollomate Opalo', 2.13, 1.13, '2024-03-10'))

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
        self.assertEqual(self.shop_manager.shop_inventory['Shop 2'].materials['Pyrite 1'].name, 'Pyrite Ingot')
        self.assertEqual(self.shop_manager.shop_inventory['Shop 2'].materials['Pyrite 1'].quantity, 18)
        self.assertEqual(self.shop_manager.shop_inventory['Shop 2'].materials['Pyrite 1'].price, 16.13)
        self.assertEqual(self.shop_manager.shop_inventory['Shop 2'].materials['Pyrite 1'].sold_date,
                         datetime.datetime.fromisoformat('2024-03-22'))


if __name__ == '__main__':
    unittest.main()
