import json
class Item:
    count = 0
    _items = []
    def __init__(self, name=None, description=None, dispatch_date='', tags=None, cost=None):
        self._id = Item.count
        Item.count += 1 # создание уникального id
        self._name = name
        self._description = description
        self._dispatch_date = dispatch_date
        self._tags = tags or []
        self._cost = cost
        # Добавить текущий инстанс item в список _items по индексу id
        Item._items.append(self)


    @staticmethod
    def get_item_by_id(id):
        # Вернуть инстанс item из списка _items по индексу id
        if isinstance(id, int) and id < len(Item._items):
            return Item._items[id]
        else:
            return TypeError('Неверный id')

    def __repr__(self):
        return f"{self._id} {self.name}: {', '.join(self._tags[:3])}"

    def __str__(self):
        return f"id {self._id}: {self.name}"

    def __len__(self):
        return len(self._tags)

    def add_tag(self, tag):
        'Добавление тега для объекта Item'
        if isinstance(tag, str) and tag not in self._tags:
            self._tags.append(tag)

    def rm_tag(self, tag):
        'Удаление тега для объекта Item'
        if isinstance(tag, str) and tag in self._tags:
            self._tags.remove(tag)

    def add_tags(self, tags):
        'Добавление тегов для объекта Item'
        for tag in tags:
            if isinstance(tag, str) and tag not in self._tags:
                self._tags.append(tag)

    def remove_tags(self, tags):
        'Удаление тегов для объекта Item'
        for tag in tags:
            if isinstance(tag, str) and tag in self._tags:
                self._tags.remove(tag)

    def __lt__(self, other):
        'Сравнение объектов Item по цене'
        if isinstance(other, Item) and isinstance(other.cost and self.cost, int | float):
            return self.cost < other.cost
        return TypeError('Неверный тип данных для сравнения')

    def is_tagged(self, tags):
        'Проверка наличия тегов в объекте Item'
        if isinstance(tags, str):
            return tags in self._tags
        else:
            return all(tag in self._tags for tag in tags)

    def copy(self):
        'Создание копии экземпляра Item с другим id'
        return Item(
            name=self._name,
            description=self._description,
            dispatch_date=self._dispatch_date,
            tags=self._tags[:], #сначала хотела использовать deepcopy, но слишком он медленный, и проверка показала, что изменение списка тегов одного экземляра не влияет на список тегов его копии
            cost=self._cost
        )


    """Создание property через передачу функций get_cost, set_cost в функцию property()"""
    # def set_cost(self, cost=None):
    #     if isinstance(cost, int):
    #         self._cost = cost
    #     else:
    #         raise ValueError('Некорректная цена')
    #
    # def get_cost(self):
    #     return self._cost
    #
    # cost = property(get_cost, set_cost)                # создаем свойство cost для управления ценой

    """Создание property через использование декоратора"""

    @property
    def name(self):
        'Поле name только для чтения'
        return self._name

    @property
    def dispatch_date(self):
        return self._dispatch_date

    @dispatch_date.setter
    def dispatch_date(self, dispatch_date):
        if isinstance(dispatch_date, str):
            self._dispatch_date = dispatch_date
        else:
            ValueError('Неверный формат даты, введите дату в формате "ДД.ММ.ГГГГ"')

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, cost):
        if isinstance(cost, int | float):
            self._cost = cost
        else:
            raise ValueError('Некорректная цена')

    @classmethod
    def create_from_json(cls, json_path):
        'Создает объект Item из файла json'
        with open(json_path, 'r') as file:
            data = json.load(file)  # передаем файловый объект
            return Item(**data)
    @classmethod
    def create_several_obj_from_json(cls, json_path):
        'Создает генератор объектов типа Item из файла json'
        with open(json_path, 'r') as file:
            data = json.load(file)  # передаем файловый объект
            for item in data:
                yield Item(**item)

    def save_as_json(self):
        with open(f'item_{self._id}.json', 'w') as file:
            json.dump(self.__dict__, file)

# не понимаю, зачем нужно переопределять хэш, если можно сравнивать два объекта по id, который уникален из условия (id доступен только для чтения)
    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        if isinstance(other, Item):
            return self._id == other._id
        return NotImplemented

