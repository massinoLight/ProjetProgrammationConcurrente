import random

from queue import *
from threading import Thread
import time
from Couleur import bcolors

Stock = Queue(10)  # notre pile, qui peut contenir 10 elements max( 0 pour enlever la limite)

#le nombre de producteurs et de consommateurs
count_producers=3
count_consumer=10

items = []
#liste des comsommateur et des producteurs
producer = []
consumer = []


"""
La Classe de nos producteurs
qui herite de la classe Thread 

"""


class Producteur(Thread):
    """
       Le constructeur de notre Classe 
       """""

    def __init__(self,numero):
        self.pret = True
        self.numero=numero
        Thread.__init__(self)

    def initialisation_du_stock(self):
        while not Stock.full():
            try:
                Stock.put("ajout", True, 1000)
            except Full as e :
                print("probléme lors du remplissage du stock")

    """ 
       Fonction qui va simuler une attente 
       """

    def wait(self, attente):
        time.sleep(attente)

    def run(self):
            ressources = random.randint(1, 10)
            i = 0
            """
                       Tant que notre file n'est pas remplie et que notre producteur a des ressources a ajouter 
                       on continue la production de ressources
                       (la file contient 10 elements au maximum)
                       un consommateur peut demander ne ressource entre temps
                       """
            while i<ressources and not Stock.full():
                try:
                    print(bcolors.WARNING + "Le producteur "+ str(self.numero)+
                          " propose une PS5...\n" + bcolors.ENDC)
                    Stock.put("ajout", True, 1000)
                    self.wait(2)

                except Full as e :
                    print("Le stock est plein!\n");





"""
La Classe de nos consommateurs
qui herite de la classe Thread 

"""


class Consommateur(Thread):
    """
    Le constructeur de notre Classe 
     """""

    def __init__(self, oui, numero):
        self.conso = oui
        self.numero = numero
        Thread.__init__(self)

    """
    Fonction qui va simuler une attente 
    """

    def wait(self, attente):
        time.sleep(attente)

    """
    La tache  que va exécuter le Thread une fois lancé
    """

    def run(self):
        while self.conso:
            time.sleep(1)

            ok = False
            ressources = random.randint(1, 6)

            i = 1
            print("vite vite Le mouton " + str(self.numero) + " demande " + str(ressources) + " PS5\n")

            """tant que le consomateur veut consommer une ressource 
            et tnt que celle-ci est disponible en sock"""
            if ressources <= Stock.qsize():
              while i <= ressources and not Stock.empty():
                try:
                    Stock.get(True, 500)
                    ok = True
                    print(bcolors.OKCYAN + "je suis le mouton " + str(
                        self.numero) + ": j\'achéte une PS5 plus que \n" +str(ressources-i)+
                          " et ça sera bon pour moi "+ bcolors.ENDC)
                    self.wait(2)

                    i +=1

                except Empty as e:
                    ok = False
                    break

            else:
                producteur = Producteur(self.numero)
                producteur.start()
            if ok:
                print(bcolors.OKCYAN + "je suis le mouton " + str(
                    self.numero) + ": et j\'ai fini mes achat\n" + bcolors.ENDC)
                print("Il reste  " + str(Stock.qsize()) + " PS5 dans notre stock\n")
            else:
                print(bcolors.OKCYAN + "je suis le mouton " + str(self.numero) +
                      ": Il n'y a pas assez de PS5 pour moi j\'attends \n")
                self.wait(2)
            self.conso = False


if __name__ == '__main__':
    print(bcolors.FAIL +"###################### Début du black friday  #####################################"+ bcolors.ENDC)
    print(bcolors.FAIL +"Attention ça ne dure pas longtemps 2 minutes seulement "+ bcolors.ENDC)
    time.sleep(2)
    p1 = Producteur(0)
    # on demarre avec un stock plein
    p1.initialisation_du_stock()
    print("il y a initialement  " + str(Stock.qsize()) + " PS5 dans notre stock\n")





    i = 1
    for i in range(1,count_consumer):
        consommateur = Consommateur(oui=True, numero=i)
        consumer.append(consommateur)

    for c in consumer:
        c.start()

    time.sleep(120)

    print(bcolors.FAIL +"##### Fin du black friday #####"+ bcolors.ENDC)
    print("Il nous reste  au final " + str(Stock.qsize()) + " PS5 dans notre stock\n")
    if Stock.qsize()==0:
      print("Nous avons tout vendu  hahahaha")
    else:
        print("ce n\'est pas grave elles se vondront de tot ou tard")