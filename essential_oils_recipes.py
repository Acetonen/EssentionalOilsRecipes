#!/usr/bin/env python3
"""Program for store recipes for aroma lamps"""

import sys
import shelve
import os
import localisations.suggestions_ru as suggest


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
            string = "{} - {}drop".format(
                self.oils[oil].oil_name, str(self.oils[oil].volume))
            oils_print = oils_print + string + '; '
        return ('{0} \n\trating: ({1}/10) \n\tcomposition: {2}'.format(
            self.name, self.rating, oils_print))


class Oil:
    """Information about essential oils."""
    def __init__(self, name, volume):
        self.oil_name = name
        self.volume = volume

    def __str__(self):
        """Pretty print of Oil object"""
        return '{0} - {1} drops'.format(self.oil_name, self.volume)


def show_all_recipes():
    """ Print sorted recipes collection"""
    sorted_base = sorted(BASE)
    for count, recipe in enumerate(sorted_base, 1):
        print("[{}] {}".format(count, BASE[recipe]))


def create_recipe():
    """Create new recipe."""
    recipe_name = input("Recipe name: ")
    if recipe_name:
        oils_list = {}
        while True:
            oil = input("Input oil (ENTER for cancel): ")
            if not oil:
                break
            drops = input("number of drops: ")
            if drops.isdigit():
                drops = int(drops)
            else:
                print("You must input NUMBER.")
                break
            oils_list[oil] = Oil(oil, drops)
        BASE[recipe_name] = Recipe(recipe_name, oils_list, 0)
        print("\nRecipe saved in BASE.\n")
    else:
        print("\nYou skip recipe creation.\n")


def delete_recipe():
    """Delete recipe from BASE."""
    recipe_number = input("Input nubmber of recipe to delete: ")
    if check_is_it_number_in_range(recipe_number, len(BASE)):
        recipe_number = int(recipe_number)
        keys = sorted(BASE)
        BASE.pop(keys[recipe_number - 1], None)
        print("\nRecipe '{}' deleted.\n".format(keys[recipe_number - 1]))


def show_available_recipe():
    """Otput recipes avaliable to make only."""
    collection = sorted(COLLECTION)
    not_enough_oils = True
    for recipe in BASE:
        avaliable_recipe = True
        for oil in list(BASE[recipe].oils):
            if oil not in collection:
                avaliable_recipe = False
        if avaliable_recipe:
            not_enough_oils = False
            print(BASE[recipe])
    if not_enough_oils:
        print("\nSeems like you havn't enough oils for any recipe :'(\n")


def give_rating_to_recipe():
    """Give rating to recipe."""
    recipe_number = input("Input nubmber of recipe: ")
    rating = input("Input rating (in range 0-10): ")
    if (check_is_it_number_in_range(recipe_number, len(BASE)) and
            check_is_it_number_in_range(rating, 10)):
        recipe_number = int(recipe_number)
        rating = int(rating)
        sorted_base = sorted(BASE)
        recipe = BASE[sorted_base[recipe_number - 1]]
        recipe.rating = rating
        BASE[sorted_base[recipe_number - 1]] = recipe


def delete_ingredient_from_collect():
    """Delete ingredient from collection."""
    oil_number = input("Input number of deleted oil: ")
    if check_is_it_number_in_range(oil_number, len(COLLECTION)):
        oil_number = int(oil_number)
        collection_sort = sorted(COLLECTION)
        COLLECTION.pop(collection_sort[oil_number - 1])
        COLLECTION.sync()
        print("\nOil '{}' deleted.".format({collection_sort[oil_number - 1]}))
    show_oils_collection()


def add_ingredient_to_collection():
    """Add ingredient to collection."""
    ingredient = input("Input oil name: ")
    if ingredient:
        COLLECTION[ingredient] = Oil(ingredient, 0)
        COLLECTION.sync()
    else:
        print("\nYou skip oil adding.\n")
    print("\nOil saved in collection.\n")
    show_oils_collection()


def show_missing_ingredients():
    """Otput list of all ingredients from recipes and show missing."""
    popularity_blocks, list_of_all_oils = create_dict_oils_popularity()
    longest_oil_name = find_max_length(list_of_all_oils)
    # Make sorted list by oil popularity.
    priority = sorted(popularity_blocks)[::-1]
    # Check aveliability of ingredients from collection.
    for position in priority:
        for ingredient in popularity_blocks[position]:
            spaces = (longest_oil_name - len(ingredient)+1) * ' '
            print("{}{}(in {} recipes)".format(
                ingredient, spaces, position), end=' ')
            collection = sorted(COLLECTION)
            if ingredient in collection:
                print(" - in collection.")
            else:
                print()


