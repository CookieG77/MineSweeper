"""
Permet l'affichage des différents menus
"""

from fltk import *
from mad_fltk import *


def start_menu_setup():
    """
    Permet de générer l'affichage du menu de démarage
    """
    efface_tout()
    height = largeur_fenetre()
    length = hauteur_fenetre()
    play_button = ButtonRect((int(height * 0.1), int(length * 0.1)),
                             (int(height * 0.2), int(length * 0.1)))
    return play_button, None


def start_menu():
    """
    Permet l'affichage et le fonctionnement du menu de démarage
    """
    list_button = start_menu_setup()
    Run = True
    list_button[0].draw(text="Play")
    while Run:
        mise_a_jour()
        event = donne_ev()
        if type_ev(event) == "Quitte":
            Run = False
        elif type_ev(event) == "Touche":
            if touche(event) == "Escape":
                Run = False
        elif type_ev(event) == "Redimension":
            list_button = start_menu_setup()
            list_button[0].draw(text="Play")



def final_screen_setup():
    """
    Permet de générer l'affichage du pop-up de fin
    """
    efface_tout()
    height = largeur_fenetre()
    length = hauteur_fenetre()
    rectangle(0, 0, height, length, epaisseur=0, remplissage="#C0C0C0")
    victory_button = ButtonRect((int(height * 0.1), int(length * 0.1)),
                                (int(height * 0.9), int(length * 0.9)))
    return victory_button, None


def final_screen(victory: bool):
    """
    Permet l'affichage du menu de fin
    """
    list_button = final_screen_setup()
    color = "#FF0000"
    if victory:
        color = "#00FF00"
    Run = True
    list_button[0].draw(color, text=str(victory))
    while Run:
        mise_a_jour()
        event = donne_ev()
        if type_ev(event) == "Quitte":
            Run = False
        elif type_ev(event) == "Touche":
            if touche(event) == "Escape":
                Run = False
        elif type_ev(event) == "Redimension":
            list_button = final_screen_setup()
            list_button[0].draw(color, text=str(victory))
        