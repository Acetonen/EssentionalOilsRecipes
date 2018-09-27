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
while True:
    choise = input("""\
    [Н] Cоздать новый рецепт.
    [И] Найти все рецепты с заданным ингридиетнтом.
    [А] Показать все рецепты.
    [У] Удалить рецепт.
    [В] Завершить программу.
    """)
    # Создание нового рецепта
    if choise == ('н' or 'Н'):
        with open("baze.txt", "a") as file:
            file.write(input("Название рецепта: "))
            file.write(":")
            file.write(input("Введите ингридиенты через запятую без пробелов: "))
    # Найти рецепты с ингредиентами
    elif choise == ('и' or 'И'):
        Baze()
        search = input("Введите название ингридиента: ")
        listOfrecipesNames = [key for (key, value) in baze.items() if search in value]
        for name in listOfrecipesNames:
            print(name, baze[name])
    # Вывод всех рецептов в алфавитном порядке
    elif choise == ('а' or 'А'):
        baze = Baze()
        keys = sorted(baze)
        for item in keys:
            print(item, baze[item])
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
        print(f"Рецепт '{delete}' удален.")
    # Завершить программу
    elif choise == 'В':
        exit()
