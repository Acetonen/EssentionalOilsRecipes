#!/usr/bin/env python3

import sys
import shelve
import os
import sys
#PEP8

class Recipe:
    """Class contain all information about recipes, oils, raiting."""
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
            self.creation_recipe()
        elif choise in ['s', 'S', 'п', 'П']:
              # Output all recipes.
            self.recipes()
        elif choise in ['r', 'R', 'у', 'У']:
              # Delete recipe.
            self.delete_recipe()
        elif choise in ['i', 'I', 'в', 'В']:
              # Otput recipes avaliable to make only.
            self.available_recipe()
        elif choise in ['g', 'G', 'р', 'Р']:
              # Give rate to recipe.
            self.recipe_rate()
        elif choise in ['e', 'E', 'з', 'З']:
              # Exit program.
              sys.exit()
        elif choise in ['o', 'O', 'к', 'К']:
              # Open collection meny.
            collection()
            while True:
                choise = input()
                if   choise in ['m', 'M', 'м', 'М']:
                    # Return in main meny.
                    print(LG.main_meny)
                    break
                CollectionMeny(choise)


    def recipes(self):
        """ Print sorted recipes collection"""
        base = shelve.open(resipe_path)
        keys = sorted(base)
        for count, recipe in enumerate(keys, 1):
            print(f"[{count}] {base[recipe]}")
        print('\n', LG.mini_main)
        base.close()

    def creation_recipe(self):
        """Creation of new recipe."""
        base = shelve.open(resipe_path)
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
        base = shelve.open(resipe_path)
        keys = sorted(base)
        choise = int(input("Input nubmber of recipe to delete: "))
        base.pop(keys[choise - 1], None)
        print(f"\nRecipe '{keys[choise - 1]}' deleted.\n")
        print(LG.mini_main)
        base.close()

    def available_recipe(self):
        """Otput recipes avaliable to make only."""
        coll = shelve.open(collection_path)
        base = shelve.open(resipe_path)
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
            collection()
        elif choise in ['r', 'R', 'у', 'У']:
              # Delete ingredient from collection.
            self.delete_ingredient()
        elif choise in ['a', 'A', 'д', 'Д']:
              # Add ingredient to collection.
            self.add_ingredient()
        elif choise in ['f', 'F', 'н', 'Н']:
              # Search recipe with the ingredient.
            self.rec_with_ing()
        elif choise in ['s', 'S', 'о', 'О']:
              # Otput list of all ingredients from recipes.
            self.ing_from_rec()
        elif choise in ['e', 'E', 'з', 'З']:
              # Exit program.
            sys.exit()
        else:
            print("There is no such option, input letter correctly\n")

    def delete_ingredient(self):
        """Delete ingredient from collection."""
        coll = shelve.open(collection_path)
        coll_sort = sorted(coll)
        n = int(input("Input number of deleted oil: "))
        coll.pop(coll_sort[n - 1])
        coll.close()
        collection()
        print(f"\nOil '{coll_sort[n - 1]}' deleted.")
        print(LG.mini_collection)

    def add_ingredient(self):
        """Add ingredient to collection."""
        coll = shelve.open(collection_path)
        ing = input("Input oil name: ")
        coll[ing] = Oil(ing, 0)
        coll.close()
        print()
        collection()
        print(LG.mini_collection)


    def ing_from_rec(self):
        """Otput list of all ingredients from recipes."""
        base = shelve.open(resipe_path)
        coll = shelve.open(collection_path)
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
        base = shelve.open(resipe_path)
        coll = shelve.open(collection_path)
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

def collection():
    """Otput numbered and sorted igredient collection."""
    print(LG.collection_meny)
    coll = shelve.open(collection_path)
    coll_sort = sorted(coll)
    print("My collection:")
    for count, oil in enumerate(coll_sort,1):
        print(f"[{count}] {oil}")
    print()
    coll.close()

def data_path(relative_path):
    """Make absolyte path of database file."""
    script_name = sys.argv[0]
    script_path = os.path.dirname(script_name)
    absolute_path = os.path.abspath(script_path)
    path_list = absolute_path.split(os.sep)
    path_list.extend(relative_path)
    os_path = os.path.join(os.sep, *path_list)
    return os_path

global resipe_path, collection_path
resipe_path = data_path(['data', 'resipe_class'])
collection_path = data_path(['data', 'collection_class'])

# Program skeleton
#==============================================================================
if __name__ == '__main__':
    # print(resipe_path)
    LG = lang()   # Localisation language
    print(LG.main_meny)  # Output main meny of program
    while True:
        choise = input()
        MainMeny(choise)
