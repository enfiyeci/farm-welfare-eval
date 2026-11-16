import numpy as np
from math import comb
rng=np.random.default_rng(3)
def cdf(k,n,p): return sum(comb(n,i)*p**i*(1-p)**(n-i) for i in range(0,k+1))
print("P(one adjacent rung below 75%) = P(correct < ceil(.75n))")
for n in [16,40,80]:
    need=int(np.ceil(0.75*n))
    print(n, "need", need, " ".join(f"a={a}:{cdf(need-1,n,a):.3f}" for a in [0.99,0.95,0.90,0.85,0.80,0.75,0.70,0.60,0.50]))
print("\nFull rule (7 rungs, 2 adjacent at accuracy a, 5 others at 0.99, unresolved rate u): P(pass)")
def sim(a,n,u=0.02,reps=20000,other=0.99):
    tot_ok=0
    res=rng.binomial(n,1-u,size=(reps,7))
    accs=np.array([a,a,other,other,other,other,other])
    corr=rng.binomial(res,accs)
    slip=(res-corr).sum(1)/res.sum(1)
    adj=(corr[:,:2]/np.maximum(res[:,:2],1))
    unres=(n*7-res.sum(1))/(n*7)
    ok=(slip<=0.10)&(adj>=0.75).all(1)&(unres<=0.10)
    return ok.mean()
for n in [16,40,80]:
    print(n," ".join(f"a={a}:{sim(a,n):.3f}" for a in [0.99,0.95,0.90,0.85,0.80,0.75,0.70,0.60,0.50]))
print("\nsame, but 'other' rungs at 0.95")
for n in [16,40,80]:
    print(n," ".join(f"a={a}:{sim(a,n,other=0.95):.3f}" for a in [0.99,0.95,0.90,0.85,0.80,0.75,0.70,0.60,0.50]))
