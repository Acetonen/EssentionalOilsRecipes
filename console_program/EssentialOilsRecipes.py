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
            print('\n', LG.collection_meny)
            show_oils_collection()
            while True:
                choise = input()
                CollectionMeny(choise)
                if choise in ['m', 'M', 'м', 'М']:
                    # Return in main meny.
                    print(LG.main_meny)
                    break
        else:
            print("There is no such option, input letter correctly\n")
        print('\n', LG.mini_main)


    def show_all_recipes(self):
        """ Print sorted recipes collection"""
        base = shelve.open(resipe_path)
        sorted_base = sorted(base)
        for count, recipe in enumerate(sorted_base, 1):
            print(f"[{count}] {base[recipe]}")
        base.close()

    def create_recipe(self):
        """Create new recipe."""
        name = input("Recipe name: ")
        if name:
            base = shelve.open(resipe_path)
            oils_list = {}
            while True:
                oil = input("Input oil (ENTER for cancel): ")
                if not oil: break
                drops = input("number of drops: ")
                try:
                    drops = int(drops)
                except:
                    print("You must input NUMBER.")
                    break
                oils_list[ingredient] = Oil(oil, drops)
            base[name] = Recipe(name, oils_list, 0)
            print(f"\nRecipe saved in base.\n")
            base.close()
        else:
            print("\nYou skip recipe creation.\n")

    def delete_recipe(self):
        """Delete recipe from base."""
        choise = input("Input nubmber of recipe to delete: ")
        try:
            choise = int(choise)
            base = shelve.open(resipe_path)
            keys = sorted(base)
            base.pop(keys[choise - 1], None)
            base.close()
            print(f"\nRecipe '{keys[choise - 1]}' deleted.\n")
        except:
            print("\nYou must input NUMBER of recipe in list.\n")

    def show_available_recipe(self):
        """Otput recipes avaliable to make only."""
        collection = sorting_from_file(collection_path)
        base = shelve.open(resipe_path)
        # Search ingredient from base in list.
        not_enough_oils = True
        for recipe in base:
            avaliable_recipe = True
            for oil in list(base[recipe].oils):
                if oil not in collection:
                    avaliable_recipe = False
            if avaliable_recipe:
                not_enough_oils = False
                print(base[recipe])
        base.close()
        if not_enough_oils:
            print("\nSeems like you havn't enough oils for any recipe :'(\n")

    def give_rating(self):
        """Give rating to recipe."""
        choise = input("Input nubmber of recipe: ")
        rating = input("Input rating (0 - 10): ")
        try:
            choise = int(choise)
            rating = int(rating)
            base = shelve.open(resipe_path)
            sorted_base = sorted(base)
            recipe = base[sorted_base[choise - 1]]
            if rating in range(11):
                recipe.rating = rating
            else: print("Rating must be in range 0-10!")
            base[sorted_base[choise - 1]] = recipe
            base.close()
        except:
            print("\nYou must input NUMBER.\n")


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
        print(LG.mini_collection)


    def delete_ingredient(self):
        """Delete ingredient from collection."""
        choise = input("Input number of deleted oil: ")
        try:
            choise = int(choise)
            collection = shelve.open(collection_path)
            collection_sort = sorted(collection)
            collection.pop(collection_sort[choise - 1])
            collection.close()
            print(f"\nOil '{collection_sort[choise - 1]}' deleted.")
        except:
            print("\nYou must input NUMBER of oil in list.\n")
        show_oils_collection()

    def add_ingredient(self):
        """Add ingredient to collection."""
        ingredient = input("Input oil name: ")
        if ingredient:
            collection = shelve.open(collection_path)
            collection[ingredient] = Oil(ingredient, 0)
            collection.close()
        else:
            print("\nYou skip oil adding.\n")
        print(f"\nOil saved in collection.\n")
        show_oils_collection()

    def show_missing_ingredients(self):
        """Otput list of all ingredients from recipes and show missing."""
        popularity_blocks, list_of_all_oils = self.create_dict_oils_popularity()
        longest_oil_name = find_max_length(list_of_all_oils)
        # Make sorted list by oil popularity.
        priority = sorted(popularity_blocks)[::-1]
        # Check aveliability of ingredients from collection.
        for position in priority:
            for ingredient in popularity_blocks[position]:
                print(f"""\
{ingredient}{(longest_oil_name - len(ingredient)+1) * ' '}\
(in {position} recipes)\
""", end=' ')
                collection = sorting_from_file(collection_path)
                if ingredient in collection:
                    print(" - in collection.")
                else: print()

    def create_dict_oils_popularity(self):
        """
        Create dictionary where keys are number in recipes, values are
        ingredients.
        """
        base = shelve.open(resipe_path)
        list_of_all_recipes_oils = []
        for recipe in base:
            list_of_all_recipes_oils += list(base[recipe].oils.keys())
        base.close()
        # Count number of ingredients.
        oils_popularity = {oil: list_of_all_recipes_oils.count(oil)
                               for oil in list_of_all_recipes_oils}
        # Creates blocks of popularity.
        popularity_blocks = {}
        for popularity, oils in oils_popularity.items():
            popularity_blocks[oils] = popularity_blocks.get(oils, [])
            popularity_blocks[oils].append(popularity)
        return popularity_blocks, list_of_all_recipes_oils

    def show_recipe_with_choosen_ingredient(self):
        """Search recipe with the ingredient."""
        choise = input("Input ingredient number: ")
        try:
            choise = int(choise)
            base = shelve.open(resipe_path)
            collection = sorting_from_file(collection_path)
            print(f"\nRecipes contane '{collection[choise-1]}':\n")
            list_of_recipes_names = []
            for recipe in base:
                if collection[choise-1] in base[recipe].oils:
                    list_of_recipes_names.append(base[recipe].name)
            base.close()
            sort_list = sorted(list_of_recipes_names)
            for name in sort_list:
                print(base[name])
            if list_of_recipes_names == []:
                print('There is no ricept with this oil.')
        except:
            print("\nYou must input NUMBER of oil in list.\n")


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
            from localisations.suggestions_RU import Suggestion
            Suggestion(resipe_path)
            break
        elif choise in ['e', 'E', 'а', 'А']:
            import localisations.EN as language
            break
        else:
            print("There is no such option, input letter correctly\n")
    return language

def show_oils_collection():
    """Otput numbered and sorted igredient collection."""
    collection = sorting_from_file(collection_path)
    print("My collection:")
    for count, oil in enumerate(collection,1):
        print(f"[{count}] {oil}")

def sorting_from_file(path):
    """Sorting data from file"""
    data = shelve.open(path)
    data_sort = sorted(data)
    data.close()
    return data_sort

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
