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


def input_to_main_meny(choise):
    """
    This is the main meny of it program.
    You can go to "Collections" sub-meny, or working here.
    """
    if choise in ['s', 'S', 'п', 'П']:
        # Output all recipes.
        show_all_recipes()
    elif choise in ['i', 'I', 'в', 'В']:
        # Otput recipes avaliable to make only.
        show_available_recipe()
    elif choise in ['c', 'C', 'с', 'С']:
        # Creation of new recipe.
        create_recipe()
    elif choise in ['a', 'A', 'а', 'А']:
        # Show season suggestions.
        print(SUGGESTION)
    elif choise in ['r', 'R', 'у', 'У']:
        # Delete recipe.
        delete_recipe()
    elif choise in ['g', 'G', 'р', 'Р']:
        # Give rate to recipe.
        give_rating()
    elif choise in ['e', 'E', 'з', 'З']:
        # Exit program.
        sys.exit()
    elif choise in ['o', 'O', 'к', 'К']:
        # Open collection meny.
        print('\n', LG.collection_meny)
        show_oils_collection()
        while True:
            choise = input()
            input_to_collection_meny(choise)
            if choise in ['m', 'M', 'м', 'М']:
                # Return in main meny.
                print(LG.main_meny)
                break
    else:
        print("There is no such option, input letter correctly\n")
    print('\n', LG.mini_main)


def input_to_collection_meny(choise):
    """
    This is the Collection meny of program.
    Here you can working with your collection.
    """
    if choise in ['o', 'O', 'к', 'К']:
        # Print mini collection meny.
        show_oils_collection()
    elif choise in ['s', 'S', 'о', 'О']:
        # Otput list of all ingredients from recipes.
        show_missing_ingredients()
    elif choise in ['a', 'A', 'д', 'Д']:
        # Add ingredient to collection.
        add_ingredient()
    elif choise in ['r', 'R', 'у', 'У']:
        # Delete ingredient from collection.
        delete_ingredient()
    elif choise in ['f', 'F', 'н', 'Н']:
        # Search recipe with the ingredient.
        show_recipe_with_choosen_oil()
    elif choise in ['e', 'E', 'з', 'З']:
        # Exit program.
        sys.exit()
    else:
        print("There is no such option, input letter correctly\n")
    print(LG.mini_collection)


def show_all_recipes():
    """ Print sorted recipes collection"""
    base = shelve.open(RECIPE_PATH)
    sorted_base = sorted(base)
    for count, recipe in enumerate(sorted_base, 1):
        print("[{}] {}".format(count, base[recipe]))
    base.close()


def create_recipe():
    """Create new recipe."""
    recipe_name = input("Recipe name: ")
    if recipe_name:
        base = shelve.open(RECIPE_PATH)
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
        base[recipe_name] = Recipe(recipe_name, oils_list, 0)
        print("\nRecipe saved in base.\n")
        base.close()
    else:
        print("\nYou skip recipe creation.\n")


def delete_recipe():
    """Delete recipe from base."""
    recipe_number = input("Input nubmber of recipe to delete: ")
    base = shelve.open(RECIPE_PATH)
    if check_is_it_number_in_range(recipe_number, len(base)):
        recipe_number = int(recipe_number)
        keys = sorted(base)
        base.pop(keys[recipe_number - 1], None)
        print("\nRecipe '{}' deleted.\n".format(keys[recipe_number - 1]))
    base.close()


def show_available_recipe():
    """Otput recipes avaliable to make only."""
    collection = sorting_from_file(COLLECTION_PATH)
    base = shelve.open(RECIPE_PATH)
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


def give_rating():
    """Give rating to recipe."""
    recipe_number = input("Input nubmber of recipe: ")
    rating = input("Input rating (in range 0-10): ")
    base = shelve.open(RECIPE_PATH)
    if (check_is_it_number_in_range(recipe_number, len(base)) and
            check_is_it_number_in_range(rating, 10)):
        recipe_number = int(recipe_number)
        rating = int(rating)
        sorted_base = sorted(base)
        recipe = base[sorted_base[recipe_number - 1]]
        recipe.rating = rating
        base[sorted_base[recipe_number - 1]] = recipe
    base.close()


def delete_ingredient():
    """Delete ingredient from collection."""
    oil_number = input("Input number of deleted oil: ")
    collection = shelve.open(COLLECTION_PATH)
    if check_is_it_number_in_range(oil_number, len(collection)):
        oil_number = int(oil_number)
        collection_sort = sorted(collection)
        collection.pop(collection_sort[oil_number - 1])
        print("\nOil '{}' deleted.".format({collection_sort[oil_number - 1]}))
    collection.close()
    show_oils_collection()


def add_ingredient():
    """Add ingredient to collection."""
    ingredient = input("Input oil name: ")
    if ingredient:
        collection = shelve.open(COLLECTION_PATH)
        collection[ingredient] = Oil(ingredient, 0)
        collection.close()
    else:
        print("\nYou skip oil adding.\n")
    print("\nOil saved in collection.\n")
    show_oils_collection()


def show_missing_ingredients():
    """Otput list of all ingredients from recipes and show missing."""
    popular_blocks, list_of_all_oils = create_dict_oils_popularity()
    longest_oil_name = find_max_length(list_of_all_oils)
    # Make sorted list by oil popularity.
    priority = sorted(popular_blocks)[::-1]
    # Check aveliability of ingredients from collection.
    for position in priority:
        for ingredient in popular_blocks[position]:
            spaces = (longest_oil_name - len(ingredient)+1) * ' '
            print("{}{}(in {} recipes)".format(
                ingredient, spaces, position), end=' ')
            collection = sorting_from_file(COLLECTION_PATH)
            if ingredient in collection:
                print(" - in collection.")
            else:
                print()


def create_dict_oils_popularity():
    """
    Create dictionary where keys are number in recipes, values are
    ingredients.
    """
    base = shelve.open(RECIPE_PATH)
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


def show_recipe_with_choosen_oil():
    """Search recipe with the ingredient."""
    oil_number = input("Input ingredient number: ")
    collection = sorting_from_file(COLLECTION_PATH)
    if check_is_it_number_in_range(oil_number, len(collection)):
        oil_number = int(oil_number)
        base = shelve.open(RECIPE_PATH)
        print(f"\nRecipes contane '{collection[oil_number-1]}':\n")
        list_of_recipes_names = []
        for recipe in base:
            if collection[oil_number-1] in base[recipe].oils:
                list_of_recipes_names.append(base[recipe].name)
        sort_list = sorted(list_of_recipes_names)
        for recipe in sort_list:
            print(base[recipe])
        base.close()
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
    collection = sorting_from_file(COLLECTION_PATH)
    print("My collection:")
    for count, oil in enumerate(collection, 1):
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


# Program skeleton
# =============================================================================
RECIPE_PATH = make_absolyte_path(['data', 'resipe_class'])
COLLECTION_PATH = make_absolyte_path(['data', 'collection_class'])

if __name__ == '__main__':
    LG = choose_language()   # Localisation language
    SUGGESTION = suggest.give_season_suggestion()
    print(SUGGESTION)
    sys.stdout.write(LG.main_meny)  # Output main meny of program
    while True:
        USER_CHOISE = input()
        input_to_main_meny(USER_CHOISE)
