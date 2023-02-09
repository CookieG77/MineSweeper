from random import randint
from fltk import *


class Demineur:
    def __init__(self,taille,nbmine) -> None:
        """
        Lancement et création du plateau
        """
        self.grille = []
        for _ in range(taille[1]):
            ltemp = []
            for _ in range(taille[0]):
                ltemp.append(["", False, False]) # [Type de case, cacher?, drapeau?]
            self.grille.append(ltemp)
        nbmineplacer = 0
        while nbmineplacer != nbmine:
            if self.grille[randint(0, taille[1])][randint(0, taille[0])] != "X":
                self.grille[randint(0, taille[1])][randint(0, taille[0])] = "X"
                nbmineplacer += 1




