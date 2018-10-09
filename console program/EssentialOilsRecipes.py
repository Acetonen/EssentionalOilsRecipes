import sys
import pickle
#PEP8


# Main classes
#==============================================================================
class MainMeny:
    """    This is the main meny of it program.
    You can go to "Collections" sub-meny, or working here.
    """


    def __init__(self, choise):

        if (choise == 'с' or choise == 'С' or
            choise == 'c' or choise == 'C'):
            # Creation of new recipe.
            self.creation_recipe()
        elif (choise == 'п' or choise == 'П' or
              choise == 's' or choise == 'S'):
              # Output all recipes.
            self.recipes()
        elif (choise == 'у' or choise == 'У' or
              choise == 'r' or choise == 'R'):
              # Delete recipe.
            self.delete_recipe()
        elif (choise == 'в' or choise == 'В' or
              choise == 'i' or choise == 'I'):
              # Otput recipes avaliable to make only.
            self.available_recipe()
        elif (choise == 'р' or choise == 'Р' or
              choise == 'g' or choise == 'G'):
              # Give rate to recipe.
            self.recipe_rate()
        elif (choise == 'з' or choise == 'З' or
              choise == 'e' or choise == 'E'):
              # Exit program.
              sys.exit()
        elif (choise == 'к' or choise == 'К' or
              choise == 'o' or choise == 'O'):
              # Open collection meny.
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

    def recipes(self):
        """ Print sorted recipes collection"""

        try: rate_dict = data('data/rate_bin')
        except: rate_dict = {}
        base = data('data/base_bin')
        keys = sorted(base)
        for count, oil in enumerate(keys,1):
            # Ensert some spaces after recite nubber.
            if count<10: spase = " "
            else: spase = ''
            print(f"[{count}] {spase}", end=' ')
            print(f"{rate_dict.get(oil, '0')}/10", end=' ')
            beauty_print(oil)
        print('\n', LG.mini_main)

    def creation_recipe(self):
        """Creation of new recipe."""

        base = data('data/base_bin')
        name = input("Название рецепта: ")
        ingredient_list = {}
        while True:
            ingredient = input("Введите ингредиет (ENTER для отмены): ")
            if ingredient == '': break
            drop = input("количество капель: ")
            ingredient_list[ingredient] = drop
        base[name] = ingredient_list
        save_data("data/base_bin", base)
        print(f"\nРецепт записан в базу.\n")
        print(LG.mini_main)

    def delete_recipe(self):
        """Delete recipe from th base."""

        keys = sorted(data('data/base_bin'))
        choise = int(input("Введите номер рецепта, который необходимо удалить: "))
        delete("data/base_bin", keys[choise - 1])
        delete("data/rate_bin", keys[choise - 1])
        print(f"\nРецепт '{keys[choise - 1]}' удален.\n")
        print(LG.mini_main)

    def available_recipe(self):
        """Otput recipes avaliable to make only."""

        coll = data('data/collection_bin')
        base = data('data/base_bin')
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
        print('\n', LG.mini_main)

    def recipe_rate(self):
        """Give rate to recipe."""

        try: rate_dict = data('data/rate_bin')
        except: rate_dict = {}
        keys = sorted(data('data/base_bin'))
        choise = int(input("Ведите номер рецепта: "))
        rate = input("Введите оценку (из 10-ти): ")
        rate_dict[keys[choise - 1]] = rate
        save_data('data/rate_bin', rate_dict)
        print(LG.mini_main)


