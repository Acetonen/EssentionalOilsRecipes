#!/usr/bin/env python3
"""Program for store recipes for aroma lamps"""

import sys

import modules.recipe_module
import modules.collection_module
from modules.recipe_class import Recipe
from modules.oil_class import Oil
from localisations import suggestions_ru


def choose_language():
    """Choose program language."""
    print("""
    Choose the choise / Выберете язык
    [E]/[А] - English
    [R]/[Р] - Russian
    """)
    while True:
        choise = input("").lower()
        if choise in ['r', 'р']:
            import localisations.rus as language
            break
        elif choise in ['e', 'а']:
            import localisations.en as language
            break
        else:
            print("There is no such option, input letter correctl.\n")
    return language


if __name__ == '__main__':

    AVAILABLE_CLASSES = (Oil, Recipe)
    PROGRAM_LANGUAGE = choose_language()
    SEASON_SUGGESTION = suggestions_ru.give_season_suggestion()
    print(SEASON_SUGGESTION)
    print(PROGRAM_LANGUAGE.MAIN_MENY)

    # Navigation for Main meny.
    while True:
        USER_CHOISE = input().lower()
        if USER_CHOISE in ['s', 'п']:
            modules.recipe_module.show_all_recipes()
        elif USER_CHOISE in ['i', 'в']:
            modules.recipe_module.show_available_recipe()
        elif USER_CHOISE in ['c', 'с']:
            modules.recipe_module.create_recipe()
        elif USER_CHOISE in ['r', 'у']:
            modules.recipe_module.delete_recipe()
        elif USER_CHOISE in ['g', 'р']:
            modules.recipe_module.give_rating_to_recipe()
        elif USER_CHOISE in ['a', 'а']:
            print(SEASON_SUGGESTION)
        elif USER_CHOISE in ['e', 'з']:
            sys.exit()
        elif USER_CHOISE in ['o', 'к']:
            print('\n', PROGRAM_LANGUAGE.COLLECTION_MENY)
            modules.collection_module.show_oils_collection()
            # Navigation for Collection meny.
            while True:
                USER_CHOISE = input().lower()
                if USER_CHOISE in ['m', 'м']:
                    # Return in main meny.
                    print(PROGRAM_LANGUAGE.MAIN_MENY)
                    break
                elif USER_CHOISE in ['o', 'к']:
                    modules.collection_module.show_oils_collection()
                elif USER_CHOISE in ['s', 'о']:
                    modules.collection_module.show_missing_ingredients()
                elif USER_CHOISE in ['a', 'д']:
                    modules.collection_module.add_ingredient_to_collection()
                elif USER_CHOISE in ['r', 'у']:
                    modules.collection_module.delete_ingredient_from_collect()
                elif USER_CHOISE in ['f', 'н']:
                    modules.collection_module.show_recipe_with_choosen_oil()
                elif USER_CHOISE in ['e', 'з']:
                    sys.exit()
                else:
                    print("There is no such option, input letter correctly\n")
                print(PROGRAM_LANGUAGE.MINI_COLLECTION)
        else:
            print("There is no such option, input letter correctly\n")
        print('\n', PROGRAM_LANGUAGE.MINI_MAIN)
