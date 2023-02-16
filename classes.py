"""
This file alloy you to play a simple MineSweeper with Python.
"""

from random import randint, choice
from fltk import (
    largeur_fenetre,
    hauteur_fenetre,
    rectangle,
    image,
    efface,
    efface_tout
    )
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
                nbmineplacer += 1
                for dim_y in range(-1,2,1):
                    for dim_x in range(-1,2,1):
                        if ((0 <= nbgen[0]+dim_y <= self.dims[0]-1)
                            and (0 <= nbgen[1]+dim_x <= self.dims[1]-1)
                            and[dim_y,dim_x] != [0,0]):
                            self.grille[nbgen[0]+dim_y][nbgen[1]+dim_x][3] +=1

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

    def load_affichage(self):
        """
        Génération de l'affichage de la grille
        """
        efface_tout()
        length = hauteur_fenetre()
        height = largeur_fenetre()
        dim_y = length // self.dims[0]
        dim_x = height // self.dims[1]
        self.dim_square = min(dim_y, dim_x)
        self.start_y = (height - (self.dim_square * self.dims[1])) // 2
        self.start_x = (length - (self.dim_square * self.dims[0])) // 2
        for coord_y in range(self.dims[0]):
            for coord_x in range(self.dims[1]):
                affichage_element(self.grille[coord_y][coord_x],
                                  (coord_x * self.dim_square) + self.start_y,
                                  (coord_y * self.dim_square) + self.start_x,
                                  self.dim_square,
                                  (coord_y, coord_x))


    def click_dig(self, coord: list[int, int], firstclick: bool) -> None:
        """
        Compare les coordonnées avec la grille pour creuser
        """
        coord_x = (coord[0] - self.start_y) // self.dim_square
        coord_y = (coord[1] - self.start_x) // self.dim_square
        if ((0 <= coord_y <= self.dims[0] - 1)
            and (0 <= coord_x <= self.dims[1] - 1)
            and not self.grille[coord_y][coord_x][2]):
            print("ui")
            if firstclick:
                self.relocatemines((coord_y, coord_x))
                self.load_affichage()

            return True, self.reveal_case((coord_y, coord_x))
        return False, None


    def click_flag(self, coord: list[int, int]) -> None:
        """
        Permet de jouer avec les drapeaux
        """
        coord_x = (coord[0] - self.start_y) // self.dim_square
        coord_y = (coord[1] - self.start_x) // self.dim_square
        if ((0 <= coord_y <= self.dims[0] - 1)
           and (0 <= coord_x <= self.dims[1] - 1)
           and self.grille[coord_y][coord_x][1] is False):
            print(self.grille[coord_y][coord_x][2])
            if self.grille[coord_y][coord_x][2]:
                self.grille[coord_y][coord_x][2] = False
                print("Enlever")
            else:
                self.grille[coord_y][coord_x][2] = True
                print("Placer")
            return True
        return False


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
                return 1
            return 0
        placed = 0
        placed += delete_mine(self, coords)
        if (self.dims[0] >= 7 and self.dims[1] >= 5) or (self.dims[0] >= 5 and self.dims[1] >= 7):
            for dim_y in range(-1,2,1):
                for dim_x in range(-1,2,1):
                    if ((0 <= coords[0]+dim_y <= self.dims[0]-1)
                        and (0 <= coords[1]+dim_x <= self.dims[1]-1)
                        and[dim_y,dim_x] != [0,0]):
                        placed += delete_mine(self, [coords[0]+dim_y, coords[1]+dim_x])
        while placed != 0:
            new_mine = [[],[]]
            if (coords[0] - 2) >= 0:
                new_mine[0].append(randint(0, coords[0] - 2))
            if (coords[0] + 2) <= (self.dims[0] - 1):
                new_mine[0].append(randint(coords[0] + 2, self.dims[0] - 1))
            if (coords[1] - 2) >= 0:
                new_mine[1].append(randint(0, coords[1] - 2))
            if (coords[1] + 2) <= (self.dims[1] - 1):
                new_mine[1].append(randint(coords[1] + 2, self.dims[1] - 1))
            new_mine = [choice(new_mine[0]), choice(new_mine[1])]

            if self.grille[new_mine[0]][new_mine[1]][0] != "X":
                self.grille[new_mine[0]][new_mine[1]][0] = "X"
                self.grille[new_mine[0]][new_mine[1]][3] = 0
                for dim_y in range(-1,2,1):
                    for dim_x in range(-1,2,1):
                        if ((0 <= new_mine[0]+dim_y <= self.dims[0]-1)
                            and (0 <= new_mine[1]+dim_x <= self.dims[1]-1)
                            and[dim_y,dim_x] != [0,0]):
                            if self.grille[new_mine[0]+dim_y][new_mine[1]+dim_x][0] != "X":
                                self.grille[new_mine[0]+dim_y][new_mine[1]+dim_x][3] += 1
                placed -= 1







    def reveal_case(self, coords: list[int, int]) -> bool:
        """
        Fonction récursive pour révéler les cases.
        """
        if self.grille[coords[0]][coords[1]][0] == "X":
            return True
        def suite(self: MineSweeper, coords: list[int, int], difcoo: list[int, int]) -> None:
            """
            Si la case au coordonnées donner est proche d'une mine on l'affiche juste,
            mais si elle est juste vide et pas proche d'une mine on affiche encore autour.
            """
            if (self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][1] is not True
                and not self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][2]):
                if (self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][0] == ""
                    and self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][3]) > 0:
                    self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][1] = True
                    efface("case" + str(coords[0] + difcoo[0]) + "-" + str(coords[1] + difcoo[1]))
                elif self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][0] == "":
                    self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][1] = True
                    self.reveal_case([coords[0] + difcoo[0], coords[1] + difcoo[1]])
                    efface("case" + str(coords[0] + difcoo[0]) + "-" + str(coords[1] + difcoo[1]))

        suite(self, coords, [0,0])
        if self.grille[coords[0]][coords[1]][3] == 0:
            for dim_y in range(-1,2,1):
                for dim_x in range(-1,2,1):
                    if ((0 <= coords[0]+dim_y <= self.dims[0]-1)
                        and (0 <= coords[1]+dim_x <= self.dims[1]-1)
                        and[dim_y,dim_x] != [0,0]):
                        suite(self, coords, [dim_y,dim_x])
        return False


def affichage_element(case, coord_x, coord_y, dim, coords: list[int, int]):
    """
    Permet d'afficher l'élément correspondant à la case dans la grille
    """
    list_color = ["#0000FD", "#017E00", "#FE0000", "#003B6F",
                  "#830003", "#008080", "#000000", "#808080"]
    if case[0] == "X": # Mine
        rectangle(coord_x, coord_y, coord_x + dim, coord_y + dim, remplissage="#000000")
    elif case[3] != 0: # Case numéroté visible
        Text((coord_x, coord_y),
             (coord_x + dim, coord_y + dim),
             str(case[3])).draw(list_color[case[3] - 1])
    if case[1] is False: # Case caché
        image(coord_x + dim//2, coord_y + dim//2, "content/textures/HiddenCase.png", dim, dim,
              tag="case" + str(coords[0]) + "-" + str(coords[1]))
    rectangle(coord_x, coord_y, coord_x + dim, coord_y + dim) # Case vide visible
    if case[2]:
        rectangle(coord_x, coord_y, coord_x + 10, coord_y + 10, remplissage= "#FF0000")