class CollectionMeny:
    """
    This is the Collection meny of program.
    Here you can working with your collection.
    """

    def __init__(self, choise):

        if (choise == 'к' or choise == 'К' or
            choise == 'o' or choise == 'O'):
              # Print mini collection meny.
            collection()
        elif (choise == 'у' or choise == 'У' or
              choise == 'r' or choise == 'R'):
              # Delete ingredient from collection.
            self.delete_ingredient()
        elif (choise == 'д' or choise == 'Д' or
              choise == 'a' or choise == 'A'):
              # Add ingredient to collection.
            self.add_ingredient()
        elif (choise == 'н' or choise == 'Н' or
              choise == 'f' or choise == 'F'):
              # Search recipe with the ingredient.
            self.rec_with_ing()
        elif (choise == 'о' or choise == 'О' or
              choise == 's' or choise == 'S'):
              # Otput list of all ingredients from recipes.
            self.ing_from_rec()
        elif (choise == 'з' or choise == 'З' or
              choise == 'e' or choise == 'E'):
              # Exit program.
              sys.exit()
        else: print("Такого варианта нет, введите команду правильно\n")

    def delete_ingredient(self):
        """Delete ingredient from collection."""

        coll = sorted(data('data/collection_bin'))
        n = int(input("Введите номер удаляемого ингридиента: "))
        del_ing = coll[n - 1]
        delete("data/collection_bin", del_ing)
        collection()
        print(f"\nИнгридиент '{del_ing}' удален.")
        print(LG.mini_collection)

    def add_ingredient(self):
        """Add ingredient to collection."""

        list_of_recipes = data('data/collection_bin')
        list_of_recipes.append(input("Введите название ингредиента: "))
        save_data('data/collection_bin', list_of_recipes)
        print()
        collection()
        print(LG.mini_collection)

    def ing_from_rec(self):
        """Otput list of all ingredients from recipes."""

        base = data('data/base_bin')
        list_of_ingredients = []
        # List from all igredients from recipes.
        for i in base:
            list_of_ingredients += list(base[i].keys())
        # Count number of ingredients.
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
                if ingredient not in data('data/collection_bin'):
                    print(" - отсутствует в коллекции.")
                else: print()
        print(LG.mini_collection)

    def rec_with_ing(self):
        """Search recipe with the ingredient."""

        base = data('data/base_bin')
        coll = sorted(data('data/collection_bin'))
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


# Support functions.
#==============================================================================

def data(file_name):
    """Load base or collection from file."""

    with open(file_name, 'rb') as file:
        data = pickle.load(file)
    return data

def save_data(file_name, data):
    """Dump base or collection in file."""

    with open(file_name, 'wb') as file:
        pickle.dump(data, file)

def delete(file_name, delete):
    """Delete ingredient or recipe from base."""

    with open(file_name, "rb+") as file:
        base = pickle.load(file)
        # Different ways to list and dictionary.
        try: base.pop(delete, None)
        except: base.remove(delete)
        file.seek(0)
        file.truncate()
        pickle.dump(base, file)

def beauty_print(name):
    """Structural output of recipes."""

    base = data('data/base_bin')
    print(f"{name}{(max_length(base) - len(name) + 1)*' '}", end=': ')
    for key in base[name]:
        print(f"{key} - {base[name][key]}к;", end=' ')
    print()

def max_length(array):
    """Search element with maximum lenght."""

    max_length = 0
    try: # if list
        for i in array:
            if len(i) > max_length: max_length = len(i)
    except: # if dictionary
        length = [key for (key, value) in array.items()]
        for i in length:
            if len(i) > max_length: max_length = len(i)
    return max_length

def lang():
    """Choose program language."""

    print("""
    Choose the choise / Выберете язык
    [E]/[А] - English
    [R]/[Р] - Russian
    """)
    choise = input("")
    if (choise == 'r' or choise == 'R' or
        choise == 'р' or choise == 'Р'):
        import localisations.RUS as language
        try: import localisations.suggestions_RU
        except: print("Здравствуте!")
    elif (choise == 'e' or choise == 'E' or
          choise == 'а' or choise == 'А'):
        import localisations.EN as language
    return language

def collection():
    """Otput numbered and sorted igredient collection."""

    print(LG.collection_meny)
    coll = sorted(data('data/collection_bin'))
    print("Моя коллекция:")
    for count, oil in enumerate(coll,1):
        print(f"[{count}] {oil}")
    print()


# Program skeleton
#==============================================================================
if __name__ == '__main__':
    LG = lang() # localisation language
    print(LG.main_meny) # output main meny of program
    while True:
        choise = input()
        MainMeny(choise)
