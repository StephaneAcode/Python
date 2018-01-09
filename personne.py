#!/usr/bin/env python
# coding: utf-8

import sys

#Pour interactif:
#python -i personne.py

class Personne: # Definition de notre classe Personne
    """Classe definissant une personne caracterisee par :
    - son nom
    - son prenom
    - son age
    - son lieu de residence"""

    
    def __init__(self, nom, prenom): # Notre methode constructeur
        self.nom = nom
        self.prenom = prenom
        self.age = "24"
        self.lieu_de_residence = "Paris"


class Compteur:
    """Cette classe possede un attribut de classe qui s'incremente a† chaque
    fois que l'on cree un objet de ce type"""

    
    objets_crees = 0 # Le compteur vaut 0 au depart
    def __init__(self):
        """a chaque fois qu'on cree un objet, on incremente le compteur"""
        Compteur.objets_crees += 1

    def combien(cls):
        """Methode de classe affichant combien d'objets ont ete crees"""
        print("Jusqu'a† present, {} objets ont ete crees.".format(cls.objets_crees))
    combien = classmethod(combien)


class TableauNoir:
    """Classe definissant une surface sur laquelle on peut ecrire,
    que l'on peut lire et effacer, par jeu de methodes. L'attribut modifie
    est 'surface'"""
    
    def __init__(self):
        """Par defaut, notre surface est vide"""
        self.surface = ""
        

    def ecrire(self, message_a_ecrire):
        """Methode permettant d'ecrire sur la surface du tableau.
        Si la surface n'est pas vide, on saute une ligne avant de rajouter
        le message a† ecrire"""
        if self.surface != "":
            self.surface += "\n"
        self.surface += message_a_ecrire
        
    def lire(self):
        print(self.surface)
    
    def effacer(self):
        self.surface = ""
        print "Ereased one object of %s" % self.__class__.__name__
    

class Test:
    """Une classe de test tout simplement"""
    def afficher():
        """Fonction charg√©e d'afficher quelque chose"""
        print("On affiche la m√™me chose.")
        print("peu importe les donn√©es de l'objet ou de la classe.")
    afficher = staticmethod(afficher)


sys.exit()

print "Coucou\n"

a = Compteur()
b = Compteur()
c = Compteur()
Compteur.objets_crees
b.objets_crees
Compteur.combien()


tab = TableauNoir()
tab.ecrire("Cool! ce sont")
tab.surface
tab.ecrire("les vacances")
tab.lire()
tab.effacer()
tab.lire()










#  ###    #
# #   #  ##
# #  ## # #
# # # #   #
# ##  #   #
# #   #   #
#  ###  #####

# ##### #####
