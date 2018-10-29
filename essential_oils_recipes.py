#!/usr/bin/env python3
"""Program for store recipes for aroma lamps"""

import sys

import recipe_module
import collection_module
from localisations import suggestions_ru
from recipe_class import Recipe
from oil_class import Oil


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
            import localisations.rus as language
            break
        elif choise in ['e', 'E', 'а', 'А']:
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
        USER_CHOISE = input()
        if USER_CHOISE in ['s', 'S', 'п', 'П']:
            recipe_module.show_all_recipes()
        elif USER_CHOISE in ['i', 'I', 'в', 'В']:
            recipe_module.show_available_recipe()
        elif USER_CHOISE in ['c', 'C', 'с', 'С']:
            recipe_module.create_recipe()
        elif USER_CHOISE in ['r', 'R', 'у', 'У']:
            recipe_module.delete_recipe()
        elif USER_CHOISE in ['g', 'G', 'р', 'Р']:
            recipe_module.give_rating_to_recipe()
        elif USER_CHOISE in ['a', 'A', 'а', 'А']:
            print(SEASON_SUGGESTION)
        elif USER_CHOISE in ['e', 'E', 'з', 'З']:
            sys.exit()
        elif USER_CHOISE in ['o', 'O', 'к', 'К']:
            print('\n', PROGRAM_LANGUAGE.COLLECTION_MENY)
            collection_module.show_oils_collection()
            # Navigation for Collection meny.
            while True:
                USER_CHOISE = input()
                if USER_CHOISE in ['m', 'M', 'м', 'М']:
                    # Return in main meny.
                    print(PROGRAM_LANGUAGE.MAIN_MENY)
                    break
                elif USER_CHOISE in ['o', 'O', 'к', 'К']:
                    collection_module.show_oils_collection()
                elif USER_CHOISE in ['s', 'S', 'о', 'О']:
                    collection_module.show_missing_ingredients()
                elif USER_CHOISE in ['a', 'A', 'д', 'Д']:
                    collection_module.add_ingredient_to_collection()
                elif USER_CHOISE in ['r', 'R', 'у', 'У']:
                    collection_module.delete_ingredient_from_collect()
                elif USER_CHOISE in ['f', 'F', 'н', 'Н']:
                    collection_module.show_recipe_with_choosen_oil()
                elif USER_CHOISE in ['e', 'E', 'з', 'З']:
                    sys.exit()
                else:
                    print("There is no such option, input letter correctly\n")
                print(PROGRAM_LANGUAGE.MINI_COLLECTION)
        else:
            print("There is no such option, input letter correctly\n")
        print('\n', PROGRAM_LANGUAGE.MINI_MAIN)