def create_dict_oils_popularity():
    """
    Create dictionary where keys are number in recipes, values are ingredients.
    """
    list_of_all_recipes_oils = []
    for recipe in BASE:
        list_of_all_recipes_oils += list(BASE[recipe].oils.keys())
    # Count number of ingredients.
    oils_popularity = {oil: list_of_all_recipes_oils.count(oil)
                       for oil in list_of_all_recipes_oils}
    # Creates blocks of popularity.
    popularity_blocks = {}
    for popularity, oils in oils_popularity.items():
        popularity_blocks[oils] = popularity_blocks.get(oils, [])
        popularity_blocks[oils].append(popularity)
    return popularity_blocks, list_of_all_recipes_oils


def show_recipe_with_choosen_oil():
    """Search recipe with the ingredient."""
    oil_number = input("Input ingredient number: ")
    collection = sorted(COLLECTION)
    if check_is_it_number_in_range(oil_number, len(collection)):
        oil_number = int(oil_number)
        print(f"\nRecipes contane '{collection[oil_number-1]}':\n")
        list_of_recipes_names = []
        for recipe in BASE:
            if collection[oil_number-1] in BASE[recipe].oils:
                list_of_recipes_names.append(BASE[recipe].name)
        sort_list = sorted(list_of_recipes_names)
        for recipe in sort_list:
            print(BASE[recipe])
        if list_of_recipes_names == []:
            print('There is no ricept with this oil.')


def check_is_it_number_in_range(number, list_range):
    """Check is input a number in current range."""
    check_number = False
    if number.isdigit():
        if int(number) in range(list_range + 1):
            check_number = True
        else:
            print("\nYou must input number IN CURRENT RANGE.\n")
    else:
        print("\nYou must input NUMBER.\n")
    return check_number


def find_max_length(array):
    """Search element with maximum lenght."""
    max_length = 0
    for i in array:
        if len(i) > max_length:
            max_length = len(i)
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
            break
        elif choise in ['e', 'E', 'а', 'А']:
            import localisations.EN as language
            break
        else:
            print("There is no such option, input letter correctl.\n")
    return language


def show_oils_collection():
    """Otput numbered and sorted igredient collection."""
    collection = sorted(COLLECTION)
    print("My collection:")
    for count, oil in enumerate(collection, 1):
        print(f"[{count}] {oil}")


def make_absolyte_path(relative_path):
    """Make absolyte path of dataBASE file."""
    script_name = sys.argv[0]
    script_path = os.path.dirname(script_name)
    absolute_path = os.path.abspath(script_path)
    os_path = os.path.join(absolute_path, *relative_path)
    return os_path


# =============================================================================
RECIPE_PATH = make_absolyte_path(['data', 'resipe_class'])
COLLECTION_PATH = make_absolyte_path(['data', 'collection_class'])

if __name__ == '__main__':
    PROGRAM_LANGUAGE = choose_language()
    SEASON_SUGGESTION = suggest.give_season_suggestion()
    print(SEASON_SUGGESTION)
    print(PROGRAM_LANGUAGE.main_meny)

    # Navigation for Main meny.
    while True:
        BASE = shelve.open(RECIPE_PATH)
        COLLECTION = shelve.open(COLLECTION_PATH)

        USER_CHOISE = input()
        if USER_CHOISE in ['s', 'S', 'п', 'П']:
            show_all_recipes()
        elif USER_CHOISE in ['i', 'I', 'в', 'В']:
            show_available_recipe()
        elif USER_CHOISE in ['c', 'C', 'с', 'С']:
            create_recipe()
        elif USER_CHOISE in ['a', 'A', 'а', 'А']:
            print(SEASON_SUGGESTION)
        elif USER_CHOISE in ['r', 'R', 'у', 'У']:
            delete_recipe()
        elif USER_CHOISE in ['g', 'G', 'р', 'Р']:
            give_rating_to_recipe()
        elif USER_CHOISE in ['e', 'E', 'з', 'З']:
            sys.exit()
        elif USER_CHOISE in ['o', 'O', 'к', 'К']:
            print('\n', PROGRAM_LANGUAGE.collection_meny)
            show_oils_collection()
            # Navigation for Collection meny.
            while True:
                USER_CHOISE = input()
                if USER_CHOISE in ['m', 'M', 'м', 'М']:
                    # Return in main meny.
                    print(PROGRAM_LANGUAGE.main_meny)
                    break
                elif USER_CHOISE in ['o', 'O', 'к', 'К']:
                    show_oils_collection()
                elif USER_CHOISE in ['s', 'S', 'о', 'О']:
                    show_missing_ingredients()
                elif USER_CHOISE in ['a', 'A', 'д', 'Д']:
                    add_ingredient_to_collection()
                elif USER_CHOISE in ['r', 'R', 'у', 'У']:
                    delete_ingredient_from_collect()
                elif USER_CHOISE in ['f', 'F', 'н', 'Н']:
                    show_recipe_with_choosen_oil()
                elif USER_CHOISE in ['e', 'E', 'з', 'З']:
                    sys.exit()
                else:
                    print("There is no such option, input letter correctly\n")
                print(PROGRAM_LANGUAGE.mini_collection)
        else:
            print("There is no such option, input letter correctly\n")
        print('\n', PROGRAM_LANGUAGE.mini_main)

        BASE.close()
        COLLECTION.close()