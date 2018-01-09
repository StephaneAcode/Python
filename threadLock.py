#!/usr/bin/env python
# coding: utf-8

import random
import sys
import time

def myProc():
    # Repete 20 fois
    i = 0
    while i < 20:
        sys.stdout.write("1")
        sys.stdout.flush()
        attente = 0.2
        attente += random.randint(1, 60) / 100
        # attente est a present entre 0.2 et 0.8
        time.sleep(attente)
        i += 1

import random
import sys
from threading import Thread
import time

class Afficheur(Thread):

    """Thread charg� simplement d'afficher une lettre dans la console."""

    def __init__(self, lettre):
        Thread.__init__(self)
        self.lettre = lettre

    def run(self):
        """Code a� executer pendant l'execution du thread."""
        i = 0
        while i < 20:
            sys.stdout.write(self.lettre)
            sys.stdout.flush()
            attente = 0.2
            attente += random.randint(1, 60) / 100
            time.sleep(attente)
            i += 1

class AfficheurNew(Afficheur):
    def __init__(self, lettre):
        Afficheur.__init__(self, lettre)

    def run(self):
        """Code a� executer pendant l'execution du thread."""
        i = 0
        while i < 20:
            sys.stdout.write(self.lettre)
            sys.stdout.flush()
            attente = 0.4
            attente += random.randint(1, 60) / 100
            time.sleep(attente)
            i += 1



## Création des threads
#thread_1 = Afficheur("1")
#thread_2 = Afficheur("2")
#
## Lancement des threads
#thread_1.start()
#thread_2.start()
#
## Attend que les threads se terminent
#thread_1.join()
#thread_2.join()
#
#
#thread_3 = AfficheurNew("3")
#thread_4 = Afficheur("4")
#
#thread_3.start()
#thread_4.start()
#
#thread_3.join()
#thread_4.join()


import random
import sys
from threading import Thread
import time

class Afficheur(Thread):

    """Thread chargé simplement d'afficher un mot dans la console."""

    def __init__(self, mot):
        Thread.__init__(self)
        self.mot = mot

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        i = 0
        while i < 5:
            for lettre in self.mot:
                sys.stdout.write(lettre)
                sys.stdout.flush()
                attente = 0.2
                attente += random.randint(1, 60) / 100
                time.sleep(attente)
            i += 1

## Création des threads
#thread_1 = Afficheur("canard")
#thread_2 = Afficheur("TORTUE")
#
## Lancement des threads
#thread_1.start()
#thread_2.start()
#
## Attend que les threads se terminent
#thread_1.join()
#thread_2.join()



import random
import sys
from threading import Thread, RLock
import time

verrou = RLock()

class Afficheur(Thread):

    """Thread chargé simplement d'afficher un mot dans la console."""

    def __init__(self, mot):
        Thread.__init__(self)
        self.mot = mot

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        i = 0
        while i < 5:
            with verrou:
                for lettre in self.mot:
                    sys.stdout.write(lettre)
                    sys.stdout.flush()
                    attente = 0.2
                    attente += random.randint(1, 60) / 100
                    time.sleep(attente)
            i += 1

# Création des threads
thread_1 = Afficheur("canard")
thread_2 = Afficheur("TORTUE")

# Lancement des threads
thread_1.start()
thread_2.start()

# Attend que les threads se terminent
thread_1.join()
thread_2.join()

