from sys import exit
import json

# Загрузка базы данных или списка ингредиентов из файла
def Data(fileName):
        # Обязательное указание кодировки для винды
        with open(fileName, 'r', encoding='utf8') as file:
            data = json.load(file)
        return data

# Запись базы данных или списка ингредиентов в файл
def SaveData(fileName, data):
        with open(fileName, 'w', encoding='utf8') as file:
            json.dump(data, file)

# Удаление элемента из базы данных или списка ингредиентов
def Delete(fileName, delete):
    with open(fileName, "r+") as file:
        baze = json.load(file) # подгружаем старую базу
        try: baze.pop(delete, None) # если имеем дело со словарем
        except: baze.remove(delete) # если имеем дело с листом
        file.seek(0) # перемещаем курсор в начало файла
        file.truncate() # очищаем файл
        json.dump(baze, file) # записываем новую базу

# Красивый вывод данных на экран
def BeautyPrint(name):
    baze = Data('data/baze.txt')
    print(f"{name}{(MaxLength(baze)-len(name)+1)*' '}", end=': ')
    for key in baze[name]:
        print(f"{key} - {baze[name][key]}к;", end=' ')
    print()

# Отображение пронумерованной и отсортированной колекции ингредиентов
def Collection():
    coll = sorted(Data('data/collection.txt'))
    print("Моя коллекция:")
    for count, oil in enumerate(coll,1):
        print(f"[{count}] {oil}")
    print()

# Отображение пронумерованной и отсортированной коллекции рецептов
def Recipes():
    try: rateDict = Data('data/rate.txt')
    except: rateDict = {}
    baze = Data('data/baze.txt') # подгружаем базу из файла
    keys = sorted(baze) # создаем лист из отсортированных ключей
    for count, oil in enumerate(keys,1):
        # добавляем пробел после номера рецепта для ровного отображения таблицы
        if count<10: spase = " "
        else: spase = ''
        print(f"[{count}] {spase}", end=' ') # номер в списке
        print(f"{rateDict.get(oil, '0')}/10", end=' ') # рейтинг рецепта
        BeautyPrint(oil) # ингридиенты в рецепте

# Нахождение элемента списка максимальной длины
def MaxLength(array):
    mL = 0
    try: # если аргументом выступает лист
        for i in array:
            if len(i) > mL:
                mL = len(i)
    except: # если аргументом выступает словарь
        length = [key for (key, value) in array.items()]
        for i in length:
            if len(i) > mL:
                mL = len(i)
    return mL

# Выбор языка программы
print("""
Choose the languege / Выберете язык
[E] - English
[R] - Russian
""")
languege = input("")
if languege == 'r' or languege == 'R':
    import localisations.RUS as RUS
    try: import localisations.suggestions_RU
    except: print("Здравствуте!")
    mainMenu = RUS.mainMenu # Главное меню программы
    miniMenu = RUS.miniMenu # Уменьшенное главное меню
    collectionMenu = RUS.collectionMenu # Меню коллекций
    miniCollectionMenu = RUS.miniCollectionMenu # Уменьшенное меню коллекций
elif languege == 'e' or languege == 'E':
    import localisations.EN as EN
    mainMenu = EN.mainMenu # Главное меню программы
    miniMenu = EN.miniMenu # Уменьшенное главное меню
    collectionMenu = EN.collectionMenu # Меню коллекций
    miniCollectionMenu = EN.miniCollectionMenu # Уменьшенное меню коллекций

# ГЛАВНОЕ МЕНЮ
print(mainMenu)
while True:
    choise = input()
# Создание нового рецепта
    if choise == 'с' or choise == 'С' or choise == 'c' or choise == 'C':
        baze = Data('data/baze.txt')
        name = input("Название рецепта: ")
        ingredientList = {}
        while True:
            ingredient = input("Введите ингредиет (ENTER для отмены): ")
            if ingredient == '': break
            drop = input("количество капель: ")
            ingredientList[ingredient] = drop
        baze[name] = ingredientList
        SaveData("data/baze.txt", baze)
        print(f"\nРецепт записан в базу.\n")
        print(miniMenu)
# Вывод всех рецептов в алфавитном порядке
    elif choise == 'п' or choise == 'П' or choise == 's' or choise == 'S':
        Recipes()
        print(miniMenu)
# Удаление рецепта
    elif choise == 'у' or choise == 'У' or choise == 'r' or choise == 'R':
        keys = sorted(Data('data/baze.txt')) # пронумерованный список рецептов
        choise = int(input("Введите номер рецепта, который необходимо удалить: "))
        Delete("data/baze.txt", keys[choise - 1])
        Delete("data/rate.txt", keys[choise - 1])
        print(f"\nРецепт '{keys[choise - 1]}' удален.\n")
        print(miniMenu)
