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
    collection_size = give_size_of_oil_collection()
    if check_is_it_number_in_range(oil_number, collection_size):
        oil = give_oil_by_position_in_collect(oil_number)
        with shelve.open(COLLECTION_PATH) as collection:
            collection.pop(oil)
        print("\nOil {} deleted.".format(oil))
    show_oils_collection()


def give_oil_by_position_in_collect(position):
    """Sorted oil collection and gige oil name by position number"""
    with shelve.open(COLLECTION_PATH) as collection:
        oil_number = int(position)
        collection_sort = sorted(collection)
        oil = collection_sort[oil_number - 1]
    return oil


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


def give_size_of_oil_collection():
    """Return size of current oils collection"""
    with shelve.open(COLLECTION_PATH) as collection:
        collection_size = len(collection)
    return collection_size


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
        for oil in popularity_blocks[position]:
            spaces = (longest_oil_name - len(oil)+1) * ' '
            print("{}{}(in {} recipes) {}".format(
                oil, spaces, position, check_oil_avaliability(oil)))


def create_dict_oils_popularity():
    """
    Create dictionary where keys are number in recipes, values are ingredients.
    """
    list_of_all_recipes_oils = []
    with shelve.open(RECIPE_PATH) as base:
        for recipe in base:
            list_of_all_recipes_oils += base[recipe].get_oils()
    # Count frequency of oils occurrence in recipes.
    oils_popularity = {oil: list_of_all_recipes_oils.count(oil)
                       for oil in list_of_all_recipes_oils}
    # Creates blocks of popularity.
    popularity_blocks = {}
    for popularity, oils in oils_popularity.items():
        popularity_blocks[oils] = popularity_blocks.get(oils, [])
        popularity_blocks[oils].append(popularity)
    return popularity_blocks, list_of_all_recipes_oils


def check_oil_avaliability(oil):
    """Check if curent oil in collection"""
    with shelve.open(COLLECTION_PATH) as collection:
        aveliability = ''
        if oil in collection:
            aveliability = " - in collection."
    return aveliability


def show_recipe_with_choosen_oil():
    """Search recipe with the ingredient."""
    oil_number = input("Input ingredient number: ")
    collection_size = give_size_of_oil_collection()
    if check_is_it_number_in_range(oil_number, collection_size):
        oil = give_oil_by_position_in_collect(oil_number)
        print(f"\nRecipes contane '{oil}':\n")
        list_of_recipes_names = []
        base = shelve.open(RECIPE_PATH)
        for recipe in base:
            if oil in base[recipe].get_oils():
                list_of_recipes_names.append(recipe)
        sort_list = sorted(list_of_recipes_names)
        for recipe in sort_list:
            print(base[recipe])
        base.close()
        if list_of_recipes_names == []:
            print('There is no ricept with this oil.')


def find_max_length(array):
    """Search element with maximum lenght."""
    max_length = 0
    for element in array:
        if len(element) > max_length:
            max_length = len(element)
    return max_length
