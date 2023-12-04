import json
import unittest
from item import Item
from datetime import datetime
from hub import Hub

class TestItem(unittest.TestCase):
    def test_item_id(self):
        'Проверка того что у разных Items разные id'
        i1 = Item()
        i2 = Item()
        self.assertFalse(i1._id == i2._id)

    def test_len(self):
        'Проверка того что при добавлении тэгов меняется значение len(item)'
        it = Item()
        tags = ['Свежий', 'Сочный', 'Из Африки', 'Скоропортящийся', "Содержит витамин C"]
        for i in range(5):
            it.add_tag(tags[i])
        self.assertEqual(len(it), 5)

    def test_equal_tags(self):
        'Проверка того что, если к предмету добавить два идентичных тега - их колчество будет один'
        it = Item()
        for i in range(3):
            it.add_tag('Большой')
        self.assertEqual(len(it), 1)

    def test_set_get_cost(self):
        'Проверка работы декоратора property для установки и чтения атрибута _cost'
        item = Item()
        item.cost = 24
        self.assertEqual(item.cost, 24)

    def test_lt_same_type_int(self):
        'Проверка сравнения объектов Item по цене, когда оба значения int'
        item1 = Item(cost=5)
        item2 = Item(cost=10)
        self.assertTrue(item1 < item2)

    def test_lt_same_type_float(self):
        'Проверка сравнения объектов Item по цене, когда оба значения float'
        item1 = Item(cost=5.5)
        item2 = Item(cost=10.5)
        self.assertTrue(item1 < item2)

    def test_lt_different_type(self):
        'Проверка возникновения ошибки при сравнении объекта Item с объектом другого типа'
        item1 = Item(cost=5)
        item2 = "10"
        self.assertRaises(TypeError, item1 < item2)

    def test_lt_same_type_str(self):
        'Проверка возникновения ошибки при сравнение объектов Item с неверным типом данным у _cost'
        item1 = Item(cost="apple")
        item2 = Item(cost="banana")
        self.assertRaises(TypeError, item1 < item2)

    def test_add_tags(self):
        'Проверка добавление контейнера тегов в объект Item'
        item = Item()
        item.add_tags(['tag1', 'tag2'])
        self.assertEqual(item._tags, ['tag1', 'tag2'])

    def test_add_tags_duplicate(self):
        'Проверка недобавления одинаковых тегов в объект Item'
        item = Item()
        item.add_tags(['tag1', 'tag2'])
        item.add_tags(['tag2', 'tag3'])
        self.assertEqual(item._tags, ['tag1', 'tag2', 'tag3'])

    def test_remove_tags(self):
        'Проверка удаления тегов'
        item = Item()
        item.add_tags(['tag1', 'tag2', 'tag3'])
        item.remove_tags(['tag1', 'tag2'])
        self.assertEqual(item._tags, ['tag3'])

    def test_remove_tags_not_in_list(self):
        'Проверка, что при передачи тегов, которых нет в _tags, _tags останется неизменным'
        item = Item()
        item.add_tags(['tag1', 'tag2', 'tag3'])
        item.remove_tags(['tag4', 'tag5'])
        self.assertEqual(item._tags, ['tag1', 'tag2', 'tag3'])

    def test_is_tagged_str(self):
        'Проверка наличия одного тега у объекта Item'
        item = Item()
        item.add_tags(['tag1', 'tag2', 'tag3'])
        self.assertTrue(item.is_tagged('tag1')) # если тег есть у объекта Item
        self.assertFalse(item.is_tagged('tag4')) # если тега нет у объекта Item
        self.assertFalse(item.is_tagged('')) # в качестве аргумента передана пустая строка

    def test_is_tagged_container(self):
        'Проверка наличия всех тегов контейнера у объекта Item'
        item = Item()
        item.add_tags(['tag1', 'tag2', 'tag3'])
        self.assertTrue(item.is_tagged(['tag1', 'tag2']))  # если теги есть у объекта Item
        self.assertFalse(item.is_tagged(['tag5', 'tag4']))  # если тегов нет у объекта Item
        self.assertFalse(item.is_tagged(['tag5', 'tag1']))  # часть тегов есть у объекта Item, часть - нет

    def test_copy(self):
        'Проверка создания копии объекта Item с другим id'
        item = Item(name="item", description="description", dispatch_date="01.02.2022", tags=["tag1", "tag2"], cost=10)
        copy_item = item.copy()

        # тестируем каждый аттрибут по отдельности
        self.assertEqual(copy_item._name, "item")
        self.assertEqual(copy_item._description, "description")
        self.assertEqual(copy_item._dispatch_date, '01.02.2022')
        self.assertEqual(copy_item._tags, ["tag1", "tag2"])
        self.assertEqual(copy_item._cost, 10)

        # тестируем, что если изменить список тегов у экземляра, у копии он не изменится
        item._tags[0] = 'no_tag'
        self.assertEqual(copy_item._tags, ["tag1", "tag2"])

    def test_create_from_json(self):
        json_item = Item().create_from_json('test.json')
        self.assertEqual(json_item._name, "item")
        self.assertEqual(json_item._description, "description")
        self.assertEqual(json_item._dispatch_date, '01.02.2022')
        self.assertEqual(json_item._tags, ["tag1", "tag2"])
        self.assertEqual(json_item._cost, 10)


    def test_hash(self):
        'Проверка, что hash вычисляется по нужному полю'
        item1 = Item()
        self.assertEqual(hash(item1), hash(item1._id))

    def test_eq(self):
        'Проверка, что два разных объекта не равны'
        item1 = Item()
        item2 = Item()
        self.assertNotEqual(item1, item2)

    def test_eq_invalid_type(self):
        'Проверка возникновения ошибки при попытке сравнения на равество объектов разных типов'
        item1 = Item()
        item2 = item1._id # int type
        self.assertRaises(TypeError, item1 == item2)

    def tests_get_item_by_id(self):
        "Проверка получения объекта Item по его id в списке _items при использовании метода"
        item1 = Item()
        self.assertEqual(Item.get_item_by_id(item1._id), item1)

    def tests_get_item_by_id_invalid_type(self):
        'Проверка возникновения ошибки при попытке обратиться по неверному индексу'
        item1 = Item()
        self.assertRaises(TypeError, Item.get_item_by_id(item1._id + 1))

    def tests_get_item_by_index_in_items(self):
        "Проверка получения объекта Item в списке _items при обращении по индексу, равному id"
        item1 = Item()
        self.assertEqual(Item._items[item1._id], item1)

    def test_save_as_json_item_object(self):
        'Проверка сохранения экземляра Item в json файл'
        item1 = Item()
        item1.save_as_json()
        with open(f'item_{item1._id}.json', 'r') as f:
            data = json.load(f)
            self.assertEqual(data, item1.__dict__)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)