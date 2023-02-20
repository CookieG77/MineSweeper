"""
Launch the game
"""
from fltk import (
    cree_fenetre,
    mise_a_jour,
    type_ev,
    donne_ev,
    touche,
    efface_tout,
    abscisse_souris,
    ordonnee_souris,
    ferme_fenetre)
from classes import MineSweeper

cree_fenetre(400, 350, redimension=True)

Run, VICTORY = True, False
PDJ = MineSweeper((69, 69))
PDJ.load_affichage()
FIRSTCLICK = True
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
        #print(largeur_fenetre(), hauteur_fenetre(), "a")
        PDJ.load_affichage()
    elif type_ev(event) == "ClicGauche":
        pelleter = PDJ.click_dig((abscisse_souris(), ordonnee_souris()), FIRSTCLICK)
        if pelleter[0]:
            if FIRSTCLICK:
                FIRSTCLICK = False
            if pelleter[1]: # Si on tombe sur une bombe
                PDJ.reveal_mine(pelleter[2])
                # Run, VICTORY = False, False
            if PDJ.check_win():
                pass
                # Run, VICTORY = False, True
    elif type_ev(event) == "ClicDroit":
        PDJ.click_flag((abscisse_souris(), ordonnee_souris()))
        if PDJ.check_win():
            pass
            # Run, VICTORY = False, True


print(VICTORY)
ferme_fenetre()
