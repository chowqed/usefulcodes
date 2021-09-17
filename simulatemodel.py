from auxiliaryfns_mle import *
from scipy.stats import gumbel_r
from auxiliaryfns_val import *
from valuefunctions import *

# simulate the household's default decisions 
####################################################################################
datafile = 'penn_truncated.csv'
pennfile = 'penn_homevalue.csv'
csvdata = readcsv(datafile)

data = np.asarray(csvdata) # read data into array

mortgagepayment = calcPayment(data[:,2],data[:,4],data[:,3])*12 # calcualte total yearly mortagge payment 
income = mortgagepayment/(data[:,6]*fracMD/100) # calculate from dti
levelofPayment = mortgagepayment/income # fraction of mortgage payment as yearly income
roundedpayment = np.int_(myroundfraction(levelofPayment)) # round to level of payment
#for i in range(roundedpayment.shape[0]):
#   print levelofPayment[i], roundedpayment[i]
#print min(roundedpayment), max(roundedpayment)

penndata = np.asarray(readcsv(pennfile)).T # read home price data
avghomevalue = np.mean(penndata.reshape(-1, 3), axis=1) # average every 3 months, total months must be divisible by 3
startperiod = data[:,16]
totalperiod = data[:,17]
defaultperiod = data[:,18]
default = data[:,14]
counterhome = np.zeros(avghomevalue.shape[0]) # counter factual home values
for j in range(avghomevalue.shape[0]):
    if (j > 8):
        counterhome[j]=avghomevalue[8]
    else:
        counterhome[j]=avghomevalue[j]

#print avghomevalue

homeinsure_5 = np.zeros(avghomevalue.shape[0]) # set minimum home values level
for j in range(avghomevalue.shape[0]):
        homeinsure_5[j]=max(138000,avghomevalue[j])

#print homeinsure_5 







mledata = np.int_(np.stack((roundedpayment,default,startperiod,totalperiod,defaultperiod)).T)

print avghomevalue.T
########################################################################################
shapepar = 0.2344 
(emaxt,schoice,probtest,sig)=calcValues(shapepar)
nsim = 1000
nhouse = mledata.shape[0]
simdraws = np.random.gumbel(0,shapepar,[nhouse,30,nsim])
#simdefault = np.zeros(30)

ns = nsim +0.0 # make sure nsim is float

#print  probtest[1,15, 3, :,3]
#print sig[1,15, 3, :,3]
#print simdraws 
#r = gumbel_r.rvs(size=1000,0,0.4)


def simmodel(homeval): # loglikelihood function
    simdefault = np.zeros(30)
    for i in range(mledata.shape[0]):
        mlvl = int(mledata[i,0])
        sav = int() # initialize saving state
        squarter = int(mledata[i,2]) # starting quarter
        equarter = int(min(mledata[i,3],mledata[i,4])) #last quarter
        d = mledata[i,1]
        for t in range(equarter+1):
            cquarter = squarter + t
            hlvl = int(calcHomeValState(homeval, squarter,cquarter))
            #hlvl = int(calcHomeValState(avghomevalue, squarter,cquarter))
            #print type(hlvl)
            sigstar = sig[1,t,mlvl,hlvl,sav]
            #print  sigstar
            sd =  sum(simdraws[i][t]-sigstar > 0)/ns
            simdefault[cquarter] = simdefault[cquarter] + sd
            sav = sav + int(schoice[1,t,mlvl,hlvl,sav]) 

    return simdefault 

result1 = simmodel(avghomevalue)
result2 = simmodel(counterhome)
result3 = simmodel(homeinsure_5)

for j in range(result1.shape[0]):
    print result1[j],result2[j],result3[j]
