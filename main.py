from fltk import *
from classes import MineSweeper




cree_fenetre(400, 350, redimension=True)

Run = True
PDJ = MineSweeper((10, 10), 20)
PDJ.show_plate()
PDJ.affichage()
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
        print(largeur_fenetre(), hauteur_fenetre(), "a")
        PDJ.affichage()
    elif type_ev(event) == "ClicGauche":
        PDJ.click_dig((abscisse_souris(), ordonnee_souris()))

ferme_fenetre()