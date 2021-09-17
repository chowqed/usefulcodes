from auxiliaryfns_mle import *
from valuefunctions import *
from scipy.optimize import minimize


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

mledata = np.int_(np.stack((roundedpayment,default,startperiod,totalperiod,defaultperiod)).T)


def loglikeobj(theta): # loglikelihood function
    par1 = theta[0]
    par1 = theta[1]
    loglh = 0.0 # objective value
    (emaxt,schoice,pchoice,sig) = calcValues(par1, par2)
    for i in range(mledata.shape[0]):
        mlvl = int(mledata[i,0])
        sav = int() # initialize saving state
        squarter = int(mledata[i,2]) # starting quarter
        equarter = int(min(mledata[i,3],mledata[i,4])) #last quarter
        d = mledata[i,1]
        for t in range(equarter+1):
            cquarter = squarter + t
            hlvl = int(calcHomeValState(avghomevalue, squarter,cquarter))
            #print type(hlvl)
            if (t < equarter):
                loglh = loglh + np.log(pchoice[1,t,mlvl,hlvl,sav])
            else:
                loglh = loglh +(1.0-np.log(pchoice[1,t,mlvl,hlvl,sav]))*d + (1-d)*np.log(pchoice[1,t,mlvl,hlvl,sav])
            
            sav = sav + int(schoice[1,t,mlvl,hlvl,sav])

    print loglh, par1
    return -loglh # negative since need to maximize later          
 
#print loglikeobj([100,3.89])


#loglikeobj([0.2344])
#loglikeobj([0.27])

initpars = [0.26, 41]
spars = minimize(loglikeobj,initpars,method='Nelder-Mead')

print spars
 
