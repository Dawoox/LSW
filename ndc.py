import pyxel


class App:
    def __init__(self):
        pyxel.init(128, 128, fps=30, title="Les sauces WAA")
        self.carte = Carte()
        self.joueur1 = Joueur(1, self.carte)
        self.joueur2 = Joueur(2, self.carte)
        self.prc = (100, 0, 0)
        self.temps = 40
        self.FIN = False
        self.nbGagnant = 0
        pyxel.load("theme.pyxres")
        pyxel.playm(0, loop=True)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        # Verification du temps restant
        if self.temps <= 0:
            self.calc_gagnant()
            self.FIN = True
        # Si le temps 
        if not self.FIN:
            self.calc_temps()
            self.joueur1.update()
            self.joueur2.update()
            self.prc = self.carte.calc_prc()

    def calc_gagnant(self):
        if self.prc[1] > self.prc[2]:
            self.nbGagnant = 1
        elif self.prc[1] < self.prc[2]:
            self.nbGagnant = 2
        else:
            self.nbGagnant = 0

    def draw_fin(self):
        if not self.nbGagnant == 0:
            pyxel.text(50, 20, "FIN DU TEMPS !", 3)
            pyxel.text(30, 30, "Le joueur " + str(self.nbGagnant) + " gagne !", 3)
        else:
            pyxel.text(50, 20, "FIN DU TEMPS !", 3)
            pyxel.text(70, 30, "Egalite !", 3)

    def draw(self):
        pyxel.cls(0)
        if not self.FIN:
            self.carte.draw()
            self.joueur1.draw()
            self.joueur2.draw()
            # Partie textuelle du HUD ci-dessous
            pyxel.text(2, 112, "Joueur 1:", 8)
            pyxel.text(16, 120, str(int(self.prc[1])) + '%', 8)
            pyxel.text(92, 112, "Joueur 2:", 10)
            pyxel.text(106, 120, str(int(self.prc[2])) + '%', 10)
            # Rendu du timer
            pyxel.text(54, 110, "Temps:", 6)
            pyxel.text(60, 118, str(self.temps), 6)
        else:
            self.draw_fin()

    def calc_temps(self):
        if pyxel.frame_count % 30 == 0:
            self.temps -= 1


class Carte:
    def __init__(self):
        self.tab = [[0 for x in range(128)] for y in range(128)]
        self.radius = 2
        # Couleur de la trainee des joueurs
        self.couleur_j1 = 2
        self.couleur_j2 = 9

    def normalize(self, val):
        if val >= 128:
            return 128
        elif val < 0:
            return 0
        else:
            return val

    def peindre(self, x, y, nbJoueur):
        self.tab[x - 2][y] = nbJoueur
        self.tab[x - 2][y - 1] = nbJoueur
        self.tab[x - 2][y + 1] = nbJoueur
        self.tab[x - 1][y + 2] = nbJoueur
        self.tab[x - 1][y - 2] = nbJoueur
        self.tab[x - 1][y] = nbJoueur
        self.tab[x - 1][y - 1] = nbJoueur
        self.tab[x - 1][y + 1] = nbJoueur
        self.tab[x][y + 2] = nbJoueur
        self.tab[x][y + 1] = nbJoueur
        self.tab[x][y - 1] = nbJoueur
        self.tab[x][y - 2] = nbJoueur
        self.tab[x + 1][y + 2] = nbJoueur
        self.tab[x + 1][y - 2] = nbJoueur
        self.tab[x + 1][y] = nbJoueur
        self.tab[x + 1][y + 1] = nbJoueur
        self.tab[x + 1][y - 1] = nbJoueur
        self.tab[x + 2][y] = nbJoueur
        self.tab[x + 2][y + 1] = nbJoueur
        self.tab[x + 1][y - 1] = nbJoueur
        self.tab[x][y] = nbJoueur

    def calc_prc(self):
        e, r, j = 0, 0, 0
        for x in range(128):
            for y in range(128):
                if self.tab[x][y] == 0:
                    e += 1
                if self.tab[x][y] == 1:
                    r += 1
                if self.tab[x][y] == 2:
                    j += 1
        e, r, j = e * 100 / 16324, r * 100 / 16324, j * 100 / 16324
        return e, r, j

    def draw(self):
        # Rendu de la carte
        pyxel.bltm(0, 0, 0, 0, 0, 16 * 8, 16 * 8)
        # Rendu de la peinture
        for x in range(len(self.tab)):
            for y in range(len(self.tab[x])):
                val = self.tab[x][y]
                if val == 1:
                    pyxel.pset(x, y, self.couleur_j1)
                elif val == 2:
                    pyxel.pset(x, y, self.couleur_j2)


