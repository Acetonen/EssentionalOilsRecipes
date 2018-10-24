#!/usr/bin/env python3

import sys
import shelve
import os
import sys
#PEP8

class Recipe:
    """Class contain name of recipe, containing oils, recipe raiting."""
    def __init__(self, name, oil, rating):
        self.name = name
        self.oils = oil
        self.rating = rating
    def __str__(self):
        """Beauty output of classs objects"""
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
        """Pretty print of Oil object"""
        return ('{0} - {1} drops'.format(self.oil_name, self.volume))


# Main classes
#==============================================================================
class MainMeny:
    """
    This is the main meny of it program.
    You can go to "Collections" sub-meny, or working here.
    """
    def __init__(self, choise):
        if choise in ['c', 'C', 'с', 'С']:
            # Creation of new recipe.
            self.create_recipe()
        elif choise in ['s', 'S', 'п', 'П']:
              # Output all recipes.
            self.show_all_recipes()
        elif choise in ['r', 'R', 'у', 'У']:
              # Delete recipe.
            self.delete_recipe()
        elif choise in ['i', 'I', 'в', 'В']:
              # Otput recipes avaliable to make only.
            self.show_available_recipe()
        elif choise in ['g', 'G', 'р', 'Р']:
              # Give rate to recipe.
            self.give_rating()
        elif choise in ['e', 'E', 'з', 'З']:
              # Exit program.
              sys.exit()
        elif choise in ['o', 'O', 'к', 'К']:
              # Open collection meny.
            show_oils_collection()
            while True:
                choise = input()
                if   choise in ['m', 'M', 'м', 'М']:
                    # Return in main meny.
                    print(LG.main_meny)
                    break
                CollectionMeny(choise)


    def show_all_recipes(self):
        """ Print sorted recipes collection"""
        base = shelve.open(resipe_path)
        keys = sorted(base)
        for count, recipe in enumerate(keys, 1):
            print(f"[{count}] {base[recipe]}")
        print('\n', LG.mini_main)
        base.close()

    def create_recipe(self):
        """Create new recipe."""
        base = shelve.open(resipe_path)
        name = input("Recipe name: ")
        ingredient_list = {}
        while True:
            ingredient = input("Input oil (ENTER for cancel): ")
            if ingredient == '': break
            ingredient_list[ingredient] = Oil(ingredient,
                                              int(input("number of drops: ")))
        base[name] = Recipe(name, ingredient_list, 0)
        print(f"\nRecipe saved in base.\n")
        print(LG.mini_main)
        base.close()

    def delete_recipe(self):
        """Delete recipe from base."""
        base = shelve.open(resipe_path)
        keys = sorted(base)
        choise = int(input("Input nubmber of recipe to delete: "))
        base.pop(keys[choise - 1], None)
        print(f"\nRecipe '{keys[choise - 1]}' deleted.\n")
        print(LG.mini_main)
        base.close()

    def show_available_recipe(self):
        """Otput recipes avaliable to make only."""
        collection = shelve.open(collection_path)
        base = shelve.open(resipe_path)
        # Search ingredient from base in list.
        main_flag = True
        for name in base:
            flag = True
            for ingredient in list(base[name].oils):
                if ingredient not in collection: flag = False
            if flag:
                main_flag = False
                print(base[name])
        if main_flag:
            print("\nSeems like you havn't enough oils for any recipe :'(\n")
        print('\n', LG.mini_main)
        collection.close()
        base.close()

    def give_rating(self):
        """Give rating to recipe."""
        base = shelve.open(resipe_path)
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
        if choise in ['o', 'O', 'к', 'К']:
              # Print mini collection meny.
            show_oils_collection()
        elif choise in ['r', 'R', 'у', 'У']:
              # Delete ingredient from collection.
            self.delete_ingredient()
        elif choise in ['a', 'A', 'д', 'Д']:
              # Add ingredient to collection.
            self.add_ingredient()
        elif choise in ['f', 'F', 'н', 'Н']:
              # Search recipe with the ingredient.
            self.show_recipe_with_choosen_ingredient()
        elif choise in ['s', 'S', 'о', 'О']:
              # Otput list of all ingredients from recipes.
            self.show_missing_ingredients()
        elif choise in ['e', 'E', 'з', 'З']:
              # Exit program.
            sys.exit()
        else:
            print("There is no such option, input letter correctly\n")

    def delete_ingredient(self):
        """Delete ingredient from collection."""
        collection = shelve.open(collection_path)
        collection_sort = sorted(collection)
        n = int(input("Input number of deleted oil: "))
        collection.pop(collection_sort[n - 1])
        collection.close()
        show_oils_collection()
        print(f"\nOil '{collection_sort[n - 1]}' deleted.")
        print(LG.mini_collection)

    def add_ingredient(self):
        """Add ingredient to collection."""
        collection = shelve.open(collection_path)
        ing = input("Input oil name: ")
        collection[ing] = Oil(ing, 0)
        collection.close()
        print()
        show_oils_collection()
        print(LG.mini_collection)


    def show_missing_ingredients(self):
        """Otput list of all ingredients from recipes and show missing."""
        base = shelve.open(resipe_path)
        collection = shelve.open(collection_path)
        list_of_ingredients = []
        # List from all igredients from recipes.
        for i in base:
            list_of_ingredients += list(base[i].oils.keys())
        # Count number of ingredients.
        ingredients_counter = {i: list_of_ingredients.count(i)
                               for i in list_of_ingredients}
        # Revert keys and values.
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
{ingredient}{(find_max_length(list_of_ingredients) - len(ingredient) + 1) * ' '}\
(in {position} recipes)\
""", end=' ')
                if ingredient in collection:
                    print(" - in collection.")
                else: print()
        print(LG.mini_collection)
        base.close()
        collection.close()

    def show_recipe_with_choosen_ingredient(self):
        """Search recipe with the ingredient."""
        base = shelve.open(resipe_path)
        collection = shelve.open(collection_path)
        collection_sort = sorted(collection)
        n = int(input("Input ingredient number: "))
        print(f"\nRecipes contane '{collection_sort[n-1]}':\n")
        list_of_recipes_names = []
        for recipe in base:
            if collection_sort[n-1] in base[recipe].oils:
                list_of_recipes_names.append(base[recipe].name)
        sort_list = sorted(list_of_recipes_names)
        for name in sort_list:
            print(base[name])
        if list_of_recipes_names == []:
            print('There is no ricept with this oil.')
        print(LG.mini_collection)
        base.close()
        collection.close()


# Support functions.
#==============================================================================

def find_max_length(array):
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

def choose_language():
    """Choose program language."""
    print("""
    Choose the choise / Выберете язык
    [E]/[А] - English
    [R]/[Р] - Russian
    """)
    while True:
        choise = input("")
        if choise in ['r', 'R', 'р', 'Р']:
            import localisations.RUS as language
            try:
                from localisations.suggestions_RU import Suggestion
                Suggestion(resipe_path)
                break
            except:
                raise
        elif choise in ['e', 'E', 'а', 'А']:
            import localisations.EN as language
            break
        else:
            print("There is no such option, input letter correctly\n")
    return language

def show_oils_collection():
    """Otput numbered and sorted igredient collection."""
    print(LG.collection_meny)
    collection = shelve.open(collection_path)
    collection_sort = sorted(collection)
    print("My collection:")
    for count, oil in enumerate(collection_sort,1):
        print(f"[{count}] {oil}")
    print()
    collection.close()

def make_absolyte_path(relative_path):
    """Make absolyte path of database file."""
    script_name = sys.argv[0]
    script_path = os.path.dirname(script_name)
    absolute_path = os.path.abspath(script_path)
    os_path = os.path.join(absolute_path, *relative_path)
    return os_path

global resipe_path, collection_path
resipe_path = make_absolyte_path(['data', 'resipe_class'])
collection_path = make_absolyte_path(['data', 'collection_class'])

# Program skeleton
#==============================================================================
if __name__ == '__main__':
    LG = choose_language()   # Localisation language
    sys.stdout.write(LG.main_meny)  # Output main meny of program
    while True:
        choise = sys.stdin.readline()[:-1]
        MainMeny(choise)
