"""
Permet l'affichage des différents menus
"""

from fltk import (
    efface_tout,
    largeur_fenetre,
    hauteur_fenetre,
    mise_a_jour,
    donne_ev,
    type_ev,
    touche,
    abscisse_souris,
    ordonnee_souris
)
from mad_fltk import (
    ButtonRect,
    ButtonCircleTex
)
from classes import (
    MineSweeper
)


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



def play_menu_setup(emoji_face: str):
    """
    Permet de générer l'affichage du menu de jeu
    """
    height = largeur_fenetre()
    length = hauteur_fenetre()
    test = ButtonCircleTex((int(height * 0.5), int(length * 0.05)), int(length * 0.04), "emoji")
    test.draw("content/textures/" + emoji_face + "_emoji.png")
    return test


def play_menu(dimentio: list[int, int]):
    """
    Permet l'affichage et le fonctionnement du menu de jeu
    """
    Run, firstclick, victory = True, True, False
    emoji_face = "neutral"
    pdj = MineSweeper((dimentio[0], dimentio[1]))
    pdj.load_affichage(firstclick)
    list_button = play_menu_setup(emoji_face)
    while Run:
        mise_a_jour()
        event = donne_ev()
        if type_ev(event) == "Quitte":
            Run = False
        elif type_ev(event) == "Touche":
            if touche(event) == "Escape":
                Run = False
        elif type_ev(event) == "Redimension":
            efface_tout()
            pdj.load_affichage(firstclick)
            list_button = play_menu_setup(emoji_face)
        elif type_ev(event) == "ClicGauche":
            pelleter = pdj.click_dig((abscisse_souris(), ordonnee_souris()), firstclick)
            if pelleter[0]:
                if firstclick:
                    firstclick = False
                    list_button = play_menu_setup(emoji_face)
                if pelleter[1]: # Si on tombe sur une bombe
                    pdj.reveal_mine(pelleter[2])
                    emoji_face = "death"
                    list_button = play_menu_setup(emoji_face)
                    # Run, VICTORY = False, False
                if pdj.check_win(): # Si il gagne
                    emoji_face = "win"
                    list_button = play_menu_setup(emoji_face)
                    # Run, victory = False, True
        elif type_ev(event) == "ClicDroit":
            pdj.click_flag((abscisse_souris(), ordonnee_souris()))
            if pdj.check_win(): # Si il gagne
                emoji_face = "win"
                list_button = play_menu_setup(emoji_face)
                # Run, victory = False, True
        pdj.update_time() #Mise à jour du chrono
    print(victory)
