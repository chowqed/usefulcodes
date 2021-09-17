import numpy as np
from scipy.stats import gumbel_r


simdraws = np.random.gumbel(0,0.4,1000)

print sum(simdraws - 2.2454805 > 0)

