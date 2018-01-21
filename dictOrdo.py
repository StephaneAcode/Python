#!/usr/bin/env python
# coding: utf-8


class DictionnaireOrdonne():
    
    
    def __init__(self, **kwargs):
        self._dicKeys = []
        self._dicValues = []
        print "Constructeur"
        for key, value in kwargs.items():
            self._dicKeys.append(key)
            self._dicValues.append(value)
            print "Constructeur Adding Key %s = %s to index %s" % (key, value, len(self._dicKeys))
        

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

    def __delitem__(self, reqKey):
    
        if reqKey in self._dicKeys:
            dicIndex = self._dicKeys.index(reqKey)
            checkKey = self._dicKeys.pop(dicIndex)
            checkValue = self._dicValues.pop(dicIndex)
            print "Deleting Key %s = %s to index %s" % (checkKey, checkValue, dicIndex)
            print self._dicKeys
        else:
            print "Deleting Key %s impossible because it doesn't exist in this object" % (reqKey)
            print self._dicKeys
    
    def __len__(self):
        
        return len(self._dicKeys)
    
    def __iter__(self):
    
        for myKey in self._dicKeys:
            yield myKey
            
    def __str__(self):
        
        retString = "{"
        for i in range(0, len(self._dicKeys)-1):
             retString += "%s: %s, " % ( self._dicKeys[i], self._dicValues[i] )
        retString += "}"
        return retString



print "Coucou"

myD = DictionnaireOrdonne(D = "d", E = "e")
myD["A"] = "z"
myD["B"] = "b"
myD["C"] = "c"
myD["A"] = "a"

myD["C"]
myD["B"]
myD["A"]

del myD["D"]
print len(myD)

del myD["Z"]
del myD["E"]

print len(myD)
print "==="
for key in myD:
    print key

print "==="
print myD

