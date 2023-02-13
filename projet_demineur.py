"""
This file alloy you to play a simple MineSweeper with Python.
"""

from random import randint
#from fltk import *


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
                #Format d'une case : [Type de case, cacher?, drapeau?, nb mines autour]
                ltemp.append(["", False, False, 0])
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
            string = "|"
            print("*---"*self.dims[0] + "*")
            for dim_x in range(self.dims[1]):
                if self.grille[dim_y][dim_x][0] == "":
                    if self.grille[dim_y][dim_x][3] != 0: #Case vide mais mine à coté
                        string += str(" ") + str(self.grille[dim_y][dim_x][3]) + str(" ")
                    else: string += "   " #Case vide
                else: string += " X " #Case avec mine
                string += "|"
            print(string)
        print("*---"*self.dims[0] + "*")

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
        if coords[0] != (self.dims[0]-1): #Vérif S
            if self.grille[coords[0]+1][coords[1]][0] == "" and self.grille[coords[0]+1][coords[1]][3] > 0:
                pass
            elif self.grille[coords[0]+1][coords[1]][0] == "":
                pass
        if coords[0] != 0: #Vérif N
            if self.grille[coords[0]-1][coords[1]][0] == "" and self.grille[coords[0]-1][coords[1]][3] > 0:
                pass
            elif self.grille[coords[0]-1][coords[1]][0] == "":
                pass
        if coords[1] != (self.dims[1]-1): #Vérif E
            if self.grille[coords[0]][coords[1]+1][0] == "" and self.grille[coords[0]][coords[1]+1][3] > 0:
                pass
            elif self.grille[coords[0]][coords[1]+1][0] == "":
                pass
        if coords[1] != 0: #Vérif O
            if self.grille[coords[0]][coords[1]-1][0] == "" and self.grille[coords[0]][coords[1]-1][3] > 0:
                pass
            elif self.grille[coords[0]][coords[1]-1][0] == "":
                pass
        if coords[0] != (self.dims[0]-1) and coords[1] != (self.dims[1]-1): #Vérif SE
            if self.grille[coords[0]+1][coords[1]+1][0] == "" and self.grille[coords[0]+1][coords[1]+1][3] > 0:
                pass
            elif self.grille[coords[0]+1][coords[1]+1][0] == "":
                pass
        if coords[0] != (self.dims[0]-1) and coords[1] != 0: #Vérif SW
            if self.grille[coords[0]+1][coords[1]-1] == "" and self.grille[coords[0]+1][coords[1]-1] > 0:
                pass
            elif self.grille[coords[0]+1][coords[1]-1] == "":
                pass
        if coords[0] != 0 and coords[1] != (self.dims[1]-1): #Vérif NE
            if self.grille[coords[0]-1][coords[1]+1] == "" and self.grille[coords[0]-1][coords[1]+1] > 0:
                pass
            elif self.grille[coords[0]-1][coords[1]+1] == "":
                pass
        if coords[0] != 0 and coords[1] != 0: #Vérif NW
            if self.grille[coords[0]-1][coords[1]-1] == "" and self.grille[coords[0]-1][coords[1]-1] > 0:
                pass
            elif self.grille[coords[0]-1][coords[1]-1] == "":
                pass

PDJ=MineSweeper((9,9), 5)
PDJ.show_plate()
