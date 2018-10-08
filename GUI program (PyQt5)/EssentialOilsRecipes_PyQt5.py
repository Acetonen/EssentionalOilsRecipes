import sys
import json
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, qApp,
                             QMessageBox, QDesktopWidget, QMainWindow,
                             QAction)
#PEP8


class MainWindow(QMainWindow):
    """
    Main window of program.
    It contain main meny
    """

    def __init__(self):
        super().__init__()
        self.main_meny_UI()

    def main_meny_UI(self):

        exit_act = QAction('&Выход', self) # create action
        exit_act.setShortcut('Ctrl+Q') # shortcut
        exit_act.setStatusTip('Выйти из приложения') # Tip on status bar
        exit_act.triggered.connect(qApp.quit) # connect to quit

        collection_act = QAction('&Коллекция', self)
        collection_act.setShortcut('Ctrl+K')
        collection_act.setStatusTip('Показать мою коллекцию')
        collection_act.triggered.connect(self.collection)

        all_recipe_act = QAction('&Рецепты', self)
        all_recipe_act.setShortcut('Ctrl+E')
        all_recipe_act.setStatusTip('Показать все имеющиеся рецепты')
        all_recipe_act.triggered.connect(recipes)

        create_recipe_act = QAction('&Новый рецепт', self)
        create_recipe_act.setShortcut('Ctrl+N')
        create_recipe_act.setStatusTip('Создать новый рецепт')
        create_recipe_act.triggered.connect(creation_recipe)

        avail_recipe_act = QAction('&Доступные рецепты', self)
        avail_recipe_act.setShortcut('Ctrl+A')
        avail_recipe_act.setStatusTip('Показать рецепты на которые хватает \
ингрдиетнов')
        avail_recipe_act.triggered.connect(available_recipe)

        ing_from_recipe_act = QAction('&Ингредиенты в рецептах', self)
        ing_from_recipe_act.setShortcut('Ctrl+I')
        ing_from_recipe_act.setStatusTip('Показать ингридиенты, \
присутствующие в рецептах')
        ing_from_recipe_act.triggered.connect(ing_from_rec)

        delete_recipe_act = QAction('(Н) &Удалить рецепт', self)
        delete_recipe_act.setShortcut('Ctrl+D')
        delete_recipe_act.setStatusTip('Удалить рецепт из базы данных')
        delete_recipe_act.triggered.connect(delete_recipe)

        rate_recipe_act = QAction('(Н) &Оценить рецепт', self)
        rate_recipe_act.setShortcut('Ctrl+R')
        rate_recipe_act.setStatusTip('Поставить оценку рецепту')
        rate_recipe_act.triggered.connect(recipe_rate)

        rec_with_ing_act = QAction('(Н) &Ингредиент в рецептах', self)
        rec_with_ing_act.setShortcut('Ctrl+R')
        rec_with_ing_act.setStatusTip('Найти все рецепты с выбраным ингридиентом')
        rec_with_ing_act.triggered.connect(rec_with_ing)

        # Create statusbar.
        self.statusBar()

        # Create meny bar.
        menubar = self.menuBar()

        # Recipes meny.
        recipes_menu = menubar.addMenu('&Рецепты')
        recipes_menu.addAction(all_recipe_act)
        recipes_menu.addAction(avail_recipe_act)
        recipes_menu.addAction(ing_from_recipe_act)
        recipes_menu.addAction(delete_recipe_act)

        # Collections meny.
        collect_menu = menubar.addMenu('&Коллекция масел')
        collect_menu.addAction(collection_act)
        collect_menu.addAction(rec_with_ing_act)

        exit = menubar.addAction(exit_act)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Рецепты для аромолампы')
        self.show()

    @pyqtSlot()
    def collection(self):
        """Otput numbered and sorted igredient collection."""

        print(LG.collection_meny)
        coll = sorted(data('data/collection.txt'))
        print("Моя коллекция:")
        for count, oil in enumerate(coll,1):
            print(f"[{count}] {oil}")
        print()

    def closeEvent(self, event):
        """Event that generated when we close QWidget."""

        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# Functions of the meny actions.
#==============================================================================
# def collection():
#     """Otput numbered and sorted igredient collection."""
#
#     print(LG.collection_meny)
#     coll = sorted(data('data/collection.txt'))
#     print("Моя коллекция:")
#     for count, oil in enumerate(coll,1):
#         print(f"[{count}] {oil}")
#     print()

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

def available_recipe():
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
