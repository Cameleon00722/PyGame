import random


class Perso:
    def __init__(self, nom, classe):
        self.nom = nom
        self.classe = classe
        self.niveau = 1
        self.courbe_Prog = 1
        self.capacite = []  # TODO crée capacité
        self.sac = ["pomme", "peche", "poire"]
        self.money = 10

        if self.classe == "mage":  # TODO vie et dgt évolutif
            self.vie = 10
            self.dmg = 3
            self.capacite.append("blitz")
        elif self.classe == "guerrier":
            self.vie = 20
            self.dmg = 3
            self.capacite.append("frappe")
        elif self.classe == "archer":
            self.vie = 15
            self.dmg = 2
            self.capacite.append("tir")
            self.capacite.append("tir enflamé")
        elif self.classe == "berserker":
            self.vie = 30
            self.dmg = 2
            self.capacite.append("booum")


def combat(self, monstre):
    print(self.nom, " nv ", self.niveau, " et ", monstre.type, " nv ", monstre.niveau, "entre en combat")

    while self.vie > 0 and monstre.vie > 0:
        print("choisis ton attaque : ")
        for i in range(len(self.capacite)):
            print(i, self.capacite[i])

        choix = int(input("choisis le numero de l'attaque : "))  # TODO gestion erreur
        print("le joueur attaque avec ", self.capacite[choix])

        print(self.nom, " vie : ", self.vie, " et ", monstre.type, " vie : ", monstre.vie - self.dmg)
        monstre.vie = monstre.vie - self.dmg

        if monstre.vie > 0:
            print("le monstre attaque")
            print(self.nom, " vie : ", self.vie - monstre.dmg, " et ", monstre.type, " vie : ", monstre.vie)
            self.vie = self.vie - monstre.dmg
            if self.vie <= 0:
                print("tu es mort, te voilà de retour au village")
                loss = random.randrange(0, self.money)
                self.money = self.money - loss
                break

        else:
            win = random.randrange(0, monstre.niveau + 10)
            xpe = random.randrange(1, monstre.niveau + 50)
            print("le monstre est mort, le joueur remporte ", win, " pièce !")

            print("le monstre est mort, le joueur remporte ", xpe,
                  " xp !")  # todo ajouter drop de monstre selon son type

            self.money = self.money + win

            if self.courbe_Prog + xpe > 10 + self.niveau * 10:
                diff = self.courbe_Prog + xpe - 10 + self.niveau * 10
                print("tu gagne un niveau, niv : ", self.niveau)
                self.niveau = self.niveau + 1
                self.courbe_Prog = self.courbe_Prog + diff
            else:
                self.courbe_Prog = self.courbe_Prog + xpe


class monstre:
    def __init__(self, type, nv):
        self.type = type
        self.niveau = nv
        self.capacity = []

        if self.type == "blob":
            self.dmg = 1 + 0.5 * nv
            self.vie = 5 + 0.5 * nv
        elif self.type == "troll":
            self.dmg = 1 + 0.5 * nv
            self.vie = 5 + 0.5 * nv
        elif self.type == "lutin":
            self.dmg = 1 + 0.5 * nv
            self.vie = 5 + 0.5 * nv
        elif self.type == "gnome":
            self.dmg = 1 + 0.5 * nv
            self.vie = 5 + 0.5 * nv
        elif self.type == "orc":
            self.dmg = 1 + 0.5 * nv
            self.vie = 5 + 0.5 * nv


def gen_monstre():
    num = random.randrange(1, 5)
    num_nv = random.randrange(1, joueur.niveau + 2)
    if num == 1:
        return monstre("blob", num_nv)
        # print(mr.type,"nv ", mr.niveau,"dmg ", mr.dmg,"vie ", mr.vie)
    elif num == 2:
        return monstre("troll", num_nv)
        # print(mr.type,"nv ", mr.niveau,"dmg ", mr.dmg,"vie ", mr.vie)
    elif num == 3:
        return monstre("lutin", num_nv)
        # print(mr.type,"nv ", mr.niveau,"dmg ", mr.dmg,"vie ", mr.vie)
    elif num == 4:
        return monstre("gnome", num_nv)
        # print(mr.type,"nv ", mr.niveau,"dmg ", mr.dmg,"vie ", mr.vie)
    elif num == 5:
        return monstre("orc", num_nv)
        # print(mr.type,"nv ", mr.niveau,"dmg ", mr.dmg,"vie ", mr.vie)


def balade(joueur):
    print("0 - marcher")
    print("1 - aller au village")
    print("2 - ouvrir le sac")
    choix = int(input("choisis ce que tu veux : "))
    while 0 >= choix < 3:
        choix = int(input("choisis ce que tu veux : "))

    if choix == 0:
        rencontre = random.randrange(0, 100)
        if rencontre < 51:
            combat(joueur, gen_monstre())
        else:
            print("vous sortez du chemin sans encombre")

    elif choix == 1:
        print("vous aller au village ... ")  # TODO créer forge, magasin , etc

    elif choix == 2:
        print("vous ouvrez votre sac ")  # todo ajouter bouton pour consomer / retour
        for i in range(len(joueur.sac)):
            print(i, "| ", joueur.sac[i])


print(" bienvennue dans Eler Quest ")
nom = input("choisi ton nom : ")
classe = input(" choisi ta classe (mage, guerrier, archer, berserker): ")  # TODO gestion erreur saisi

joueur = Perso(nom, classe)
balade(joueur)