class Joueur:
    def __init__(self, joueurNb, carte):
        self.nb = joueurNb
        # Loc par default j1
        self.x = 4
        self.y = 52
        # Loc par default j2
        if self.nb == 2:
            self.x = 116
            self.y = 44
        # Couleur du sprite
        self.couleur_j1 = 8
        self.couleur_j2 = 10
        self.size = 8
        self.carte = carte
        # Sprite par default sont ceux du j1
        self.sprite_UP = (8, 8)
        self.sprite_DOWN = (16, 8)
        self.sprite_RIGHT = (16, 0)
        self.sprite_LEFT = (8, 0)
        # Modification des sprites si j2
        if self.nb == 2:
            self.sprite_UP = (24, 8)
            self.sprite_DOWN = (32, 8)
            self.sprite_RIGHT = (32, 0)
            self.sprite_LEFT = (24, 0)
        # Set le sprite par default au demarrage
        self.sprite_actuel = self.sprite_UP

    def collision(self, x, y):
        self.color_collisionUP = [pyxel.pget(x, y - 1), pyxel.pget(x + 5, y - 1), pyxel.pget(x + 8, y - 1)]
        self.color_collisionDOWN = [pyxel.pget(x, y + 9), pyxel.pget(x + 5, y + 9), pyxel.pget(x + 8, y + 9)]
        self.color_collisionLEFT = [pyxel.pget(x - 1, y), pyxel.pget(x - 1, y + 5), pyxel.pget(x - 1, y + 8)]
        self.color_collisionRIGHT = [pyxel.pget(x + 9, y), pyxel.pget(x + 9, y + 5), pyxel.pget(x + 9, y + 8)]
        self.contactUP = False
        self.contactDOWN = False
        self.contactRIGHT = False
        self.contactLEFT = False
        for y in range(len(self.color_collisionUP)):
            if self.color_collisionUP[y] == 3:
                self.contactUP = True
        for y in range(len(self.color_collisionDOWN)):
            if self.color_collisionDOWN[y] == 3:
                self.contactDOWN = True
        for y in range(len(self.color_collisionRIGHT)):
            if self.color_collisionRIGHT[y] == 3:
                self.contactRIGHT = True
        for y in range(len(self.color_collisionLEFT)):
            if self.color_collisionLEFT[y] == 3:
                self.contactLEFT = True

    def update(self):
        self.collision(self.x, self.y)
        self.check_inputs()
        self.paint()

    def check_inputs(self):
        if self.nb == 2:
            if pyxel.btn(pyxel.KEY_RIGHT) and (self.x + self.size) < 128 and not self.contactRIGHT:
                self.sprite_actuel = self.sprite_RIGHT
                self.x += 1
            if pyxel.btn(pyxel.KEY_LEFT) and (self.x - 1) >= 0 and not self.contactLEFT:
                self.sprite_actuel = self.sprite_LEFT
                self.x -= 1
            if pyxel.btn(pyxel.KEY_UP) and (self.y - 1) >= 0 and not self.contactUP:
                self.sprite_actuel = self.sprite_UP
                self.y -= 1
            if pyxel.btn(pyxel.KEY_DOWN) and (self.y + self.size) < 104 and not self.contactDOWN:
                self.sprite_actuel = self.sprite_DOWN
                self.y += 1
        elif self.nb == 1:
            if pyxel.btn(pyxel.KEY_D) and (self.x + self.size) < 128 and not self.contactRIGHT:
                self.sprite_actuel = self.sprite_RIGHT
                self.x += 1
            if pyxel.btn(pyxel.KEY_Q) and (self.x - 1) >= 0 and not self.contactLEFT:
                self.sprite_actuel = self.sprite_LEFT
                self.x -= 1
            if pyxel.btn(pyxel.KEY_Z) and (self.y - 1) >= 0 and not self.contactUP:
                self.sprite_actuel = self.sprite_UP
                self.y -= 1
            if pyxel.btn(pyxel.KEY_S) and (self.y + self.size) < 104 and not self.contactDOWN:
                self.sprite_actuel = self.sprite_DOWN
                self.y += 1

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.sprite_actuel[0], self.sprite_actuel[1], 8, 8, 0)

    def paint(self):
        self.carte.peindre(self.x + int(self.size / 2), self.y + int(self.size / 2), self.nb)


App()
