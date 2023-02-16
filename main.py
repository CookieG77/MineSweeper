from fltk import *
from classes import MineSweeper




cree_fenetre(400, 350, redimension=True)

Run = True
PDJ = MineSweeper((14, 18), 40)
PDJ.show_plate(True )
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
        if PDJ.click_dig((abscisse_souris(), ordonnee_souris()), FIRSTCLICK)[0]:
            if FIRSTCLICK:
                FIRSTCLICK = False
            #
            #PDJ.show_plate()
    elif type_ev(event) == "ClicDroit":
        if PDJ.click_flag((abscisse_souris(), ordonnee_souris())):
            pass
            #

ferme_fenetre()