# Только те рецепты, на которых достаточно ингредиентов
    elif choise == 'в' or choise == 'В' or choise == 'i' or choise == 'I':
        coll = Data('data/collection.txt') # подгружаем коллекцию из файла
        baze = Data('data/baze.txt') # подгружаем базу из файла
        # Ищем ингредиенты из базы в списке доступных
        mainFlag = True
        for name in baze:
            flag = True
            for ing in list(baze[name].keys()):
                if ing not in coll:
                    flag = False
            # Красиво выводим список на экран
            if flag:
                mainFlag = False
                BeautyPrint(name)
        if mainFlag:
            print("\nПохоже, что у Вас ни на что не хватает ингредиентов :'(\n")
        print(miniMenu)
# Рейтинг рецепту
    elif choise == 'р' or choise == 'Р' or choise == 'g' or choise == 'G':
        try: rateDict = Data('data/rate.txt')
        except: rateDict = {}
        keys = sorted(Data('data/baze.txt'))
        choise = int(input("Ведите номер рецепта: "))
        rate = input("Введите оценку (из 10-ти): ")
        rateDict[keys[choise - 1]] = rate
        SaveData('data/rate.txt', rateDict)
        print(miniMenu)

# МЕНЮ КОЛЛЕКЦИИ
    elif choise == 'к' or choise == 'К' or choise == 'o' or choise == 'O':
        print(collectionMenu)
        Collection()
        while True:
            choise = input()
            # Удаляем ингридиент из коллекции
            if choise == 'у' or choise == 'У' or choise == 'r' or choise == 'R':
                coll = sorted(Data('data/collection.txt'))
                n = int(input("Введите номер удаляемого ингридиента: "))
                delete = coll[n - 1]
                Delete("data/collection.txt", delete)
                Collection()
                print(f"\nИнгридиент '{delete}' удален.")
                print(miniCollectionMenu)
            # Добавляем ингридиент в коллекцию
            elif choise == 'д' or choise == 'Д' or choise == 'a' or choise == 'A':
                listOfrecipes = Data('data/collection.txt')
                listOfrecipes.append(input("Введите название ингредиента: "))
                SaveData('data/collection.txt', listOfrecipes)
                print()
                Collection()
                print(miniCollectionMenu)
            # Найти рецепты с ингредиентами
            elif choise == 'н' or choise == 'Н' or choise == 'f' or choise == 'F':
                baze = Data('data/baze.txt') # подгружаем базу из файла
                coll = sorted(Data('data/collection.txt')) # подгружаем отсортированную коллекцию
                n = int(input("Введите номер ингредиента: "))
                search = coll[n - 1]
                print(f"\nРецепты, содержащие '{search}':\n")
                # создаем лист из ключей нашей базы, в которые входит искомый компонент
                listOfrecipesNames = [keyg for (keyg, value) in baze.items() if search in value]
                sortList = sorted(listOfrecipesNames)
                for name in sortList:
                    BeautyPrint(name)
                print(miniCollectionMenu)
            # Показываем список всех ингредиентов в рецептах и помечаем отсутствующие
            elif choise == 'о' or choise == 'О' or choise == 's' or choise == 'S':
                baze = Data('data/baze.txt') # подгружаем базу из файла
                listOfIngredients = []
                # Формируем лист из всех ингредиентов в рецептах (без повторов)
                for i in baze:
                    listOfIngredients += list(baze[i].keys())
                # Подсчитываем частоту встречаемости ингредиентов в рецептах
                ingredientsCounter = {i: listOfIngredients.count(i) for i in listOfIngredients}
                # Группируем ингридиенты по частоте встречаемости
                reverseCounter = {}
                for k, v in ingredientsCounter.items():
                    reverseCounter[v] = reverseCounter.get(v, [])
                    reverseCounter[v].append(k)
                # Создаем сортировочный лист по частоте встречаемости
                priority = list(reversed(sorted([key for (key, value) in reverseCounter.items()])))
                # Выводим список ингридиентов по частоте встречаемости в рецептах
                # и проверяем наличие ингридиентов в коллекции
                for position in priority:
                    for ingredient in reverseCounter[position]:
                        print(f"""\
{ingredient}{(MaxLength(listOfIngredients) - len(ingredient) + 1) * ' '}\
(в {position} рецептах)\
""", end=' ')
                        if ingredient not in Data('data/collection.txt'):
                            print(" - отсутствует в коллекции.")
                        else: print()
                print(miniCollectionMenu)
            # Показать меню коллекции
            elif choise == 'к' or choise == 'К' or choise == 'o' or choise == 'O':
                Collection()
            # Возвращаемся в главное меню
            elif choise == 'м' or choise == 'М' or choise == 'm' or choise == 'M':
                print(mainMenu)
                break
            # Ошибка ввода буквы
            elif choise == 'з' or choise == 'З' or choise == 'e' or choise == 'E': exit()
            else:
                print("Такого варианта нет, введите команду правильно\n")

# Завершить программу
    elif choise == 'з' or choise == 'З' or choise == 'e' or choise == 'E': exit()











































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
