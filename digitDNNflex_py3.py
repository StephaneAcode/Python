#!/usr/local/bin/python3.7
# coding: utf-8

#https://iamtrask.github.io/2015/07/12/basic-python-network/

import numpy as np
np.set_printoptions(precision=2,suppress=1)

def nonlin(x,deriv=False):
    if deriv:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))

def processNet(input):
    lp = []
    Xp = np.array([list(map(ord, input))])  # Convert map object to list
    Xp = np.delete(Xp, [0,6,12,18,24,30,36,42], 1)
    Xp = (Xp - 32) / 3.0
    lp.append(Xp)
    for i in range(0, len(netConfig)-1):
        lp.append(nonlin(np.dot(lp[i], syn[i])))
    print(lp[-1])

input0 = """
 ### 
#   #
#  ##
# # #
##  #
#   #
 ### 
"""

input1 = """
  #  
 ##  
# #  
  #  
  #  
  #  
#####
"""

input1b = """
  #  
 ##  
# #  
  #  
  #  
  #  
  #  
"""

input2 = """
 ### 
#   #
    #
   # 
  #  
 #   
#####
"""

input2b = """
 ### 
#   #
    #
 ### 
#    
#    
#####
"""

input3 = """
 ### 
#   #
    #
  ## 
    #
#   #
 ### 
"""

input3b = """
#### 
    #
    #
 ####
    #
    #
#### 
"""

input4 = """
    #
   # 
  #  
 #   
#  # 
#####
   # 
"""

input5 = """
#####
#    
#    
#### 
    #
#   #
 ### 
"""

input6 = """
 ### 
#   #
#    
#### 
#   #
#   #
 ### 
"""

input6b = """
  #  
 #   
#    
#### 
#   #
#   #
 ### 
"""

input7 = """
#####
    #
   # 
  #  
 #   
 #   
 #   
"""

input8 = """
 ### 
#   #
#   #
 ### 
#   #
#   #
 ### 
"""

input9 = """
 ### 
#   #
#   #
 ####
    #
   # 
 ##  
"""

input9b = """
 ### 
#   #
#   #
 ####
    #
    #
 ### 
"""

# map(ord,inputx) => converts a string into an array of ascii values
# len(map(ord,input0)) => 43

#chatGPT suggere d'augmenter le nombre de donnes d'apprentissage => 2x1, 2x2, 2x6, 2x9 => ca marche mieux !
X = np.array([list(map(ord, input0)),
              list(map(ord, input1)),
              list(map(ord, input1b)),
              list(map(ord, input2)),
              list(map(ord, input2b)),
              list(map(ord, input3)),
              list(map(ord, input3b)),
              list(map(ord, input4)),
              list(map(ord, input5)),
              list(map(ord, input6)),
              list(map(ord, input6b)),
              list(map(ord, input7)),
              list(map(ord, input8)),
              list(map(ord, input9)),
              list(map(ord, input9b))])

X = np.delete(X, [0, 6, 12, 18, 24, 30, 36, 42], 1)

y = np.array([[1,0,0,0,0,0,0,0,0,0],
              [0,1,0,0,0,0,0,0,0,0],
              [0,1,0,0,0,0,0,0,0,0],
              [0,0,1,0,0,0,0,0,0,0],
              [0,0,1,0,0,0,0,0,0,0],
              [0,0,0,1,0,0,0,0,0,0],
              [0,0,0,1,0,0,0,0,0,0],
              [0,0,0,0,1,0,0,0,0,0],
              [0,0,0,0,0,1,0,0,0,0],
              [0,0,0,0,0,0,1,0,0,0],
              [0,0,0,0,0,0,1,0,0,0],
              [0,0,0,0,0,0,0,1,0,0],
              [0,0,0,0,0,0,0,0,1,0],
              [0,0,0,0,0,0,0,0,0,1],
              [0,0,0,0,0,0,0,0,0,1]])

learn_iter = 30000
nb_samples = 15
X = X[:nb_samples, :]
X = (X - 32) / 3.0
y = y[:nb_samples, :]

print("Learning set samples: %d" % (len(X[:, 1])))
print("Input length %d" % (len(X[1, :])))

netConfig = [len(X[1, :]), 400, 150, 50, 30, len(y[1, :])]

syn = []

np.random.seed(1)

for i in range(1, len(netConfig)):
    print("Layer %2d, %4d neurones." % (i, netConfig[i]))
    #syn.append(2 * np.random.random((netConfig[i - 1], netConfig[i])) - 1)
    #chatGPT suggere une initialisation de Xavier (ou Glorot) => ca marche
    syn.append(np.random.randn(netConfig[i - 1], netConfig[i]) * np.sqrt(2.0 / (netConfig[i - 1] + netConfig[i])))

print("Output length %d" % (len(y[1, :])))

for j in range(learn_iter):  # Use range instead of xrange in Python 3

    l = []
    l_error = []
    l_delta = []

    l.append(X)
    for i in range(0, len(netConfig) - 1):
        l.append(nonlin(np.dot(l[i], syn[i])))
        l_delta.append([])
        l_error.append([])

    l_error[len(netConfig) - 2] = y - l[len(netConfig) - 1]
    l_delta[len(netConfig) - 2] = l_error[len(netConfig) - 2] * nonlin(l[len(netConfig) - 1], deriv=True)
    for i in range(len(netConfig) - 2, 0, -1):
        l_error[i - 1] = l_delta[i].dot(syn[i].T)
        l_delta[i - 1] = l_error[i - 1] * nonlin(l[i], deriv=True)

    for i in range(len(netConfig) - 1, 0, -1):
        syn[i - 1] += l[i - 1].T.dot(l_delta[i - 1])

    if (j % (learn_iter // 10)) == 0:
        print("Iter %5d, Error: %6.4f" % (j, np.mean(np.abs(l_error[-1]))))

print(l[-1])

print("====")
input1 = """
  #  
 ##  
  #  
  #  
  #  
  #  
 ### 
"""

processNet(input1)
