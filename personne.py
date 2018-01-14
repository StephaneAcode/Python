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
    """Cette classe possede un attribut de classe qui s'incremente a  chaque
    fois que l'on cree un objet de ce type"""

    
    objets_crees = 0 # Le compteur vaut 0 au depart
    def __init__(self):
        """a chaque fois qu'on cree un objet, on incremente le compteur"""
        Compteur.objets_crees += 1

    def combien(cls):
        """Methode de classe affichant combien d'objets ont ete crees"""
        print("Jusqu'a  present, {} objets ont ete crees.".format(cls.objets_crees))
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
        le message a  ecrire"""
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
        """Fonction chargÃ©e d'afficher quelque chose"""
        print("On affiche la mÃªme chose.")
        print("peu importe les donnÃ©es de l'objet ou de la classe.")
    afficher = staticmethod(afficher)



class Personne:
    """Classe définissant une personne caractérisée par :
    - son nom ;
    - son prénom ;
    - son âge ;
    - son lieu de résidence"""

    
    def __init__(self, nom, prenom):
        """Constructeur de notre classe"""
        self.nom = nom
        self.prenom = prenom
        self.age = 33
        self._lieu_residence = "Paris" # Notez le souligné _ devant le nom
    def _get_lieu_residence(self):
    """Méthode qui sera appelée quand on souhaitera accéder en lecture
        à l'attribut 'lieu_residence'"""
        
        
        print("On accède à l'attribut lieu_residence !")
        return self._lieu_residence
    def _set_lieu_residence(self, nouvelle_residence):
        """Méthode appelée quand on souhaite modifier le lieu de résidence"""
        print("Attention, il semble que {} déménage à {}.".format( \
                self.prenom, nouvelle_residence))
        self._lieu_residence = nouvelle_residence
    # On va dire à Python que notre attribut lieu_residence pointe vers une
    # propriété
    lieu_residence = property(_get_lieu_residence, _set_lieu_residence)
    


sys.exit()

print "Coucou\n"

jean = Personne()
david = Personne()
print jean.nom
print david.nom
jean.prenom
jean.age
jean.lieu_residence
# Jean demenage...
jean.lieu_residence = "Berlin"
jean.lieu_residence

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




Compteur.combien()
a = Compteur()
Compteur.combien()
b = Compteur()
Compteur.combien()

pan = Test()
pan.afficher()





#  ###    #
# #   #  ##
# #  ## # #
# # # #   #
# ##  #   #
# #   #   #
#  ###  #####

# ##### #####
