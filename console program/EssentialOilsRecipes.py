import sys
import shelve
import pprint
#PEP8

class Recipe:
    """Class contain oll information about recipes, oils, raiting."""

    def __init__(self, name, oil, rating):
        self.name = name
        self.oils = oil
        self.rating = rating
    def __str__(self):
        oils_print = ''
        for oil in self.oils:
            s = f"{self.oils[oil].oil_name} - {str(self.oils[oil].volume)}drop"
            oils_print = oils_print + s +'; '
        return ('{0} \n\trating: ({1}/10) \n\tcomposition: {2}'.format(
                self.name, self.rating, oils_print))


class Oil:
    """Information about essential oils."""

    def __init__(self, name, volume):
        self.oil_name = name
        self.volume = volume
    def __str__(self):
        return ('{0} - {1} drops'.format(self.oil_name, self.volume))


# Main classes
#==============================================================================
class MainMeny:
    """
    This is the main meny of it program.
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

        base = shelve.open('data/resipe_class')
        keys = sorted(base)
        for count, oil in enumerate(keys, 1):
            print(f"[{count}] {base[oil]}")
        print('\n', LG.mini_main)
        base.close()

    def creation_recipe(self):
        """Creation of new recipe."""

        base = shelve.open('data/resipe_class')
        name = input("Recipe name: ")
        ing_list = {}
        while True:
            ing = input("Input oil (ENTER for cancel): ")
            if ing == '': break
            ing_list[ing] = Oil(ing ,int(input("number of drops: ")))
        base[name] = Recipe(name, ing_list, 0)
        print(f"\nRecipe saved in base.\n")
        print(LG.mini_main)
        base.close()

    def delete_recipe(self):
        """Delete recipe from th base."""

        base = shelve.open('data/resipe_class')
        keys = sorted(base)
        choise = int(input("Input nubmber of recipe to delete: "))
        base.pop(keys[choise - 1], None)
        print(f"\nRecipe '{keys[choise - 1]}' deleted.\n")
        print(LG.mini_main)
        base.close()

    def available_recipe(self):
        """Otput recipes avaliable to make only."""

        coll = shelve.open('data/collection_class')
        base = shelve.open('data/resipe_class')
        # Search ingredient from base in list.
        main_flag = True
        for name in base:
            flag = True
            for ing in list(base[name].oils):
                if ing not in coll: flag = False
            if flag:
                main_flag = False
                print(base[name])
        if main_flag:
            print("\nSeems like you havn't enough oils for any recipe :'(\n")
        print('\n', LG.mini_main)
        coll.close()
        base.close()

    def recipe_rate(self):
        """Give rate to recipe."""

        base = shelve.open('data/resipe_class')
        keys = sorted(base)
        choise = int(input("Input number of recipe: "))
        recipe = base[keys[choise - 1]]
        recipe.rating = int(input("Input rating (from 10): "))
        base[keys[choise - 1]] = recipe
        print(LG.mini_main)
        base.close()


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
        else: print("There is no such option, input letter correctly\n")

    def delete_ingredient(self):
        """Delete ingredient from collection."""

        coll = shelve.open('data/collection_class')
        coll_sort = sorted(coll)
        n = int(input("Input number of deleted oil: "))
        coll.pop(coll_sort[n - 1])
        coll.close()
        collection()
        print(f"\nOil '{coll_sort[n - 1]}' deleted.")
        print(LG.mini_collection)

    def add_ingredient(self):
        """Add ingredient to collection."""

        coll = shelve.open('data/collection_class')
        ing = input("Input oil name: ")
        coll[ing] = Oil(ing, 0)
        coll.close()
        print()
        collection()
        print(LG.mini_collection)


    def ing_from_rec(self):
        """Otput list of all ingredients from recipes."""

        base = shelve.open('data/resipe_class')
        coll = shelve.open('data/collection_class')
        list_of_ingredients = []
        # List from all igredients from recipes.
        for i in base:
            list_of_ingredients += list(base[i].oils.keys())
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
(in {position} recipes)\
""", end=' ')
                if ingredient not in coll:
                    print(" - not in collection.")
                else: print()
        print(LG.mini_collection)
        base.close()
        coll.close()

    def rec_with_ing(self):
        """Search recipe with the ingredient."""

        base = shelve.open('data/resipe_class')
        coll = shelve.open('data/collection_class')
        coll_sort = sorted(coll)
        n = int(input("Input ingredient number: "))
        print(f"\nRecipes contane '{coll_sort[n-1]}':\n")
        list_of_recipes_names = []
        for recipe in base:
            if coll_sort[n-1] in base[recipe].oils:
                list_of_recipes_names.append(base[recipe].name)
        sort_list = sorted(list_of_recipes_names)
        for name in sort_list:
            print(base[name])
        if list_of_recipes_names == []:
            print('There is no ricept with this oil.')
        print(LG.mini_collection)
        base.close()
        coll.close()


# Support functions.
#==============================================================================

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
        except: print("Hello World!!")
    elif (choise == 'e' or choise == 'E' or
          choise == 'а' or choise == 'А'):
        import localisations.EN as language
    return language

def collection():
    """Otput numbered and sorted igredient collection."""

    print(LG.collection_meny)
    coll = shelve.open('data/collection_class')
    coll_sort = sorted(coll)
    print("My collection:")
    for count, oil in enumerate(coll_sort,1):
        print(f"[{count}] {oil}")
    print()
    coll.close()


# Program skeleton
#==============================================================================
if __name__ == '__main__':
    LG = lang() # localisation language
    print(LG.main_meny) # output main meny of program
    while True:
        choise = input()
        MainMeny(choise)
