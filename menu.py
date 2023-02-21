"""
Permet l'affichage des différents menus
"""

from fltk import *
from mad_fltk import *

def final_screen(victory: bool):
    """
    Permet l'affichage du menu de fin
    """
    victory_button = ButtonRect((100, 100), (200, 200))
    victory_button.draw(text=str(victory))
    Run = True
    while Run:
        mise_a_jour()
        event = donne_ev()
        if type_ev(event) == "Quitte":
            Run = False
        elif type_ev(event) == "Touche":
            if touche(event) == "Escape":
                Run = False
