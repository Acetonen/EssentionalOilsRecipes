from sys import exit
import json

# Загрузка базы данных или списка ингредиентов из файла
def Data(fileName):
        with open(fileName) as file:
            data = json.load(file)
        return data

# Запись базы данных или списка ингредиентов в файл
def SaveData(fileName, data):
        with open(fileName, 'w') as file:
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
    baze = Data('baze.txt')
    print(name, end=': ')
    for key in baze[name]:
        print(f"{key} - {baze[name][key]}к;", end=' ')
    print()

# Отображение пронумерованной и отсортированной колекции ингредиентов
def Collection():
    coll = sorted(Data('collection.txt'))
    print("Моя коллекция:")
    for count, oil in enumerate(coll,1):
        print(f"[{count}] {oil}")
    print()

# Отображение пронумерованной и отсортированной коллекции рецептов
def Recipes():
    try: rateDict = Data('rate.txt')
    except: rateDict = {}
    baze = Data('baze.txt') # подгружаем базу из файла
    keys = sorted(baze) # создаем лист из отсортированных ключей
    for count, oil in enumerate(keys,1):
        print(f"[{count}]", end=' ') # номер в списке
        print(f"{rateDict.get(oil, '0')}/10", end=' ') # рейтинг рецепта
        BeautyPrint(oil) # ингридиенты в рецепте

# Главное меню программы
mainMenu = """\

RecipesDatabase ver.1.1
****************************************************
    [С] Cоздать новый рецепт
    [П] Показать все рецепты
    [В] Показать рецепты с ингредиентами из коллекции
    [У] Удалить рецепт
    [К] Показать мою коллекцию масел
    [Р] Поставить рейтинг рецепту
    [З] Завершить программу
****************************************************
    """
# Уменьшенное главное меню
miniMenu = """\
----------------------------------------------------
[С]-нов.рецепт [П]-все рецепты [В]-возможные рецепты
[У]-уд. рецепт [К]-моя коллекц.[Р]-поставить рейтинг
[З]-завершить прогр.
"""
# Меню коллекций
collectionMenu = """
****************************************************
    [Д] Добавить масло в коллекцию
    [У] Удалить масло из коллекции
    [Н] Найти все рецепты с заданным ингредиетнтом
    [О] Показать лист отсутсвующих ингредиентов
    [М] Вернуться в основное меню программы
    [З] Завершить программу
****************************************************
"""
# Уменьшенное меню коллекций
miniCollectionMenu = """
----------------------------------------------------
[Д]-добав.масло [У]-удл.масло [Н]-найти рецепты
[О]-отсут.ингр. [М]-меню      [К]-показать колекцию
[З]-завершить прогр.
"""

# ГЛАВНОЕ МЕНЮ
print(mainMenu)
while True:
    choise = input()
# Создание нового рецепта
    if choise == ('с' or 'С'):
        baze = Data('baze.txt')
        name = input("Название рецепта: ")
        ingredientList = {}
        while True:
            ingredient = input("Введите ингредиет (ENTER для отмены): ")
            if ingredient == '': break
            drop = input("количество капель: ")
            ingredientList[ingredient] = drop
        baze[name] = ingredientList
        SaveData("baze.txt", baze)
        print(f"\nРецепт записан в базу.\n")
        print(miniMenu)
# Вывод всех рецептов в алфавитном порядке
    elif choise == ('п' or 'П'):
        Recipes()
        print(miniMenu)
# Удаление рецепта
    elif choise == ('у' or 'У'):
        keys = sorted(Data('baze.txt')) # пронумерованный список рецептов
        choise = int(input("Введите номер рецепта, который необходимо удалить: "))
        Delete("baze.txt", keys[choise - 1])
        Delete("rate.txt", keys[choise - 1])
        print(f"\nРецепт '{keys[choise - 1]}' удален.\n")
        print(miniMenu)
# Только те рецепты, на которых достаточно ингредиентов
    elif choise == ('в' or 'В'):
        coll = Data('collection.txt') # подгружаем коллекцию из файла
        baze = Data('baze.txt') # подгружаем базу из файла
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
                print()
                BeautyPrint(name)
        if mainFlag:
            print("\nПохоже, что у Вас ни на что не хватает ингредиентов :'(\n")
        print(miniMenu)
# Рейтинг рецепту
    elif choise == ('р' or 'Р'):
        try: rateDict = Data('rate.txt')
        except: rateDict = {}
        keys = sorted(Data('baze.txt'))
        choise = int(input("Ведите номер рецепта: "))
        rate = input("Введите оценку (из 10-ти): ")
        rateDict[keys[choise - 1]] = rate
        SaveData('rate.txt', rateDict)
        print(miniMenu)

# МЕНЮ КОЛЛЕКЦИИ
    elif choise == ('к' or 'К'):
        print(collectionMenu)
        Collection()
        while True:
            choise = input()
            # Удаляем ингридиент из коллекции
            if choise == ('у' or 'У'):
                coll = sorted(Data('collection.txt'))
                n = int(input("Введите номер удаляемого ингридиента: "))
                delete = coll[n - 1]
                Delete("collection.txt", delete)
                Collection()
                print(f"\nИнгридиент '{delete}' удален.")
                print(miniCollectionMenu)
            # Добавляем ингридиент в коллекцию
            elif choise == ('д' or 'Д'):
                listOfrecipes = Data('collection.txt')
                listOfrecipes.append(input("Введите название ингредиента: "))
                SaveData('collection.txt', listOfrecipes)
                print()
                Collection()
                print(miniCollectionMenu)
            # Найти рецепты с ингредиентами
            elif choise == ('н' or 'Н'):
                baze = Data('baze.txt') # подгружаем базу из файла
                coll = sorted(Data('collection.txt')) # подгружаем отсортированную коллекцию
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
            elif choise == ('о' or 'О'):
                baze = Data('baze.txt') # подгружаем базу из файла
                listOfIngredients = []
                # Формируем лист из всех ингредиентов в рецептах (без повторов)
                for i in baze:
                    listOfIngredients += list(baze[i].keys())
                listOfIngredients = sorted(set(listOfIngredients))
                # Ищем отсутствующие ингредиенты из нашей коллекции
                for i in range(len(listOfIngredients)):
                    print(listOfIngredients[i], end=' ')
                    if listOfIngredients[i] not in Data('collection.txt'):
                        print(" - отсутствует.")
                    else: print()
                print(miniCollectionMenu)
            elif choise == ('к' or 'К'):
                Collection()
            # Возвращаемся в главное меню
            elif choise == ('м' or 'М'):
                print(mainMenu)
                break
            # Ошибка ввода буквы
            elif choise == ('З' or 'з'): exit()
            else:
                print("Такого варианта нет, введите команду правильно\n")

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
