from sys import exit

# Загрузка базы из файла
def Baze():
    file = open("baze.txt", "r+")
    baze = {}
    for line in file:
        baze[line[:line.index(':')]] = list(line[line.index(':') + 1:-1].split(','))
    return baze
    file.close()
# Выбор пользователя
print("""\
    [С] Cоздать новый рецепт.
    [Н] Найти все рецепты с заданным ингридиетнтом.
    [П] Показать все рецепты.
    [У] Удалить рецепт.
    [З] Завершить программу.
    """)
while True:
    choise = input()
# Создание нового рецепта
    if choise == ('с' or 'С'):
        with open("baze.txt", "a") as file:
            file.write(input("Название рецепта: "))
            file.write(":")
            file.write(input("Введите ингридиенты через запятую без пробелов: "))
            file.write("\n")
        print(f"Рецепт создан в базе\n")
# Найти рецепты с ингредиентами
    elif choise == ('н' or 'Н'):
        Baze()
        search = input("Введите название ингридиента: ")
        listOfrecipesNames = [key for (key, value) in baze.items() if search in value]
        for name in listOfrecipesNames:
            print(name, baze[name])
        print()
# Вывод всех рецептов в алфавитном порядке
    elif choise == ('п' or 'П'):
        baze = Baze()
        keys = sorted(baze)
        for item in keys:
            print(item, baze[item])
        print()
# Удаление рецепта
    elif choise == ('у' or 'У'):
        delete = input("Введите название рецепта, который необходимо удалить: ")
        with open("baze.txt", "r+") as file:
            oldBaze = file.readlines()
            file.seek(0)
            for line in oldBaze:
                if line[:len(delete)] != delete:
                    file.write(line)
            file.truncate()
        print(f"Рецепт '{delete}' удален.\n")
# Завершить программу
    elif choise == ('З' or 'з'):
        exit()
    else:
        print("Такого варианта нет, введите команду правильно\n")
