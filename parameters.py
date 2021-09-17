# Global parameters
import numpy as np

##### Global Constant ########
euler = 0.5772156649 # euler's constant
beta = 0.95 # discount factor
bequest = 20 # bequest motive, terminal 
gamma = 0.0 # risk aversion
#kappa = 2 # relative importance of house wealth to cash
phi = 0.31 # relative weight of housing



##### Value Function Constant ########
ownHome = 2 # home owner states 1=home owner, 0=renter
T = 22# 20 quarters, last quarter just terminal wealth
lvlMortgage = 10 # 10 levels of mortgage payment 5, 10, .., 30% of income
HomeVal = 20 # 20 states for home values, in 20% multiples of yearly income
#PriceToRent = 5 # 5 states for price-to-rent ratio
Saving = 20 # 20 states for savings


##### MLE Constant ########
fracMD = 0.7 # fraction of mortgage as total debt
basehomevalue = 90 # lowest level of homevalue


