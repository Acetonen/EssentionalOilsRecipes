#!/usr/bin/env python3
"""Functions to work with collection"""

import shelve

from modules.oil_class import Oil
from modules.absolyte_path_module import COLLECTION_PATH, RECIPE_PATH


def show_oils_collection():
    """Otput numbered and sorted igredient collection."""
    with shelve.open(COLLECTION_PATH) as collection:
        sorted_collection = sorted(collection)
    print("My collection:")
    for count, oil in enumerate(sorted_collection, 1):
        print(f"[{count}] {oil}")


def delete_ingredient_from_collect():
    """Delete ingredient from collection."""
    oil_number = input("Input number of deleted oil: ")
    collection = shelve.open(COLLECTION_PATH)
    if check_is_it_number_in_range(oil_number, len(collection)):
        oil_number = int(oil_number)
        collection_sort = sorted(collection)
        collection.pop(collection_sort[oil_number - 1])
        print("\nOil {} deleted.".format(collection_sort[oil_number - 1]))
    collection.close()
    show_oils_collection()


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


def add_ingredient_to_collection():
    """Add ingredient to collection."""
    ingredient = input("Input oil name: ")
    if ingredient:
        with shelve.open(COLLECTION_PATH) as collection:
            collection[ingredient] = Oil(ingredient, 0)
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
            with shelve.open(COLLECTION_PATH) as collection:
                sorted_collection = sorted(collection)
            if ingredient in sorted_collection:
                print(" - in collection.")
            else:
                print()


def create_dict_oils_popularity():
    """
    Create dictionary where keys are number in recipes, values are ingredients.
    """
    list_of_all_recipes_oils = []
    base = shelve.open(RECIPE_PATH)
    for recipe in base:
        list_of_all_recipes_oils += list(base[recipe].oils.keys())
    # Count number of ingredients.
    base.close()
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
    with shelve.open(COLLECTION_PATH) as collection:
        sorted_collection = sorted(collection)
    if check_is_it_number_in_range(oil_number, len(sorted_collection)):
        oil_number = int(oil_number)
        print(f"\nRecipes contane '{sorted_collection[oil_number-1]}':\n")
        list_of_recipes_names = []
        base = shelve.open(RECIPE_PATH)
        for recipe in base:
            if sorted_collection[oil_number-1] in base[recipe].oils:
                list_of_recipes_names.append(base[recipe].name)
        sort_list = sorted(list_of_recipes_names)
        for recipe in sort_list:
            print(base[recipe])
        base.close()
        if list_of_recipes_names == []:
            print('There is no ricept with this oil.')


def find_max_length(array):
    """Search element with maximum lenght."""
    max_length = 0
    for i in array:
        if len(i) > max_length:
            max_length = len(i)
    return max_length
