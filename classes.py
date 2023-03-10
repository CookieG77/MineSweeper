"""
This file alloy you to play a simple MineSweeper with Python.
"""
import threading
from random import randint, choice
from PIL import Image
from time import time
from playsound import playsound
from fltk import (
    largeur_fenetre,
    hauteur_fenetre,
    rectangle,
    image,
    efface,
    efface_tout)
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
        self.nb_case_visible = 0
        self.mine_coord = []
        self.time, self.startingtime = 0, time()
        self.flag_coord = []
        # Pour l'affichage
        self.start_x, self.start_y = 0, 0
        self.chronopos, self.counterpos = [0, 0], [0, 0]
        self.chonoscale = [24,14]
        self.dim_square = 0
        self.last_left_click = [[-1, -1], 0]

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
                self.mine_coord.append([nbgen[0], nbgen[1]])
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
        string = "*---"*self.dims[1] + "*"
        for dim_y in range(self.dims[0]):
            string += "\n|"
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
            string += "\n" + ("*---"*self.dims[1] + "*")
        print(string)


    def load_affichage(self, firstclick=False):
        """
        Génération de l'affichage de la grille
        """
        efface_tout()
        length = hauteur_fenetre() // 10 * 9
        height = largeur_fenetre()
        dim_y = length // self.dims[0]
        dim_x = height // self.dims[1]
        self.dim_square = min(dim_y, dim_x)
        self.start_y = (height - (self.dim_square * self.dims[1])) // 2
        self.start_x = (length - (self.dim_square * self.dims[0])) // 2 + (hauteur_fenetre() // 10)
        num_width, num_height = Image.open("./content/textures/0.png").size
        self.chronopos = [self.start_y+self.dim_square*(self.dims[1]-1), hauteur_fenetre() //20]
        self.chonoscale = [int(num_width*(self.dim_square*self.dims[0]/30*2/num_height)),
                           int(self.dim_square*self.dims[0]/30*2)]
        self.counterpos = [self.start_y+self.dim_square+2*self.chonoscale[0], hauteur_fenetre() //20]
        #Couleur fond
        rectangle(0, 0, largeur_fenetre(), hauteur_fenetre(), remplissage="#c0c0c0", epaisseur=0)
        for coord_y in range(self.dims[0]):
            for coord_x in range(self.dims[1]):
                affichage_case(self.grille[coord_y][coord_x],
                               ((coord_x * self.dim_square) + self.start_y,
                               (coord_y * self.dim_square) + self.start_x),
                               self.dim_square, (coord_y, coord_x),
                               firstclick)
        self.affichage_chrono()
        self.affichage_counter()


    def click_dig(self, coords: list[int, int], firstclick: bool) -> None:
        """
        Compare les coordonnées avec la grille pour creuser
        """
        coord_x = (coords[0] - self.start_y) // self.dim_square
        coord_y = (coords[1] - self.start_x) // self.dim_square
        if ((0 <= coord_y <= self.dims[0] - 1)
            and (0 <= coord_x <= self.dims[1] - 1)
            and not self.grille[coord_y][coord_x][2]):
            if firstclick:
                self.relocatemines((coord_y, coord_x))
                self.load_affichage()
            if not self.grille[coord_y][coord_x][1]:
                check_death = self.reveal_case((coord_y, coord_x))
                if check_death:
                    mp3file="content/sounds/explosion.wav"
                    playmysound(mp3file)
                else:
                    mp3file="content/sounds/select.wav"
                    playmysound(mp3file)
                return True, check_death, (coord_y, coord_x)
            elif (self.grille[coord_y][coord_x][1] is True
                and self.grille[coord_y][coord_x][3] > 0):
                check_death = self.reveal_case_nearby([coord_y, coord_x])
                if check_death:
                    mp3file="content/sounds/explosion.wav"
                    playmysound(mp3file)
                    self.reveal_case((coord_y, coord_x))
                else:
                    mp3file="content/sounds/select.wav"
                    playmysound(mp3file)
                return True, check_death, (coord_y, coord_x)
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
            if self.grille[coord_y][coord_x][2]: #Suppresion drapeau
                self.grille[coord_y][coord_x][2] = False
                efface("flag" + str(coord_y) + "-" + str(coord_x))
                playmysound("content/sounds/retirdrapeau.wav")
                self.flag_coord.remove([coord_y, coord_x])
                self.affichage_counter()
            else: #Ajout drapeau
                if len(self.flag_coord) < self.nbmine:
                    self.grille[coord_y][coord_x][2] = True
                    image(coord_x * self.dim_square + self.start_y + self.dim_square//2,
                        coord_y * self.dim_square + self.start_x + self.dim_square//2,
                        "content/textures/Flag.png",
                        self.dim_square, self.dim_square,
                        tag="flag" + str(coord_y) + "-" + str(coord_x))
                    playmysound("content/sounds/poserdrapeau.wav")
                    self.flag_coord.append([coord_y, coord_x])
                    self.affichage_counter()


    def check_win(self) -> bool:
        """
        Retourne un booléen qui dit si la partie est gagnée.
        """
        A, B = True, True
        for mine in self.mine_coord:
            if self.grille[mine[0]][mine[1]][2] is False:
                A = False
        if self.nb_case_visible != (self.dims[0]*self.dims[1]-self.nbmine):
            B = False
        if A or B :
            return True
        return False


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
                self.mine_coord.remove([coords[0], coords[1]])

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
                self.mine_coord.append([new_mine[0], new_mine[1]])
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
        def suite(self: MineSweeper, coords: list[int, int], difcoo: list[int, int]) -> None:
            """
            Si la case au coordonnées donner est proche d'une mine on l'affiche juste,
            mais si elle est juste vide et pas proche d'une mine on affiche encore autour.
            """
            if (self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][1] is not True
                and not self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][2]):
                if (self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][0] == ""
                    and self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][3] > 0):
                    self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][1] = True
                    efface("case" + str(coords[0] + difcoo[0]) + "-" + str(coords[1] + difcoo[1]))
                    self.nb_case_visible += 1
                elif self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][0] == "":
                    self.grille[coords[0]+difcoo[0]][coords[1]+difcoo[1]][1] = True
                    self.reveal_case([coords[0] + difcoo[0], coords[1] + difcoo[1]])
                    efface("case" + str(coords[0] + difcoo[0]) + "-" + str(coords[1] + difcoo[1]))
                    self.nb_case_visible += 1


        if self.grille[coords[0]][coords[1]][0] == "X":
            return True
        suite(self, coords, [0,0])
        if self.grille[coords[0]][coords[1]][3] == 0:
            for dim_y in range(-1,2,1):
                for dim_x in range(-1,2,1):
                    if ((0 <= coords[0]+dim_y <= self.dims[0]-1)
                        and (0 <= coords[1]+dim_x <= self.dims[1]-1)
                        and[dim_y,dim_x] != [0,0]):
                        suite(self, coords, [dim_y,dim_x])
        return False


    def reveal_case_nearby(self, coords: list[int, int]) -> None:
        """
        Fonction permettant de mettre à jour le double clique sur une case,
        et de révéler les case vides si toutes les mines alentour sont marqué d'un drapeau.
        """
        if coords == self.last_left_click[0]:
            reveal = 0
            for dim_y in range(-1,2,1):
                for dim_x in range(-1,2,1):
                    if ((0 <= coords[0]+dim_y <= self.dims[0]-1)
                        and (0 <= coords[1]+dim_x <= self.dims[1]-1)
                        and [dim_y,dim_x] != [0,0]):
                        if (self.grille[coords[0]+dim_y][coords[1]+dim_x][2]):
                            reveal += 1
            if reveal == self.grille[coords[0]][coords[1]][3]:
                for dim_y in range(-1,2,1):
                    for dim_x in range(-1,2,1):
                        if ((0 <= coords[0]+dim_y <= self.dims[0]-1)
                            and (0 <= coords[1]+dim_x <= self.dims[1]-1)
                            and [dim_y,dim_x] != [0,0]):
                            if self.grille[coords[0]+dim_y][coords[1]+dim_x][0] != "X":
                                if self.grille[coords[0]+dim_y][coords[1]+dim_x][3] == 0:
                                    self.reveal_case([coords[0]+dim_y,coords[1]+dim_x])
                                else:
                                    self.grille[coords[0]+dim_y][coords[1]+dim_x][1] = True
                                    efface("case" + str(coords[0] + dim_y) + "-" + str(coords[1] + dim_x))
                            elif not self.grille[coords[0]+dim_y][coords[1]+dim_x][2]:
                                return True
                self.last_left_click[0] = [-1, -1]
        else:
            self.last_left_click[0] = [coords[0], coords[1]]
        return False


    def update_time(self) -> None:
        """
        Met à jour le temps en seconde depuis le lancement du programme.
        """
        if (self.last_left_click[0] != [-1, -1]
            and self.last_left_click[1] == 2):
            self.last_left_click = [[-1, -1], 0]
        time_since_start = int(time() - self.startingtime)
        if time_since_start != self.time:
            if (self.last_left_click[0] != [-1, -1]): #Reset du double click
                self.last_left_click[1] += 1
            self.time = time_since_start #Update du temps et chrono
            self.affichage_chrono()


    def affichage_chrono(self) -> None:
        """
        Fonction pour afficher le chronomètre
        """
        efface("chrono_number")
        rectangle(self.chronopos[0]+self.chonoscale[0]//2,
                  self.chronopos[1]+self.chonoscale[1]//2,
                  self.chronopos[0]-self.chonoscale[0]*2.5,
                  self.chronopos[1]-self.chonoscale[1]//2,
                  remplissage="#000000", epaisseur=0,
                  tag="chrono_number")
        if len(str(self.time)) == 1:
            image(self.chronopos[0],
                  self.chronopos[1] , "content/textures/"+ str(self.time) +".png",
                  self.chonoscale[0],
                  self.chonoscale[1],
                  tag="chrono_number")
            for i in range(1,3,1):
                image(int(self.chronopos[0] - i*14*(self.dim_square*self.dims[0]/30*2/24)),
                      self.chronopos[1] , "content/textures/empty.png",
                      self.chonoscale[0],
                      self.chonoscale[1],
                      tag="chrono_number")
        elif len(str(self.time)) == 2:
            for i in range(2):
                image(int(self.chronopos[0] - i*14*(self.dim_square*self.dims[0]/30*2/24)),
                      self.chronopos[1] , "content/textures/"+ str(self.time)[1-i] +".png",
                      self.chonoscale[0],
                      self.chonoscale[1],
                      tag="chrono_number")
            image(int(self.chronopos[0] - 2*14*(self.dim_square*self.dims[0]/30*2/24)),
                  self.chronopos[1] , "content/textures/empty.png",
                  self.chonoscale[0],
                  self.chonoscale[1],
                  tag="chrono_number")
        elif len(str(self.time)) == 3:
            for i in range(3):
                image(int(self.chronopos[0] - i*14*(self.dim_square*self.dims[0]/30*2/24)),
                      self.chronopos[1] , "content/textures/"+ str(self.time)[2-i] +".png",
                      self.chonoscale[0],
                      self.chonoscale[1],
                      tag="chrono_number")
        else:
            for i in range(3):
                image(int(self.chronopos[0] - i*14*(self.dim_square*self.dims[0]/30*2/24)),
                      self.chronopos[1] , "content/textures/9.png",
                      self.chonoscale[0],
                      self.chonoscale[1],
                      tag="chrono_number")


    def affichage_counter(self) -> None:
        """
        Permet de mettre à jour le compteur de drapeau restant à placer.
        """
        nb_flag = self.nbmine - len(self.flag_coord)
        efface("counter_number")
        rectangle(self.counterpos[0]+self.chonoscale[0]//2,
                  self.counterpos[1]+self.chonoscale[1]//2,
                  self.counterpos[0]-self.chonoscale[0]*2.5,
                  self.counterpos[1]-self.chonoscale[1]//2,
                  remplissage="#000000", epaisseur=0,
                  tag="counter_number")
        if len(str(nb_flag)) == 1:
            image(self.counterpos[0],
                  self.counterpos[1] , "content/textures/"+ str(nb_flag) +".png",
                  self.chonoscale[0],
                  self.chonoscale[1],
                  tag="counter_number")
            for i in range(1,3,1):
                image(int(self.counterpos[0] - i*14*(self.dim_square*self.dims[0]/30*2/24)),
                      self.counterpos[1] , "content/textures/empty.png",
                      self.chonoscale[0],
                      self.chonoscale[1],
                      tag="counter_number")
        elif len(str(nb_flag)) == 2:
            for i in range(2):
                image(int(self.counterpos[0] - i*14*(self.dim_square*self.dims[0]/30*2/24)),
                      self.counterpos[1] , "content/textures/"+ str(nb_flag)[1-i] +".png",
                      self.chonoscale[0],
                      self.chonoscale[1],
                      tag="counter_number")
            image(int(self.counterpos[0] - 2*14*(self.dim_square*self.dims[0]/30*2/24)),
                  self.counterpos[1] , "content/textures/empty.png",
                  self.chonoscale[0],
                  self.chonoscale[1],
                  tag="counter_number")
        elif len(str(nb_flag)) == 3:
            for i in range(3):
                image(int(self.counterpos[0] - i*14*(self.dim_square*self.dims[0]/30*2/24)),
                      self.counterpos[1] , "content/textures/"+ str(nb_flag)[2-i] +".png",
                      self.chonoscale[0],
                      self.chonoscale[1],
                      tag="counter_number")
        else:
            for i in range(3):
                image(int(self.counterpos[0] - i*14*(self.dim_square*self.dims[0]/30*2/24)),
                      self.counterpos[1] , "content/textures/9.png",
                      self.chonoscale[0],
                      self.chonoscale[1],
                      tag="counter_number")



    def reveal_mine(self, coord: list[int, int]) -> None:
        """
        Permet de révéler toutes les mines du plateaux
        """
        for mine in self.mine_coord:
            if mine not in self.flag_coord:
                efface("case" + str(mine[0]) + "-" + str(mine[1]))
            if mine[0] != coord[0] or mine[1] != coord[1]:
                efface("death" + str(mine[0]) + "-" + str(mine[1]))
        for flag in self.flag_coord:
            if flag not in self.mine_coord:
                efface("flag" + str(flag[0]) + "-" + str(flag[1]))


