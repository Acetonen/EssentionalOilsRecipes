from sys import exit

# Загрузка базы из файла
def Baze():
    file = open("baze.txt", "r+")
    baze = {}
    for line in file:
        # построчно из файла идет построение словаря из словарей
        # до двоеточия формируется ключ главного словаря, после двоеточия
        # идет формирование словаря, к-з которого разделяются запятой,
        # а ключи от значений отделяяются тире
        baze[line[:line.index(':')]] = dict(item.split('-') for item in
                                       line[line.index(':') + 1:-1].split(','))
    return baze
    file.close()

# Загрузка коллекции ингредиентов из файла
def Collection():
    with open("collection.txt", 'r+') as file:
        collection = []
        for line in file:
            collection.append(line[:-1])
    sortList = sorted(collection)
    return sortList

# Удаление элемента из базы данных
def Delete(fileName, delete, name):
    with open(fileName, "r+") as file:
        oldBaze = file.readlines() # подгружаем старую базу
        file.seek(0) # перемещаем курсор в начало файла
        for line in oldBaze:
            # записываем базу в начало файла кроме удаляемой строки
            if line[:len(delete)] != delete:
                file.write(line)
        # удаляем старую базу из файла
        file.truncate()
    print(f"{name} '{delete}' удален.\r\n")

def BeautyPrint(name):
    print(name, end=': ')
    for key in baze[name]:
        print(f"{key} - {baze[name][key]}к;", end=' ')
    print()

# Главное меню программы
mainMenu = """\
RecipesDatabase ver.1.1
----------------------------------------------------
    [С] Cоздать новый рецепт
    [П] Показать все рецепты
    [В] Показать только те рецепты, для которых хватает ингредиентов
    [У] Удалить рецепт
    [К] Показать мою коллекцию масел
    [З] Завершить программу
----------------------------------------------------
    """
# Уменьшенное главное меню
miniMenu = """\
----------------------------------------------------
[С]-нов.рецепт [П]-все рецепты [В]-возможные рецепты
[У]-уд. рецепт [К]-моя коллекц.[З]-завершить прогр.
"""
# Меню коллекций
collectionMenu = """
----------------------------------------------------
    [Д] Добавить масло в коллекцию
    [У] Удалить масло из коллекции
    [Н] Найти все рецепты с заданным ингредиетнтом
    [О] Показать лист отсутсвующих ингредиентов
    [М] Вернуться в основное меню программы
"""


print(mainMenu)
while True:
    choise = input()
# Создание нового рецепта
    if choise == ('с' or 'С'):
        with open("baze.txt", "a") as file:
            file.write(input("Название рецепта: "))
            file.write(":")
            inp = input("Введите ингредиенты с количеством капель \
по одному (напр: герань-3): ")
            file.write(f"{inp}")
            while True:
                inp = input("Введите ингредиет ( просто ENTER, чтобы закончить): ")
                if inp != '':
                    file.write(',')
                    file.write(f"{inp}")
                else: break
            file.write("\r\n")
        print(f"Рецепт создан в базе\r\n")
        print(miniMenu)
# Вывод всех рецептов в алфавитном порядке
    elif choise == ('п' or 'П'):
        baze = Baze() # подгружаем базу из файла
        keys = sorted(baze) # создаем лист из отсортированных ключей
        for item in keys:
            BeautyPrint(item)
        print(miniMenu)
# Удаление рецепта
    elif choise == ('у' or 'У'):
        delete = input("Введите название рецепта, который необходимо удалить: ")
        Delete("baze.txt", delete, "Рецепт")
        print(miniMenu)
# Только те рецепты, на которых достаточно ингредиентов
    elif choise == ('в' or 'В'):
        coll = Collection() # подгружаем коллекцию из файла
        baze = Baze() # подгружаем базу из файла
        # Ищем ингредиенты из базы в списке доступных
        for name in baze:
            flag = True
            for ing in list(baze[name].keys()):
                if ing not in coll:
                    flag = False
            # Красиво выводим список на экран
            if flag:
                BeautyPrint(name)
        print(miniMenu)

# Выводим пронумерованную коллекцию масел и остаемся в меню коллекции
    elif choise == ('к' or 'К'):
        coll = Collection()
        print("Моя коллекция:")
        for count, oil in enumerate(Collection(),1):
            print(f"[{count}] {oil}")
        print(collectionMenu)
        while True:
            choise = input()
            # Удаляем ингридиент из коллекции
            if choise == ('у' or 'У'):
                n = int(input("Введите номер удаляемого ингридиента: "))
                delete = coll[n - 1]
                Delete("collection.txt", delete, "Ингредиент")
            # Добавляем ингридиент в коллекцию
            elif choise == ('д' or 'Д'):
                with open("collection.txt", "a") as file:
                    file.write(input("Введите название ингредиента: "))
                    file.write("\r\n")
                print(collectionMenu)
            # Найти рецепты с ингредиентами
            elif choise == ('н' or 'Н'):
                baze = Baze() # подгружаем базу из файла
                n = int(input("Введите номер ингредиента: "))
                search = coll[n - 1]
                print(f"\r\nРецепты, содержащие '{search}':")
                # создаем лист из ключей нашей базы, в которые входит искомый компонент
                listOfrecipesNames = [keyg for (keyg, value) in baze.items() if search in value]
                for name in listOfrecipesNames:
                    print(name, end=': ')
                    for key in baze[name]:
                        print(f"{key} - {baze[name][key]}к;", end=' ')
                    print()
                print(collectionMenu)
            # Показываем список всех ингредиентов в рецептах и помечаем отсутствующие
            elif choise == ('о' or 'О'):
                baze = Baze() # подгружаем базу из файла
                listOfIngredients = []
                # Формируем лист из всех ингредиентов в рецептах (без повторов)
                for i in baze:
                    listOfIngredients += list(baze[i].keys())
                listOfIngredients = sorted(set(listOfIngredients))
                # Ищем отсутствующие ингредиенты из нашей коллекции
                for i in range(len(listOfIngredients)):
                    print(listOfIngredients[i], end=' ')
                    if listOfIngredients[i] not in Collection():
                        print(" - отсутствует.")
                    else: print()
                print(collectionMenu)
            # Возвращаемся в главное меню
            elif choise == ('м' or 'М'):
                print(mainMenu)
                break
            # Ошибка ввода буквы
            else:
                print("Такого варианта нет, введите команду правильно\r\n")

# Завершить программу
    elif choise == ('З' or 'з'): exit()











































    elif choise == 'Анечка':
        print("""
            Антошка любит Анечку :-*

            $$$$$$$$      $$$$$$$$$
          $$$$$$$$$$$$  $$$$$$$  $$$$
         $$$$$$$$$$$$$$$$$$$$$$$$  $$$
         $$$$$$$$$$$$$$$$$$$$$$$$  $$$
         $$$$$$$$$$$$$$$$$$$$$$$$  $$$
          $$$$$$$$$$$$$$$$$$$$$$  $$$
            $$$$$$$$$$$$$$$$$$$$$$$
               $$$$$$$$$$$$$$$$$
                 $$$$$$$$$$$$$
                    $$$$$$$
                      $$$
                       $
""")
# Ошибка ввода буквы
    else:
        print("Такого варианта нет, введите команду правильно\n")
