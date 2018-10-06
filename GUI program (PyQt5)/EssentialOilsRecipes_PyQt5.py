import sys
import json
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
#PEP8


class MainWindow(QWidget):
    """
    Main window of program.
    It contain main meny
    """

    def __init__(self):
        super().__init__()
        self.main_meny_UI()

    def main_meny_UI(self):

        # Button that shown collection of ingredients.
        collection_button = QPushButton('Коллекция', self)
        collection_button.clicked.connect(collection)
        collection_button.resize(150, 25)
        collection_button.move(50, 10)

        # Button that shown all recipes.
        recipes_button = QPushButton('Все рецепты', self)
        recipes_button.clicked.connect(recipes)
        recipes_button.resize(150, 25)
        recipes_button.move(50, 40)

        # Button to create recipe.
        create_button = QPushButton('(Н) Создать рецепт', self)
        create_button.clicked.connect(creation_recipe)
        create_button.resize(150, 25)
        create_button.move(50, 70)

        # Button to delete recipe.
        delete_button = QPushButton('(Н) Удалить рецепт', self)
        delete_button.clicked.connect(delete_recipe)
        delete_button.resize(150, 25)
        delete_button.move(50, 100)

        # Button to show aveliable recipes.
        aveliable_recipe_button = QPushButton('Доступные рецепты', self)
        aveliable_recipe_button.clicked.connect(aveliable_recipe)
        aveliable_recipe_button.resize(150, 25)
        aveliable_recipe_button.move(50, 130)

        # Give rate to recipe.
        rate_recipe_button = QPushButton('(Н) Оценить рецепт', self)
        rate_recipe_button.clicked.connect(recipe_rate)
        rate_recipe_button.resize(150, 25)
        rate_recipe_button.move(50, 160)

        # Ingredients from recipes.
        ing_from_rec_button = QPushButton('Ингредиенты из рецептов', self)
        ing_from_rec_button.clicked.connect(ing_from_rec)
        ing_from_rec_button.resize(200, 25)
        ing_from_rec_button.move(50, 190)

        # Recipe with ingridient.
        rec_with_ing_button = QPushButton('(Н) Рецепты с ингридиентом', self)
        rec_with_ing_button.clicked.connect(rec_with_ing)
        rec_with_ing_button.resize(200, 25)
        rec_with_ing_button.move(50, 220)

        # Exit aplication.
        qbtn = QPushButton('Выход', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(50, 25)
        qbtn.move(50, 270)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Рецепты для аромолампы')
        self.show()


# Functions of the buttons.
#==============================================================================
def collection():
    """Otput numbered and sorted igredient collection."""

    print(LG.collection_meny)
    coll = sorted(data('data/collection.txt'))
    print("Моя коллекция:")
    for count, oil in enumerate(coll,1):
        print(f"[{count}] {oil}")
    print()

def recipes():
    """ Print sorted recipes collection"""

    try: rate_dict = data('data/rate.txt')
    except: rate_dict = {}
    base = data('data/base.txt')
    keys = sorted(base)
    for count, oil in enumerate(keys,1):
        # Ensert some spaces after recite nubber.
        if count<10: spase = " "
        else: spase = ''
        print(f"[{count}] {spase}", end=' ')
        print(f"{rate_dict.get(oil, '0')}/10", end=' ')
        beauty_print(oil)
    print('\n', LG.mini_main)

def creation_recipe():
    """Creation of new recipe."""

    base = data('data/base.txt')
    name = input("Название рецепта: ")
    ingredient_list = {}
    while True:
        ingredient = input("Введите ингредиет (ENTER для отмены): ")
        if ingredient == '': break
        drop = input("количество капель: ")
        ingredient_list[ingredient] = drop
    base[name] = ingredient_list
    save_data("data/base.txt", base)
    print(f"\nРецепт записан в базу.\n")
    print(LG.mini_main)

def delete_recipe():
    """Delete recipe from th base."""

    keys = sorted(data('data/base.txt'))
    choise = int(input("Введите номер рецепта, который необходимо удалить: "))
    delete("data/base.txt", keys[choise - 1])
    delete("data/rate.txt", keys[choise - 1])
    print(f"\nРецепт '{keys[choise - 1]}' удален.\n")
    print(LG.mini_main)

def aveliable_recipe():
    """Otput recipes avaliable to make only."""

    coll = data('data/collection.txt')
    base = data('data/base.txt')
    # Search ingredient from base in list.
    main_flag = True
    for name in base:
        flag = True
        for ing in list(base[name].keys()):
            if ing not in coll: flag = False
        if flag:
            main_flag = False
            beauty_print(name)
    if main_flag:
        print("\nПохоже, что у Вас ни на что не хватает ингредиентов :'(\n")
    print('\n', LG.mini_main)

def recipe_rate():
    """Give rate to recipe."""

    try: rate_dict = data('data/rate.txt')
    except: rate_dict = {}
    keys = sorted(data('data/base.txt'))
    choise = int(input("Ведите номер рецепта: "))
    rate = input("Введите оценку (из 10-ти): ")
    rate_dict[keys[choise - 1]] = rate
    save_data('data/rate.txt', rate_dict)
    print(LG.mini_main)

def delete_ingredient():
    """Delete ingredient from collection."""

    coll = sorted(data('data/collection.txt'))
    n = int(input("Введите номер удаляемого ингридиента: "))
    delete = coll[n - 1]
    delete("data/collection.txt", delete)
    collection()
    print(f"\nИнгридиент '{delete}' удален.")
    print(LG.mini_collection)

def add_ingredient():
    """Add ingredient to collection."""

    list_of_recipes = data('data/collection.txt')
    list_of_recipes.append(input("Введите название ингредиента: "))
    save_data('data/collection.txt', list_of_recipes)
    print()
    collection()
    print(LG.mini_collection)

def ing_from_rec():
    """Otput list of all ingredients from recipes."""

    base = data('data/base.txt')
    list_of_ingredients = []
    # List from all igredients from recipes.
    for i in base:
        list_of_ingredients += list(base[i].keys())
    # Count number of ingredientsself.
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
(в {position} рецептах)\
""", end=' ')
            if ingredient not in data('data/collection.txt'):
                print(" - отсутствует в коллекции.")
            else: print()
    print(LG.mini_collection)

def rec_with_ing():
    """Search recipe with the ingredient."""

    base = data('data/base.txt')
    coll = sorted(data('data/collection.txt'))
    n = int(input("Введите номер ингредиента: "))
    search = coll[n - 1]
    print(f"\nРецепты, содержащие '{search}':\n")
    # Create list of keys from our base with the ingredient.
    list_of_recipes_names = [keyg for (keyg, value) in
                            base.items() if search in value]
    sortList = sorted(list_of_recipes_names)
    for name in sortList:
        beauty_print(name)
    print(LG.mini_collection)


# Support functions.
#==============================================================================
def data(file_name):
    """Load base from file."""

    with open(file_name, 'r', encoding='utf8') as file:
        data = json.load(file)
    return data

def save_data(file_name, data):
    """Dump base in file."""

    with open(file_name, 'w', encoding='utf8') as file:
        json.dump(data, file)

def delete(file_name, delete):
    """Delete ingredient or recipe from base."""

    with open(file_name, "r+") as file:
        base = json.load(file)
        # Different ways to list and dictionary.
        try: base.pop(delete, None)
        except: base.remove(delete)
        file.seek(0)
        file.truncate()
        json.dump(base, file)

def beauty_print(name):
    """Structural output of recipes."""

    base = data('data/base.txt')
    print(f"{name}{(max_length(base) - len(name) + 1)*' '}", end=': ')
    for key in base[name]:
        print(f"{key} - {base[name][key]}к;", end=' ')
    print()

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
    [E] - English
    [R] - Russian
    """)
    choise = input("")
    if choise == 'r' or choise == 'R':
        import localisations.RUS as language
        try: import localisations.suggestions_RU
        except: print("Здравствуте!")
    elif choise == 'e' or choise == 'E':
        import localisations.EN as language
    return language


# Program skeleton
if __name__ == '__main__':
    app = QApplication(sys.argv)
    LG = lang() # localisation language
    meny = MainWindow()
    print(LG.main_meny) # output main meny of program
    sys.exit(app.exec_())
