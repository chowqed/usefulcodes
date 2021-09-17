from parameters import *
import csv


def myroundfraction(x, base=.05, prec=2): # get a fraction and round to 0.05
    #return round(base * round(float(x)/base),prec)
    return np.round(x/base)


def calcPayment(upb, terms, i): # upb - balance, terms, i - interest rate
    r = i/100.0 # put interest in decimals
    monthly_payment = (upb*r/12)/(1-(1+r/12)**(-terms))
    return monthly_payment

def calcRemainBalance(upb, terms, i, m): # calculate balance after m months of payment
    d = calcPayment(upb, terms,i) # monthly payment
    r=i/100.0
    re_balance = d*(1-(1+r/12)**(-(terms-m)))/(r/12)
    return re_balance

def totalPaymentPaid(upb,terms,i,m): # calculate total payment paid after m months
    return upb - calcRemainBalance(upb,terms,i,m)

def fractionPaidtoBalance(upb,terms,i,m): # calculate fraction of mortgage payment towards upb
    d = calcPayment(upb, terms,i)
    total_p = totalPaymentPaid(upb,terms,i,m)
    return total_p/(d*m)


def readcsv(filename):	
    ifile = open(filename, "r")
    reader = csv.reader(ifile, delimiter=",",quoting=csv.QUOTE_NONNUMERIC)
    rownum = 0	
    a = []
    for row in reader:
        a.append (row)
        rownum += 1
    ifile.close()
    return a
def calcHomeValState(homevalue,startperiod,currentperiod): # calculate the state of home values given starting period
    state =   np.int_(myroundfraction(homevalue[currentperiod]/homevalue[startperiod],0.01,2))-basehomevalue
    return state




#print calcPayment(200000,360,4)
print calcRemainBalance(200000,240,2,60)
print calcRemainBalance(200000,240,4,60)

#print fractionPaidtoBalance(562300,240,5.4,60)
#print returnHomeVal(0)
#print lvlmortgage(2)

