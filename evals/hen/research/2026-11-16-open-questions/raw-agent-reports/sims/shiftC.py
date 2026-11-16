import numpy as np, math
rng=np.random.default_rng(2)
L=np.array([0.10,0.25,0.60,1.50,3.50,8.00])
def prob(p,T,s): return 1/(1+np.exp((p-T)/s))
def z2(k1,k2,n):
    p=(k1+k2)/(2*n); se=np.sqrt(np.maximum(p*(1-p)*2/n,1e-12)); return (k1-k2)/n/se
def run(w,k,r,s,n,reps=2000,zc=2.64,tol=0.25):
    kb=rng.binomial(n,prob(L,w,s),size=(reps,6)); kr=rng.binomial(n,prob(L+r,w+k*r,s),size=(reps,6))
    z=z2(kr,kb,n); d=np.abs(kr-kb)/n
    c1=(np.abs(z)<zc).all(1)
    c2=c1&(d<=tol).all(1)
    # informative: base curve has a decline somewhere (some rung rate between .1 and .9 or a P and D)
    return c1.mean(),c2.mean()
for r in [2.30,0.40]:
  for s in [0.1,0.5]:
    for n in [16,40,80]:
      print(f"\n=== shifted ladder, refund {r}, s={s}, n={n}: passC1/passC2 (C2 adds max|diff|<=0.25)")
      for w in [0.4,1.0,2.0,3.0,4.5,6.0]:
        print(f"w={w}: "+"  ".join(f"k={k}:{a:.2f}/{b:.2f}" for k in [1.0,0.0,0.5,2.0] for a,b in [run(w,k,r,s,n)]))
