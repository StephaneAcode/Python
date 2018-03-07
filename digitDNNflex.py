#!/usr/bin/env python
# coding: utf-8

#https://iamtrask.github.io/2015/07/12/basic-python-network/

import numpy as np
np.set_printoptions(precision=2,suppress=1)
#np.set_printoptions()

def nonlin(x,deriv=False):
	if(deriv==True):
	    return x*(1-x)

	return 1/(1+np.exp(-x))
    


def processNet(input):
    lp=[]
    Xp = np.array([map(ord,input)])
    Xp = np.delete(Xp, [0,6,12,18,24,30,36,42], 1)
    Xp = (Xp-32)/3.0
    lp.append(Xp)
    for i in range(0, len(netConfig)-1):
        lp.append(nonlin(np.dot(lp[i],syn[i])))
    print lp[-1]



#  ###     #     ###    ###       #  #####   ###   #####   ###    ### 
# #   #   ##    #   #  #   #     #   #      #   #      #  #   #  #   #
# #  ##  # #        #      #    #    #      #         #   #   #  #   #
# # # #    #       #     ##    #     ####   ####     #     ###    ####
# ##  #    #      #        #  #  #       #  #   #   #     #   #      #
# #   #    #     #     #   #  #####  #   #  #   #   #     #   #     # 
#  ###   #####  #####   ###      #    ###    ###    #      ###    ##  

# #####  #####


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

# map(ord,inputx) => converts a string into an array of ascii values
# len(map(ord,input0)) => 43

X = np.array([map(ord,input0),
              map(ord,input1),
              map(ord,input1b),
              map(ord,input2),
              map(ord,input2b),
              map(ord,input3),
              map(ord,input4),
              map(ord,input5),
              map(ord,input6),
              map(ord,input7),
              map(ord,input8),
              map(ord,input9)])

X = np.delete(X, [0,6,12,18,24,30,36,42], 1)
           
y = np.array([[1,0,0,0,0,0,0,0,0,0],
			  [0,1,0,0,0,0,0,0,0,0],
			  [0,1,0,0,0,0,0,0,0,0],
			  [0,0,1,0,0,0,0,0,0,0],
			  [0,0,1,0,0,0,0,0,0,0],
			  [0,0,0,1,0,0,0,0,0,0],
			  [0,0,0,0,1,0,0,0,0,0],
			  [0,0,0,0,0,1,0,0,0,0],
			  [0,0,0,0,0,0,1,0,0,0],
			  [0,0,0,0,0,0,0,1,0,0],
			  [0,0,0,0,0,0,0,0,1,0],
			  [0,0,0,0,0,0,0,0,0,1]])

learn_iter = 25000
nb_samples = 11
X = X[:nb_samples,:]
X = (X-32)/3.0
#print X.reshape(-1,5)

y = y[:nb_samples,:]

print "Learning set samples: %d" % ( len(X[:,1]) )
print "Input length %d" % ( len(X[1,:]) )


#netConfig = [ len(X[1,:]), 250, 100, 50, 30, len(y[1,:]) ]
#For 11 samples, 2x1, 2x2
#netConfig = [ len(X[1,:]), 400, 110, 50, 30, len(y[1,:]) ]
netConfig = [ len(X[1,:]), 400, 110, 50, 30, len(y[1,:]) ]

syn=[]

np.random.seed(1)

for i in range(1, len(netConfig)):
    print "Layer %2d, %4d neurones." % ( i, netConfig[i] )
    syn.append(2*np.random.random((netConfig[i-1],netConfig[i])) - 1)

print "Output length %d" % ( len(y[1,:]) )


for j in xrange(learn_iter):


    l=[]
    l_error=[]
    l_delta=[]
	
    l.append(X)
    for i in range(0, len(netConfig)-1):
        l.append(nonlin(np.dot(l[i],syn[i])))
        l_delta.append([])
        l_error.append([])


    l_error[len(netConfig)-2] = y - l[len(netConfig)-1]
    l_delta[len(netConfig)-2] = l_error[len(netConfig)-2]*nonlin(l[len(netConfig)-1],deriv=True)
    for i in range(len(netConfig)-2, 0, -1):
        l_error[i-1] = l_delta[i].dot(syn[i].T)
        l_delta[i-1] = l_error[i-1]*nonlin(l[i],deriv=True)

    for i in range(len(netConfig)-1, 0, -1):
        #if j == 0:
            #print "syn compute i: %2d" % ( i )
        syn[i-1] += l[i-1].T.dot(l_delta[i-1])


    if (j% (learn_iter/10) ) == 0:
        print "Iter %5d, Error: %6.4f" % ( j, np.mean(np.abs(l_error[-1])))


print l[-1]

input1 = """
  #  
 ##  
  #  
  #  
  #  
  #  
 ### 
"""

print "===="
processNet(input1)


