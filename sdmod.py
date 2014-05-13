'''
Functions related with SD modulators
 '''

import numpy as np
from numpy import (zeros, arange)

def gen_mash(order, N, K):
    ''' Generates a mash type $\Sigma-\Delta$ sequence 
    
    Parameters
    ----------
    order : int
        order of the $\Sigma-\Delta$ modulator.
    N : int
        Number of bits of the modulator.
    K : float
        Value being converted
        
    Returns
    -------
    div : 
    per : int
        Period of the sequence
    
    Commentaries
    ------------
    This implementation is not really effective from the computational 
    point of view but is representative of the architecture of the
    system. 
        '''
    # Modulator of order 1
    MAX = 2**N-1
    L = len(K)
    if order == 1:
        over1 = zeros(L, dtype=np.int)
        over1[0] = 1
        stat1 = zeros(L, dtype=np.int)
        for j in arange(1, L):
            stat1[j] = stat1[j-1]+K[j-1]
            if stat1[j] > MAX:
                over1[j] = 1
                stat1[j] = stat1[j] - (MAX+1)
        div = over1
        per = (stat1 == 0).astype(int)
        if len(per) > 1:
            per = per[1]-per[0]
        else:
            per = -1

    # Modulator of order 2
    elif order == 2:
        stat1 = zeros(L, dtype=np.int)
        stat2 = zeros(L, dtype=np.int)
        over1 = zeros(L, dtype=np.int)
        over2 = zeros(L, dtype=np.int)

        for j in arange(1, L):
            stat1[j] = stat1[j-1] + K[j-1]
            if stat1[j] > MAX:
                over1[j] = 1
                stat1[j] = stat1[j] - (MAX + 1)
            stat2[j] = stat2[j-1] + stat1[j]
            if stat2[j] > MAX:
                over2[j] = 1
                stat2[j] = stat2[j] - (MAX + 1)
        div = over1 + over2 - np.hstack(([0], over2[:-1]))
        stat = stat1 + stat2
        per = (stat == 0).astype(int)
        if len(per) > 1:
            per = per[1] - per[0]
        else:
            per = -1

    # Modulator of order 3
    elif order == 3:

        stat1 = zeros(L, dtype=np.int)
        stat2 = zeros(L, dtype=np.int)
        stat3 = zeros(L, dtype=np.int)

        over1 = zeros(L, dtype=np.int)
        over1[0] = 1
        over2 = zeros(L, dtype=np.int)
        over3 = zeros(L, dtype=np.int)

        for j in arange(1, L):
            stat1[j] = stat1[j-1] + K[j-1]
            if stat1[j] > MAX:
                over1[j] = 1
                stat1[j] = stat1[j] - (MAX + 1)

            stat2[j] = stat2[j-1] + stat1[j]
            if stat2[j] > MAX:
                over2[j] = 1
                stat2[j] = stat2[j] - (MAX + 1)

            stat3[j] = stat3[j-1] + stat2[j]
            if stat3[j] > MAX:
                over3[j] = 1
                stat3[j] = stat3[j] - (MAX + 1)
        div = over1
        div += over2 - np.hstack(([0], over2[:-1]))
        div += over3 - 2*np.hstack(([0], over3[:-1]))
        div += np.hstack(([0], [0], over3[:-2]))

        stat = stat1 + stat2 + stat3
        per = (stat == 0).astype(int)
        if len(per) > 1:
            per = per[1] - per[0]
        else:
            per = -1

    return div, per
  
def mash_theoretical():
    pass
if __name__ == "__main__":
    from numpy.testing import  assert_almost_equal
    import  numpy.random as rnd
    # Test order one assert the mean value
    floatnum = rnd.rand()*np.ones(10000)
    
    # order one
    sequence, per = gen_mash(1, 19, floatnum*2**19)
    assert_almost_equal(sequence.mean(), floatnum.mean(), 4)
    # order two
    sequence, per = gen_mash(2, 19, floatnum*2**19)
    assert_almost_equal(sequence.mean(), floatnum.mean(), 4)
    
    

