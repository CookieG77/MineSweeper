"""
This file alloy you to play a simple MineSweeper with Python.
"""

from random import randint
from fltk import *


class MineSweeper:
    """
    Class to play MineSweeper
    """
    def __init__(self,taille: list[int, int],nbmine: int) -> None:
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
                self.grille[nbgen[0]][nbgen[1]] = ["X", False, False, 0]
                print(nbgen)
                if nbgen[0] != (self.dims[0]-1): #Vérif S
                    self.grille[nbgen[0]+1][nbgen[1]][3] +=1
                if nbgen[0] != 0: #Vérif N
                    self.grille[nbgen[0]-1][nbgen[1]][3] +=1
                if nbgen[1] != (self.dims[1]-1): #Vérif E
                    self.grille[nbgen[0]][nbgen[1]+1][3] +=1
                if nbgen[1] != 0: #Vérif O
                    self.grille[nbgen[0]][nbgen[1]-1][3] +=1
                if nbgen[0] != (self.dims[0]-1) and nbgen[1] != (self.dims[1]-1): #Vérif SE
                    self.grille[nbgen[0]+1][nbgen[1]+1][3] +=1
                if nbgen[0] != (self.dims[0]-1) and nbgen[1] != 0: #Vérif SW
                    self.grille[nbgen[0]+1][nbgen[1]-1][3] +=1
                if nbgen[0] != 0 and nbgen[1] != (self.dims[1]-1): #Vérif NE
                    self.grille[nbgen[0]-1][nbgen[1]+1][3] +=1
                if nbgen[0] != 0 and nbgen[1] != 0: #Vérif NW
                    self.grille[nbgen[0]-1][nbgen[1]-1][3] +=1
                nbmineplacer += 1

    def show_plate(self) -> None:
        """
        Yay This is a test
        """
        for dim_y in range(self.dims[0]):
            string = ""
            for dim_x in range(self.dims[1]):
                if self.grille[dim_y][dim_x][0] == "":
                    if self.grille[dim_y][dim_x][3] != 0:
                        string += str(self.grille[dim_y][dim_x][3])
                    else:
                        string += "_"
                else:
                    string += "X"
            print(string)




PDJ=MineSweeper((9,9), 5)
PDJ.show_plate()
