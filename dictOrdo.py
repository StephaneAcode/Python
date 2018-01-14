#!/usr/bin/env python
# coding: utf-8




class DictionnaireOrdonne():
    
    
    def __init__(self):
        self._dicKeys = []
        self._dicValues = []
        print "Constructeur"
        


    #Pour gerer:
    #objet[index];
    #objet[index] = valeur;
    #del objet[index];
    
    def __getitem__(self, reqKey):
        
        if reqKey in self._dicKeys:
            dicIndex = self._dicKeys.index(reqKey)
            print "Getting Key %s ( %s ) at index %s" % (reqKey, self._dicValues[dicIndex], dicIndex)
            return self._dicValues[dicIndex]

    def __setitem__(self, reqKey, reqValue):
        
        if reqKey in self._dicKeys:
            dicIndex = self._dicKeys.index(reqKey)
            self._dicValues[dicIndex] = reqValue
            print "Setting Key %s = %s to index %s" % (reqKey, reqValue, dicIndex)
        else:
            print "Adding Key %s = %s to index %s" % (reqKey, reqValue, len(self._dicKeys))
            self._dicKeys.append(reqKey)
            self._dicValues.append(reqValue)
            print self._dicKeys


    #def __delitem__():


print "Coucou"

myD = DictionnaireOrdonne()
myD["A"] = "a"
myD["B"] = "b"
myD["C"] = "c"

myD["C"]
myD["B"]
myD["A"]
