from websocket import create_connection
import random
import json

names = ["Эйнштейн", "Карим", "Кумбосар", "Бенди", "Антон", "Эдик", "Антонио", "Степан", "Кирилл", "Королёв", "Глеб", "Кириллов", "Айзер", "Блатной", "Писькин", "Пупкин", "Вася", "Фрешбар", "Кнайф", "Чарджери", "Лампочка", "Ковалёв", "Альметов", "Альметевск", "Камиль"]
car_types = ["autotower","crane","loader"]

ws = create_connection("ws://localhost:9000/")

ids_file = open("ids_papa.txt", 'w')
machine_files = open("ids.txt", 'r')

machine_ids = machine_files.read().split('\n')

for i in range(1, 139) :
    fullname = names[random.randint(0, len(names) - 1)] + " " + names[random.randint(0, len(names) - 1)] + " " + names[random.randint(0, len(names) - 1)]
    monthHours = str(random.randint(0, 100))
    allHours = str(int(monthHours) + random.randint(0, 1000))
    malf_js = '{"type":"Drivers", "data": { "type":"' + car_types[random.randint(0,2)] + '", "name":"' + fullname + '", "month_hours": ' + monthHours + ', "all_hours":' + allHours + ', "daily_transport_id":"' + machine_ids[i-1] + '" } }'
    ws.send(malf_js)
    result = json.loads(ws.recv())
    ids_file.write(result["id"] + "\n")
ids_file.close()
    