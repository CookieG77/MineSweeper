"""
This file alloy you to play a simple MineSweeper with Python.
"""

from random import randint
from fltk import largeur_fenetre,hauteur_fenetre,rectangle
from mad_fltk import (
    Text
)


class MineSweeper:
    """
    Class to play MineSweeper
    """
    def __init__(self,taille: list[int, int],nbmine: int = -1) -> None:
        """
        Lancement et création du plateau
        """
        if nbmine < 0:
            self.nbmine = int(taille[0] * taille[1] * 0.16)
        else: self.nbmine = nbmine
        self.grille = []
        self.length = taille[0]
        self.height = taille[1]
        self.dims = taille
        # Pour l'affichage
        self.start_x = 0
        self.start_y = 0
        self.dim_square = 0
        for _ in range(taille[0]):
            ltemp = []
            for _ in range(taille[1]):
                #Format d'une case : [Type de case, découverte?, drapeau?, nb mines autour]
                ltemp.append(["", False, False, 0])
            self.grille.append(ltemp)
        nbmineplacer = 0
        while nbmineplacer < self.nbmine:
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

    def show_plate(self, hidden: bool = True) -> None:
        """
        Yay This is a test
        """
        for dim_y in range(self.dims[0]):
            string = "|"
            print("*---"*self.dims[1] + "*")
            for dim_x in range(self.dims[1]):
                if self.grille[dim_y][dim_x][1] is True or not hidden:
                    if self.grille[dim_y][dim_x][0] == "":
                        if self.grille[dim_y][dim_x][3] != 0: #Case vide mais mine à coté
                            string += str(" ") + str(self.grille[dim_y][dim_x][3]) + str(" ")
                        else: string += "   " #Case vide
                    else: string += " X " #Case avec mine
                else:
                    string += " C "
                string += "|"
            print(string)
        print("*---"*self.dims[1] + "*")

    def affichage(self):
        """
        Affichage de la grille
        """
        length = largeur_fenetre()
        width = hauteur_fenetre()

        dim_x = length / self.length
        dim_y = width / self.height

        if dim_x <= dim_y:
            self.dim_square = int(dim_x)
        else:
            self.dim_square = int(dim_y)
        self.start_x = (length - (self.length * self.dim_square)) // 2
        self.start_y = (width - (self.height * self.dim_square)) // 2
        print(self.start_x, self.start_y ,self.dim_square)
        for coord_y in range(self.length):
            start_y_temp = self.start_y
            for coord_x in range(self.height):
                affichage_element(self.grille[coord_x][coord_y],
                                  self.start_x,
                                  start_y_temp,
                                  self.dim_square)
                start_y_temp += self.dim_square
            self.start_x += self.dim_square

    def click_dig(self, coord):
        """
        Compare les coordonnées avec la grille pour creuser
        """
        coord_x = (coord[0] - self.start_x) // self.dim_square
        coord_y = (coord[1] - self.start_y) // self.dim_square
        print(coord_x, coord_y)

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


    def relocatemines(self, coords: list[int, int]) -> None:
        """
        Permet de déplacer les mines à un emplacement donner autre part sur le plateau.
        """
        def delete_mine(self: MineSweeper, coords: list[int, int]) -> None:
            """
            Supprime une mine à un endroit donner et actualise la valeur des cases autours.
            """
            if self.grille[coords[0]][coords[1]][0] == "X":
                self.grille[coords[0]][coords[1]][0] = ""
                self.grille[coords[0]][coords[1]][3] = 0

                for dim_y in range(-1,2,1):
                    for dim_x in range(-1,2,1):
                        if ((0 <= coords[0]+dim_y <= self.dims[0]-1)
                            and (0 <= coords[1]+dim_x <= self.dims[1]-1)
                            and[dim_y,dim_x] != [0,0]):
                            if self.grille[coords[0]+dim_y][coords[1]+dim_x][0] == "":
                                self.grille[coords[0]+dim_y][coords[1]+dim_x][3] -= 1
                            elif self.grille[coords[0]+dim_y][coords[1]+dim_x][0] == "X":
                                self.grille[coords[0]][coords[1]][3] += 1

        delete_mine(self, coords)
        if (self.dims[0] >= 7 and self.dims[1] >= 5) or (self.dims[0] >= 5 and self.dims[1] >= 7):
            for dim_y in range(-1,2,1):
                for dim_x in range(-1,2,1):
                    print(dim_y, dim_x)
                    if ((0 <= coords[0]+dim_y <= self.dims[0]-1)
                        and (0 <= coords[1]+dim_x <= self.dims[1]-1)
                        and[dim_y,dim_x] != [0,0]):
                        delete_mine(self, [coords[0]+dim_y, coords[1]+dim_x])


    def reveal_case(self, coords: list[int, int]) -> None:
        """
        Fonction récursive pour révéler les cases.
        """
        def suite(self: MineSweeper, coords: list[int, int], difcoo: list[int, int]) -> None:
            """
            Si la case au coordonnées donner est proche d'une mine on l'affiche juste,
            mais si elle est juste vide et pas proche d'une mine on affiche encore autour.
            """
            if self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][1] is not True:
                if (self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][0] == ""
                    and self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][3]) > 0:
                    self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][1] = True
                elif self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][0] == "":
                    self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][1] = True
                    self.reveal_case([coords[0] + difcoo[0], coords[1] + difcoo[1]])

        suite(self, coords, [0,0])
        if self.grille[coords[0]][coords[1]][3] == 0:
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


def affichage_element(case, coord_x, coord_y, dim):
    """
    Permet d'afficher l'élément correspondant à la case dans la grille
    """
    list_color = ["#0000FD", "#017E00", "#FE0000", "#003B6F",
                  "#830003", "#008080", "#000000", "#808080"]
    if case[0] == "X":
        rectangle(coord_x, coord_y, coord_x + dim, coord_y + dim, remplissage="#000000")
    elif case[3] != 0:
        Text((coord_x, coord_y),
             (coord_x + dim, coord_y + dim),
             str(case[3])).draw(list_color[case[3] - 1])
    rectangle(coord_x, coord_y, coord_x + dim, coord_y + dim)



TDJ = MineSweeper((5,7))
TDJ.relocatemines((3,3))
TDJ.reveal_case((3,3))
TDJ.show_plate()
TDJ.show_plate(False)
