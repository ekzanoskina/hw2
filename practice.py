from hub import Hub
from item import Item
import random
from datetime import datetime
from datetime import timedelta

# Создание объекта Hub
hub = Hub(hub='Grocery shop', hdate='02.12.2023')

# Добавление объектов Item в Hub
items_list = ['Banana', 'Apple', 'orange', 'pineapple', 'asparagus', 'chili', 'garlic', 'celery', 'pepper', 'currant', 'cherry', 'blackberry', 'gooseberry', 'potato', 'pumpkin', 'kale', 'tomatoes', 'peas', 'daikon', 'carrot']
costs_list = [24, 45.50, 45, 78, 12, 56, 0, 13, 15, 91, 100, 45.08, 36, 77, 16, 54, 23, 43, 45, 89]
dispatch_dates = ['29.11.2024', '31.12.2024', '23.11.2023', '04.12.2023', '07.10.2023', '01.01.2024', '27.12.2023', '13.11.2023', '12.12.2023', '04.06.2024', '09.10.2023', '01.01.2022', '01.01.2025', '29.11.2029', '31.12.2032', '15.11.2025', '05.12.2023', '06.10.2023', '17.01.2024', '13.12.2023']
for i in zip(items_list, costs_list, dispatch_dates):
    hub.add_item(Item(name=i[0], cost=i[1], dispatch_date=i[2]))

# Выбросите все объекты с названиями начинающиеся на "a" или "A", записав их в отдельный лист A
A = []
for item in hub.items:
    if item.name.lower().startswith('a'):
        A.append(item.name)
        hub.rm_item(item)
print(A)

# Выбросите все объекты с датой отправки раньше чем дата в hub, записав их в отдельный лист Outdated
outdated = []
for item in hub.find_by_date(hub.hdate):
    hub.rm_item(item)
    outdated.append(item)
print(outdated)

# Выбросите топ-10 объектов из hub, записав их в MostValuable
most_valuable = []
for item in hub.find_most_valuable(10):
    hub.rm_item(item)
    most_valuable.append(item)
print(most_valuable)

# Оставшиеся на складе объекты запишите в Others
others = hub.items
print(others)

# Генератор объектов Item
def get_random_date():
    'Возвращает случайную дату из диапазона'
    start_dt = datetime.strptime('01.01.2023', '%d.%m.%Y')
    end_dt = datetime.strptime('31.12.2024', '%d.%m.%Y')
    delta = end_dt - start_dt
    random_date = start_dt + timedelta(random.randint(0, delta.days))
    return random_date.strftime('%d.%m.%Y')

def generate_item():
    'Бесконечный генератор обектов Item'
    counter = 0
    while True:
        item = Item(name=f'item_{counter}', dispatch_date=get_random_date(), cost=random.randint(50, 500))
        counter += 1
        yield item

# Пример использования бесконечного генератора
gen = generate_item()
for i in range(20):
    print(next(gen))