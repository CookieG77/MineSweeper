"""
This file alloy you to play a simple MineSweeper with Python.
"""

from random import randint
from fltk import *


class MineSweeper:
    """
    Class to play MineSweeper
    """
    def __init__(self,taille,nbmine) -> None:
        """
        Lancement et création du plateau
        """
        self.grille = []
        self.dims = taille
        for _ in range(taille[1]):
            ltemp = []
            for _ in range(taille[0]):
                ltemp.append(["", False, False, 0]) # [Type de case, cacher?, drapeau?]
            self.grille.append(ltemp)
        nbmineplacer = 0
        while nbmineplacer < nbmine:
            nbgen = (randint(0, taille[1]-1), randint(0, taille[0]-1))
            if self.grille[nbgen[0]][nbgen[1]][0] != "X":
                self.grille[nbgen[0]][nbgen[1]][0] = "X"
                if nbgen[0] == self.dims[0]:
                    pass
                elif nbgen[0] == 0:
                    pass
                if nbgen[1] == self.dims[1]:
                    pass
                elif nbgen[1] == 0:
                    pass
                nbmineplacer += 1

    def ShowPlate(self) -> None:
        """
        Yay This is a test
        """
        for y in range(self.dims[0]):
            string = ""
            for x in range(self.dims[1]):
                if self.grille[y][x][0] == "":
                    if self.grille[y][x][3] != 0:
                        string += str(self.grille[y][x][3])
                    else:
                        string += "_"
                else:
                    string += "X"
            print(string)
                



PDJ=MineSweeper((5,5), 5)
PDJ.ShowPlate()
