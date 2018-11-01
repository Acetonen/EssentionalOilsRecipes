#!/usr/bin/env python3
"""Functions to work with recipes"""

import shelve

from modules.recipe_class import Recipe
from modules.oil_class import Oil
from modules.absolyte_path_module import COLLECTION_PATH, RECIPE_PATH


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
        with shelve.open(RECIPE_PATH) as base:
            base[recipe_name] = Recipe(recipe_name, oils_list, 0)
        print("\nRecipe saved in base.\n")
    else:
        print("\nYou skip recipe creation.\n")


def delete_recipe():
    """Delete recipe from base."""
<<<<<<< HEAD
    recipe_number = input("Input number of recipe to delete: ")
    base_size = give_size_of_recipe_base()
    if check_is_it_number_in_range(recipe_number, base_size):
        recipe = give_recipe_by_position_in_base(recipe_number)
        with shelve.open(RECIPE_PATH) as base:
            base.pop(recipe, None)
        print("\nRecipe '{}' deleted.\n".format(recipe))


def give_recipe_by_position_in_base(position):
    """Sorte recipe collection and give recipe name by position number"""
    with shelve.open(RECIPE_PATH) as base:
        recipe_number = int(position)
        base_sort = sorted(base)
        recipe = base_sort[recipe_number - 1]
    return recipe


def give_size_of_recipe_base():
    """Return size of current recipe base"""
    with shelve.open(RECIPE_PATH) as base:
        base_size = len(base)
    return base_size
=======
    recipe_number = input("Input nubmber of recipe to delete: ")
    base = shelve.open(RECIPE_PATH)
    if check_is_it_number_in_range(recipe_number, len(base)):
        recipe_number = int(recipe_number)
        sorted_base = sorted(base)
        recipe = sorted_base[recipe_number - 1]
        base.pop(recipe, None)
        print("\nRecipe '{}' deleted.\n".format(recipe))
    base.close()
>>>>>>> 13830e729c51abcbf014966160abaf1bf34d8b83


def show_available_recipe():
    """Otput recipes avaliable to make only."""
    with shelve.open(COLLECTION_PATH) as collection:
        sorted_collection = sorted(collection)
    not_enough_oils = True
    base = shelve.open(RECIPE_PATH)
    for recipe in base:
        for oil in base[recipe].get_oils():
            if oil not in sorted_collection:
                break
        else:
            not_enough_oils = False
            print(base[recipe])
    base.close()
    if not_enough_oils:
        print("\nSeems like you havn't enough oils for any recipe :'(\n")


def give_rating_to_recipe():
    """Give rating to recipe."""
    recipe_number = input("Input nubmber of recipe: ")
    rating = input("Input rating (in range 0-10): ")
    base_size = give_size_of_recipe_base()
    if (check_is_it_number_in_range(recipe_number, base_size) and
            check_is_it_number_in_range(rating, 10)):
        rating = int(rating)
<<<<<<< HEAD
        recipe = give_recipe_by_position_in_base(recipe_number)
        with shelve.open(RECIPE_PATH) as base:
            temp_recipe = base[recipe]
            temp_recipe.set_rating(rating)
            base[recipe] = temp_recipe
=======
        sorted_base = sorted(base)
        choosen_recipe = sorted_base[recipe_number - 1]
        temp_recipe = base[choosen_recipe]
        temp_recipe.set_rating(rating)
        base[choosen_recipe] = temp_recipe
    base.close()
>>>>>>> 13830e729c51abcbf014966160abaf1bf34d8b83


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
