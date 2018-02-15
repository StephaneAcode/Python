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

X = np.array([[2,2,35,1],
              [2,35,35,3],
              [35,2,35,1],
              [35,35,35,3]])

X = np.array([[10, 32, 35, 35, 35, 32, 10, 35, 32, 32, 32, 35, 10, 35, 32, 32, 35, 35, 10, 35, 32, 35, 32, 35, 10, 35, 35, 32, 32, 35, 10, 35, 32, 32, 32, 35, 10, 32, 35, 35, 35, 32, 10],
              [10, 32, 32, 35, 32, 32, 10, 32, 35, 35, 32, 32, 10, 35, 32, 35, 32, 32, 10, 32, 32, 35, 32, 32, 10, 32, 32, 35, 32, 32, 10, 32, 32, 35, 32, 32, 10, 35, 35, 35, 35, 35, 10]])

X = np.array([[10, 32, 35, 35, 35, 32, 10, 35, 32, 32, 32, 35, 10, 35, 32, 32, 35, 35, 10, 35, 32, 35, 32, 35, 10, 35, 35, 32, 32, 35, 10, 35, 32, 32, 32, 35, 10],
              [10, 32, 32, 35, 32, 32, 10, 32, 35, 35, 32, 32, 10, 35, 32, 35, 32, 32, 10, 32, 32, 35, 32, 32, 10, 32, 32, 35, 32, 32, 10, 32, 32, 35, 32, 32, 10]])
X = X/10.0
               
y = np.array([[1,0,0,0,0,0,0,0,0,0],
			  [0,1,0,0,0,0,0,0,0,0]])


print "Length %d" % ( len(X[1,:]) )

np.random.seed(1)

# randomly initialize our weights with mean 0
syn0 = 2*np.random.random((len(X[1,:]),200)) - 1
syn1 = 2*np.random.random((200,100)) - 1
syn2 = 2*np.random.random((100,10)) - 1

for j in xrange(30000):

	# Feed forward through layers 0, 1, and 2
    l0 = X
    l1 = nonlin(np.dot(l0,syn0))
    l2 = nonlin(np.dot(l1,syn1))
    l3 = nonlin(np.dot(l2,syn2))

    # how much did we miss the target value?
    l3_error = y - l3
    
    if (j% 10000) == 0:
        print "Error:" + str(np.mean(np.abs(l3_error)))

    # in what direction is the target value?
    # were we really sure? if so, don't change too much.
    l3_delta = l3_error*nonlin(l3,deriv=True)

    # how much did each l1 value contribute to the l2 error (according to the weights)?
    l2_error = l3_delta.dot(syn2.T)
    
    # in what direction is the target l1?
    # were we really sure? if so, don't change too much.
    l2_delta = l2_error * nonlin(l2,deriv=True)

    l1_error = l2_delta.dot(syn1.T)
    l1_delta = l1_error * nonlin(l1,deriv=True)

    syn2 += l2.T.dot(l3_delta)
    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)

print l3
