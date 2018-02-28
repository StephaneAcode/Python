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

input2 = """
 ### 
#   #
    #
   # 
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
              map(ord,input2),
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
			  [0,0,1,0,0,0,0,0,0,0],
			  [0,0,0,1,0,0,0,0,0,0],
			  [0,0,0,0,1,0,0,0,0,0],
			  [0,0,0,0,0,1,0,0,0,0],
			  [0,0,0,0,0,0,1,0,0,0],
			  [0,0,0,0,0,0,0,1,0,0],
			  [0,0,0,0,0,0,0,0,1,0],
			  [0,0,0,0,0,0,0,0,0,1]])

nb_samples = 10
learn_iter = 15000
X = X[:nb_samples,:]
X = (X-32)/3.0
#print X.reshape(-1,5)

y = y[:nb_samples,:]

print "Input length %d" % ( len(X[1,:]) )


netConfig = [ len(X[1,:]), 250, 100, 50, 30, len(y[1,:]) ]

syn=[]

np.random.seed(1)

for i in range(1, len(netConfig)):
    print "Layer %2d, %4d neurones." % ( i, netConfig[i] )
    syn.append(2*np.random.random((netConfig[i-1],netConfig[i])) - 1)

print "Output length %d" % ( len(y[1,:]) )

np.random.seed(1)

# randomly initialize our weights with mean 0
syn0 = 2*np.random.random((len(X[1,:]),100)) - 1
syn5 = 2*np.random.random((100,50)) - 1
syn1 = 2*np.random.random((50,50)) - 1
syn2 = 2*np.random.random((50,50)) - 1
syn3 = 2*np.random.random((50,10)) - 1

for j in xrange(learn_iter):


    # Feed forward through layers 0, 1, and 2
    l0 = X
    l5 = nonlin(np.dot(l0,syn0))
    l1 = nonlin(np.dot(l5,syn5))
    l2 = nonlin(np.dot(l1,syn1))
    l3 = nonlin(np.dot(l2,syn2))
    l4 = nonlin(np.dot(l3,syn3))


    # how much did we miss the target value?
    l4_error = y - l4

    # in what direction is the target value?
    # were we really sure? if so, don't change too much.
    l4_delta = l4_error*nonlin(l4,deriv=True)

    # how much did each l1 value contribute to the l2 error (according to the weights)?
    l3_error = l4_delta.dot(syn3.T)
    
    # in what direction is the target l1?
    # were we really sure? if so, don't change too much.
    l3_delta = l3_error * nonlin(l3,deriv=True)

    l2_error = l3_delta.dot(syn2.T)
    l2_delta = l2_error * nonlin(l2,deriv=True)

    l1_error = l2_delta.dot(syn1.T)
    l1_delta = l1_error * nonlin(l1,deriv=True)

    l5_error = l1_delta.dot(syn5.T)
    l5_delta = l5_error * nonlin(l5,deriv=True)

    
    syn3 += l3.T.dot(l4_delta)
    syn2 += l2.T.dot(l3_delta)
    syn1 += l1.T.dot(l2_delta)
    syn5 += l5.T.dot(l1_delta)
    syn0 += l0.T.dot(l5_delta)



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
        print "Iter %5d, Error: %6.4f , %6.4f" % ( j, np.mean(np.abs(l4_error)), np.mean(np.abs(l_error[-1])))



print l4
print l[-1]
