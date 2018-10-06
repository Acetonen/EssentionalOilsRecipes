import sys
import json
#PEP8

def data(file_name):
    """Load base from file."""
    with open(file_name, 'r', encoding='utf8') as file:
        data = json.load(file)
    return data

def save_data(file_name, data):
    """Dump base in file."""
    with open(file_name, 'w', encoding='utf8') as file:
        json.dump(data, file)

def delete(file_name, delete):
    """Delete ingredient or recipe from base."""
    with open(file_name, "r+") as file:
        base = json.load(file)
        # Different ways to list and dictionary.
        try: base.pop(delete, None)
        except: base.remove(delete)
        file.seek(0)
        file.truncate()
        json.dump(base, file)

def beauty_print(name):
    """Structural output."""
    base = data('data/base.txt')
    print(f"{name}{(max_length(base) - len(name) + 1)*' '}", end=': ')
    for key in base[name]:
        print(f"{key} - {base[name][key]}к;", end=' ')
    print()

def collection():
    """Otput numbered and sorted igredient collection."""
    coll = sorted(data('data/collection.txt'))
    print("Моя коллекция:")
    for count, oil in enumerate(coll,1):
        print(f"[{count}] {oil}")
    print()

def recipes():
    """ Print sorted recipes collection"""
    try: rate_dict = data('data/rate.txt')
    except: rate_dict = {}
    base = data('data/base.txt')
    keys = sorted(base)
    for count, oil in enumerate(keys,1):
        # Ensert some spaces after recite nubber.
        if count<10: spase = " "
        else: spase = ''
        print(f"[{count}] {spase}", end=' ')
        print(f"{rate_dict.get(oil, '0')}/10", end=' ')
        beauty_print(oil)

def max_length(array):
    """Search element with maximum lenght."""
    mL = 0
    try: # if list
        for i in array:
            if len(i) > mL: mL = len(i)
    except: # if dictionary
        length = [key for (key, value) in array.items()]
        for i in length:
            if len(i) > mL: mL = len(i)
    return mL

def lang():
    """Choose program language."""
    print("""
    Choose the choise / Выберете язык
    [E] - English
    [R] - Russian
    """)
    choise = input("")
    if choise == 'r' or choise == 'R':
        import localisations.RUS as language
        try: import localisations.suggestions_RU
        except: print("Здравствуте!")
    elif choise == 'e' or choise == 'E':
        import localisations.EN as language
    return language


def MainMeny(choise):
    """
    This is the main meny of it program.
    You can go to "Collections" sub-meny, or working here.
    """

    if (choise == 'с' or choise == 'С' or
        choise == 'c' or choise == 'C'):
        # Creation of new recipe.
        base = data('data/base.txt')
        name = input("Название рецепта: ")
        ingredient_list = {}
        while True:
            ingredient = input("Введите ингредиет (ENTER для отмены): ")
            if ingredient == '': break
            drop = input("количество капель: ")
            ingredient_list[ingredient] = drop
        base[name] = ingredient_list
        save_data("data/base.txt", base)
        print(f"\nРецепт записан в базу.\n")
        print(LG.mini_main)
    elif (choise == 'п' or choise == 'П' or
          choise == 's' or choise == 'S'):
          # Output all recipes.
        recipes()
        print(LG.mini_main)
    elif (choise == 'у' or choise == 'У' or
          choise == 'r' or choise == 'R'):
          # Delete recipe.
        keys = sorted(data('data/base.txt'))
        choise = int(input("Введите номер рецепта, который необходимо удалить: "))
        delete("data/base.txt", keys[choise - 1])
        delete("data/rate.txt", keys[choise - 1])
        print(f"\nРецепт '{keys[choise - 1]}' удален.\n")
        print(LG.mini_main)
    elif (choise == 'в' or choise == 'В' or
          choise == 'i' or choise == 'I'):
          # Otput recipes avaliable to make only.
        coll = data('data/collection.txt')
        base = data('data/base.txt')
        # Search ingredient from base in list.
        main_flag = True
        for name in base:
            flag = True
            for ing in list(base[name].keys()):
                if ing not in coll: flag = False
            if flag:
                main_flag = False
                beauty_print(name)
        if main_flag:
            print("\nПохоже, что у Вас ни на что не хватает ингредиентов :'(\n")
        print(LG.mini_main)
    elif (choise == 'р' or choise == 'Р' or
          choise == 'g' or choise == 'G'):
          # Give rate to recipe.
        try: rate_dict = data('data/rate.txt')
        except: rate_dict = {}
        keys = sorted(data('data/base.txt'))
        choise = int(input("Ведите номер рецепта: "))
        rate = input("Введите оценку (из 10-ти): ")
        rate_dict[keys[choise - 1]] = rate
        save_data('data/rate.txt', rate_dict)
        print(LG.mini_main)
    elif (choise == 'з' or choise == 'З' or
          choise == 'e' or choise == 'E'): sys.exit()
          # Exit program.
    elif (choise == 'к' or choise == 'К' or
          choise == 'o' or choise == 'O'):
        print(LG.collection_meny)
        collection()
        while True:
            choise = input()
            if (choise == 'м' or choise == 'М' or
                choise == 'm' or choise == 'M'):
                print(LG.main_meny)
                break
                # Return in main meny.
            CollectionMeny(choise)


