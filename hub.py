from datetime import date, datetime
from item import Item

class Hub:
    __instance = None
    def __new__(cls, *args, **kwargs):
        'Функционал Синглтона'
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, hub=None, hdate=date.today(), items=None):
        self._hub = hub
        self.hdate = hdate # использование свойства hdate при инициализации объекта
        self._items = items or []

    def __repr__(self):
        return f"{self._hub}: {self._items[:3]}"

    def __str__(self):
        return f"{self._hub}: {', '.join([item._name for item in self._items[:3]])}"

    def __len__(self):
        return len(self._items)

    def __getitem__(self, i):
        'Обращение к отдельным item в _items объекта Hub по индексам'
        if len(self._items) < i:
           raise IndexError
        return (self._items)[i]

    @property
    def items(self):
        return self._items

    def add_item(self, item):
        'Добавление одного item для объекта Hub'
        if isinstance(item, Item):
            self._items.append(item)
        else:
            raise TypeError("Аргумент должен быть объектом класса Item()")

    def add_items(self, items):
        'Добавление items для объекта Hub'
        for item in items:
            if isinstance(item, Item) and item not in self._items:
                self._items.append(item)


    def find_by_id(self, id):
        'Поиск item и его индекса по его id в _items объекта Hub'
        for pos, item in enumerate(self._items):
            if id == item._id:
                result = (pos, item)
            else:
                result = (-1, None)
            return result

    def find_by_tags(self, tags):
        'Поиск items в _items объекта Hub со всеми тегами из tags'
        result = []
        for item in self._items:
            counter = 0
            for tag in tags:
                if tag in item._tags:
                    counter += 1
            if counter == len(tags):
                result.append(item)
        return result

    def rm_item(self, i=None):
        'Удаление item из _items объекта Hub'
        if isinstance(i, Item):
            if i in self._items:
                self._items.remove(i)
        elif isinstance(i, int):
            for item in self._items:
                if item._id == i:
                    self._items.remove(item)
                    break
        else:
            raise TypeError('Неверный тип аргумента')

    def drop_items(self, items):
        'Удаление переданных объектов items из _items объекта Hub'
        for item in items:
            self.rm_item(item)

    def clear(self):
        'Очистка _items объекта Hub'
        self._items.clear()

    @property
    def hdate(self):
        return self._hdate

    @hdate.setter
    def hdate(self, hdate):
        if isinstance(hdate, str):
            self._hdate = hdate
        else:
            ValueError('Неверный формат даты, введите дату в формате "ДД.ММ.ГГГГ"')

    def find_by_date(self, *dates):
        'Возвращение списка всех объектов Item из _items, подходящих по дате'
        if len(dates) == 1:
            # Return all items with a date earlier than or equal to the given date
            return [item for item in self._items if datetime.strptime(item.dispatch_date, '%d.%m.%Y') <= datetime.strptime(dates[0], '%d.%m.%Y')]
        elif len(dates) == 2:
            # Return all items with a date in the given interval
            start_date, end_date = sorted([datetime.strptime(d, '%d.%m.%Y') for d in dates])
            return [item for item in self._items if start_date <= datetime.strptime(item.dispatch_date, '%d.%m.%Y') <= end_date]
        else:
            raise ValueError("Too many parameters passed to find_by_date() method.")


    def find_most_valuable(self, amount=1):
        'Поиск самых дорогих предметов на складе в количестве amount'
        sorted_items = sorted(self._items, key=lambda item: item.cost, reverse=True)
        return sorted_items[:amount]