def affichage_case(case: list, coords_start: list[int, int],
                      dim: int, coords: list[int, int],
                      firstclick: bool) -> None:

    """
    Permet d'afficher l'élément correspondant à la case dans la grille
    """
    list_color = ["#0000FD", "#017E00", "#FE0000", "#003B6F",
                  "#830003", "#008080", "#000000", "#808080"]
    if case[0] == "X" and not firstclick: # Mine
        rectangle(coords_start[0], coords_start[1],
                  coords_start[0] + dim, coords_start[1] + dim,
                  remplissage="#FF0000",
                  tag="death" + str(coords[0]) + "-" + str(coords[1]))
        image(coords_start[0] + dim//2,
              coords_start[1] + dim//2,
              "content/textures/Mine.png",
              dim, dim)
    # Case numéroté visible
    elif case[3] != 0 and not firstclick:
        Text((coords_start[0], coords_start[1]),
             (coords_start[0] + dim, coords_start[1] + dim),
             str(case[3])).draw(list_color[case[3] - 1])

    # Case vide visible
    rectangle(coords_start[0], coords_start[1],
              coords_start[0] + dim, coords_start[1] + dim,
              couleur= "#808080")

    # Case caché
    if not case[1]:
        image(coords_start[0] + dim//2,
              coords_start[1] + dim//2,
              "content/textures/HiddenCase.png",
              dim, dim,
              tag="case" + str(coords[0]) + "-" + str(coords[1]))

    # Drapeau
    if case[2]:
        image(coords_start[0] + dim//2,
              coords_start[1] + dim//2,
              "content/textures/Flag.png",
              dim, dim,
              tag="flag" + str(coords[0]) + "-" + str(coords[1]))






def playmysound(file: str) -> None:
    """
    Permet de jouer un son sans mettre en pause le reste du programme.
    """
    play = threading.Thread(target=playsound, args=(file,))
    play.start()
 