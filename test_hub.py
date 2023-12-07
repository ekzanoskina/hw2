import json
import unittest
from hub import Hub
from item import Item

class TestHub(unittest.TestCase):

    def setUp(self):
        self.hub = Hub()

    # def tearDown(self):
    #     self.hub.clear()
    def test_hub_singleton(self):
        'Проверка того что hub - синглтон'
        self.assertTrue(self.hub is Hub())

    def test_len(self):
        'Проверка того что при добавлении предметов меняется значение len(item)'
        for i in range(5):
            self.hub.add_item(Item())
        self.assertEqual(len(self.hub), 5)

    def test_get_item_by_index(self):
        'Проверка, что по объекту Hub можно итерироваться и брать i-ты элимент используя [i]'
        item = Item()
        self.hub.add_item(item)
        self.assertEqual(self.hub[0], item)

    def test_find_by_id(self):
        'Проверка получения позиции в списке _items и объекта Item по его id'
        item = Item()
        self.hub.add_item(item)
        self.hub.find_by_id(item._id)
        self.assertEqual(self.hub.find_by_id(item._id), (0, item))
        self.assertEqual(self.hub.find_by_id(-1), (-1, None))

    def test_find_by_tags(self):
        'Проверка нахождения items по тегам'
        tags = ['tag1', 'tag2']
        item1 = Item(tags=['tag1'])
        item2 = Item(tags=['tag1', 'tag2'])
        item3 = Item(tags=['tag3'])
        self.hub.add_items([item1, item2, item3])
        self.assertEqual(self.hub.find_by_tags(tags), [item2])

    def test_add_item_valid(self):
        'Проверка добавления тега валидного типа'
        item = Item()
        self.hub.add_item(item)
        self.assertEqual(len(self.hub._items), 1)


    def test_add_item_invalid(self):
        'Проверка возникновения ошибки при добавлении невалидного тега'
        item = "not an item"
        with self.assertRaises(TypeError):
            self.hub.add_item(item)

    def test_rm_item_by_object(self):
        'Проверка удаления item из _items объекта Hub'
        item = Item()
        self.hub.add_item(item)
        self.hub.rm_item(item)
        self.assertNotIn(item, self.hub._items)

    def test_rm_item_remove_by_id(self):
        'Проверка удаления item из _items объекта Hub по его id'
        item1 = Item()
        item2 = Item()
        self.hub.add_items([item1, item2])
        self.hub.rm_item(item1._id)
        self.assertNotIn(item1, self.hub._items)
        self.assertIn(item2, self.hub._items)

    def test_rm_item_invalid_argument_type(self):
        'Проверка возникновения ошибки при попытке удаления объекта невалидного типа'
        self.hub.add_item(Item())
        with self.assertRaises(TypeError):
            self.hub.rm_item('invalid')

    def tests_find_by_date_single_date(self):
        'Проверка возращения подходящих по дате items при передаче одной даты'

        item1 = Item()
        item2 = Item()
        item1.dispatch_date = '01.01.2000'
        item2.dispatch_date = '01.01.2002'
        self.hub.add_items([item1, item2])
        self.assertEqual(self.hub.find_by_date('01.01.2002'), [item1, item2])

    def tests_find_by_date_interval(self):
        'Проверка возращения подходящих по дате items при передаче интервала дат'
        item1 = Item(dispatch_date='01.01.2005')
        item2 = Item(dispatch_date='01.01.2002')
        self.hub.add_items([item1, item2])
        self.assertEqual(self.hub.find_by_date('01.01.2001', '01.01.2004'), [item2])

    def tests_find_by_date_too_many_parameters(self):
        'Проверка возникновения ошибки при передачи больше двух аргументов для поиска подходящих по дате items'
        item = Item()
        item.dispatch_date = '01.01.2002'
        self.hub.add_item(item)
        with self.assertRaises(ValueError):
            self.hub.find_by_date('01.01.2002', '01.01.2002', '01.01.2002')

    def test_find_most_valuable(self):
        'Проверка возвращения самых ценных items в кол-ве, не превышающем длину списка _items'
        item1 = Item(cost=25)
        item2 = Item(cost=50)
        item3 = Item(cost=70.6)
        self.hub.add_items([item1, item2, item3])
        self.assertEqual(self.hub.find_most_valuable(2), [item3, item2])

    def test_find_most_valuable_large_amount(self):
        'Проверка возвращения самых ценных items в кол-ве, превышающем длину списка _items'
        hub = Hub()
        item1 = Item(cost=25)
        item2 = Item(cost=50)
        item3 = Item(cost=70.6)
        self.hub.add_items([item1, item2, item3])
        self.assertEqual(self.hub.find_most_valuable(5), [item3, item2, item1])

    def test_save_as_json_hub_object(self):
        'Проверка сохранения экземляра Hub в json файл'
        hub = Hub('hub1')
        self.hub.save_as_json()
        with open(f'hub_{hub._hub}.json', 'r') as f:
            data = json.load(f)
            self.assertEqual(data, self.hub.__dict__)

    def test_read_from_json(self):
        'Проверка создания одного экземпляра класса Hub из json файла'
        json_item = Hub().read_from_json('test_hub.json')
        self.assertEqual(json_item._hub, "hub1")
        self.assertEqual(json_item._hdate, "01.02.2023")
        self.assertEqual(json_item._items, [])


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)