def CollectionMeny(choise):
    """
    This is the Collection meny of program.
    Here you can working with your collection.
    """
    if (choise == 'к' or choise == 'К' or
        choise == 'o' or choise == 'O'): collection()
          # Print mini collection meny.
    elif (choise == 'у' or choise == 'У' or
          choise == 'r' or choise == 'R'):
          # Delete ingredient from collection.
        coll = sorted(data('data/collection.txt'))
        n = int(input("Введите номер удаляемого ингридиента: "))
        delete = coll[n - 1]
        delete("data/collection.txt", delete)
        collection()
        print(f"\nИнгридиент '{delete}' удален.")
        print(LG.mini_collection)
    elif (choise == 'д' or choise == 'Д' or
          choise == 'a' or choise == 'A'):
          # Add ingredient to collection.
        list_of_recipes = data('data/collection.txt')
        list_of_recipes.append(input("Введите название ингредиента: "))
        save_data('data/collection.txt', list_of_recipes)
        print()
        collection()
        print(LG.mini_collection)
    elif (choise == 'н' or choise == 'Н' or
          choise == 'f' or choise == 'F'):
          # Search recipe with the ingredient.
        base = data('data/base.txt')
        coll = sorted(data('data/collection.txt'))
        n = int(input("Введите номер ингредиента: "))
        search = coll[n - 1]
        print(f"\nРецепты, содержащие '{search}':\n")
        # Create list of keys from our base with the ingredient.
        list_of_recipes_names = [keyg for (keyg, value) in
                                base.items() if search in value]
        sortList = sorted(list_of_recipes_names)
        for name in sortList:
            beauty_print(name)
        print(LG.mini_collection)
    elif (choise == 'о' or choise == 'О' or
          choise == 's' or choise == 'S'):
          # Otput list of all ingredients from recipes.
        base = data('data/base.txt')
        list_of_ingredients = []
        # List from all igredients from recipes.
        for i in base:
            list_of_ingredients += list(base[i].keys())
        # Count number of ingredientsself.
        ingredients_counter = {i: list_of_ingredients.count(i)
                               for i in list_of_ingredients}
        # Grouped elements for sequenses.
        reverse_counter = {}
        for k, v in ingredients_counter.items():
            reverse_counter[v] = reverse_counter.get(v, [])
            reverse_counter[v].append(k)
        # Make sorted list.
        priority = list(reversed(sorted([key for (key, value) in
                                         reverse_counter.items()])))
        # Check aveliability of element from collection.
        for position in priority:
            for ingredient in reverse_counter[position]:
                print(f"""\
{ingredient}{(max_length(list_of_ingredients) - len(ingredient) + 1) * ' '}\
(в {position} рецептах)\
""", end=' ')
                if ingredient not in data('data/collection.txt'):
                    print(" - отсутствует в коллекции.")
                else: print()
        print(LG.mini_collection)
    elif (choise == 'з' or choise == 'З' or
          choise == 'e' or choise == 'E'): sys.exit()
          # Exit program.
    else: print("Такого варианта нет, введите команду правильно\n")


if __name__ == '__main__':
    LG = lang() # localisation language
    print(LG.main_meny) # output main meny of program
    while True:
        choise = input()
        MainMeny(choise)
