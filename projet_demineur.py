"""
This file alloy you to play a simple MineSweeper with Python.
"""

from random import randint
#from fltk import *


class MineSweeper:
    """
    Class to play MineSweeper
    """
    def __init__(self,taille: list[int, int],nbmine: int = 0) -> None:
        """
        Lancement et création du plateau
        """
        if nbmine == 0:
            nbmine = int(taille[0] * taille[1] * 0.16)
        self.grille = []
        self.dims = taille
        for _ in range(taille[0]):
            ltemp = []
            for _ in range(taille[1]):
                #Format d'une case : [Type de case, cacher?, drapeau?, nb mines autour]
                ltemp.append(["", False, False, 0])
            self.grille.append(ltemp)
        nbmineplacer = 0
        while nbmineplacer < nbmine:
            nbgen = (randint(0, taille[0]-1), randint(0, taille[1]-1))
            if self.grille[nbgen[0]][nbgen[1]][0] != "X":
                self.grille[nbgen[0]][nbgen[1]] = ["X", False, False, 0]
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
            string = "|"
            print("*---"*self.dims[1] + "*")
            for dim_x in range(self.dims[1]):
                if self.grille[dim_y][dim_x][0] == "":
                    if self.grille[dim_y][dim_x][3] != 0: #Case vide mais mine à coté
                        string += str(" ") + str(self.grille[dim_y][dim_x][3]) + str(" ")
                    else: string += "   " #Case vide
                else: string += " X " #Case avec mine
                string += "|"
            print(string)
        print("*---"*self.dims[1] + "*")

    def check_win(self) -> bool:
        """
        Retourne un booléen qui dit si la partie est gagnée.
        """
        for dim_y in range(self.dims[0]):
            for dim_x in range(self.dims[1]):
                if ((self.grille[dim_y][dim_x][2] is not True)
                    and (self.grille[dim_y][dim_x][0] == "X")):
                    return False
        return True

    def reveal_case(self, coords: list[int, int]) -> None:
        """
        Fonction récursive pour révéler les cases.
        """
        def suite(self, coords: list[int, int], difcoo: list[int, int]) -> None:
            """
            Si la case au coordonnées donner est proche d'une mine on l'affiche juste,
            mais si elle est juste vide et pas proche d'une mine on affiche encore autour.
            """
            if self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][1] is True:
                if (self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][0] == ""
                    and self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][3]) > 0:
                    self.reveal_case([coords[0] + difcoo[0], coords[1] + difcoo[1]])
                elif self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][0] == "":
                    self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][1] = True
        if coords[0] != (self.dims[0]-1): #Vérif S
            suite(self, coords, [1,0])
        if coords[0] != 0: #Vérif N
            suite(self, coords, [-1,0])
        if coords[1] != (self.dims[1]-1): #Vérif E
            suite(self, coords, [0,1])
        if coords[1] != 0: #Vérif O
            suite(self, coords, [0,-1])
        if (coords[0] != (self.dims[0]-1)
            and coords[1] != (self.dims[1]-1)): #Vérif SE
            suite(self, coords, [1,1])
        if (coords[0] != (self.dims[0]-1)
            and coords[1] != 0): #Vérif SW
            suite(self, coords, [1,-1])
        if (coords[0] != 0
            and coords[1] != (self.dims[1]-1)): #Vérif NE
            suite(self, coords, [-1,1])
        if (coords[0] != 0
            and coords[1] != 0): #Vérif NW
            suite(self, coords, [-1,-1])

PDJ=MineSweeper((5,7))
PDJ.show_plate()
