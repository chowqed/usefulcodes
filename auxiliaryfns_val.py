# auiliary functions that help with the estimations

from parameters import *


def lvlmortgage(l): # return balance paid to the mortagge as a fraction of yearly income
    return (l+1.0)*0.05/4.0  # divide by 4 for each quarter

def returnHomeVal(h): # return % of initial home value
    return 0.9+h/100.0 # 

def terminalWealth(o,l, h, s, k=1): # l level of mortgage payment, h homeval state, s saving state
    return (o*0.5*returnHomeVal(h)*lvlmortgage(l)*5*k+s*0.05)*bequest

def calcUtil(c,h=1.0): # utility function
    u = (c**(1.0-gamma))/(1.0-gamma) + (h**(1.0-gamma))/(1.0-gamma)
    #u = c**(1.0-gamma)/(1.0-gamma)
   # u = c +phi*h
    #u = c
    return u

def calcEV1Prob(c1,c0,ev1,ev0,rho): # calculate probability of paying mortgage
    prob = np.exp((1.0/rho)*(c1-c0+beta*(ev1-ev0)))/(1.0+np.exp((1.0/rho)*(c1-c0+beta*(ev1-ev0))))
    #print c1,c0,beta,ev1,ev0,(1.0/rho)*(c1-c0+beta*(ev1-ev0)),np.exp((1.0/rho)*(c1-c0+beta*(ev1-ev0))), prob
    if (prob < 0.00001):
        prob = 0.00001
    return prob

def calcEmax(c1,c0,ev1,ev0,rho):
    prob1 = calcEV1Prob(c1,c0,ev1,ev0,rho)
    #emax = rho*(euler+(c1-c0+beta*ev1)/rho-np.log(prob1))
    emax = rho*(euler+(c1+beta*ev1)/rho-np.log(prob1))
    return emax

def calcSigstar(c1,c0,ev1,ev0):
    sigstar = c1-c0+beta*(ev1-ev0)
    return sigstar

#print calcEV1Prob(1.2,0.9,12.78,13.01,1.2)
#print calcEmax(1.2,0.9,12.78,13.01,1.2)
#print np.exp(-5)
#print lvlmortgage(5)
#print calcUtil(0,1)
#print lvlmortgage(5)
