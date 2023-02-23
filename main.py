"""
Launch the game
"""
from fltk import (
    cree_fenetre,
    ferme_fenetre)
from menu import play_menu

cree_fenetre(400, 350, redimension=True)

play_menu((12, 14))

ferme_fenetre()
