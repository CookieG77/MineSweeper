from fltk import *
from classes import MineSweeper

cree_fenetre(200, 150, redimension=True)

continuer = True
PDJ = MineSweeper((10, 10), 20)
PDJ.show_plate()
while continuer:
    event = donne_ev()
    if type_ev(event) == "Quitte":
        continuer = False
    elif type_ev(event) == "Touche":
        if touche(event) == "Escape":
            continuer = False

    if type_ev(event) == "Redimension":
        efface_tout()
        print(largeur_fenetre(), hauteur_fenetre(), "a")
        PDJ.affichage()

    mise_a_jour()

ferme_fenetre()