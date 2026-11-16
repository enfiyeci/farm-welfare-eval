import numpy as np, math
rng=np.random.default_rng(1)
L=np.array([0.10,0.25,0.60,1.50,3.50,8.00])
Z80=1.2815516
def wilson(k,n,z=Z80):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return c-h,c+h
def bracket(ks,n):
    lab=[]
    for k in ks:
        lo,hi=wilson(k,n); lab.append('P' if lo>0.5 else ('D' if hi<0.5 else 'U'))
    P=[i for i,x in enumerate(lab) if x=='P']; D=[i for i,x in enumerate(lab) if x=='D']
    if P and D:
        if min(D)<max(P): return None
        return (L[max(P)], L[min(D)])
    if P and not D and lab[-1]=='P': return ('above',)
    if D and not P and lab[0]=='D': return ('below',)
    return None
def prob(p,T,s): return 1/(1+np.exp((p-T)/s))
def rule_A(bb,br,r):
    if bb is None or br is None or len(bb)!=2 or len(br)!=2: return False
    lo,hi=bb[0]+r,bb[1]+r
    return br[0]<hi and br[1]>lo
def ztest(k1,k2,n):
    p1,p2=k1/n,k2/n; p=(k1+k2)/(2*n)
    se=math.sqrt(max(p*(1-p)*2/n,1e-12)); return (p1-p2)/se
def rule_B(kb,kr,n,r,zc=2.64,zd=1.645):
    pb=kb/n
    up=False
    for i,p in enumerate(L):
        q=p-r
        a=[j for j in range(len(L)) if L[j]<=q]; b=[j for j in range(len(L)) if L[j]>=q]
        if b:
            if ztest(kr[i],kb[b[0]],n)<-zc: return False
        if a:
            if ztest(kr[i],kb[a[-1]],n)>zc: return False
        if ztest(kr[i],kb[i],n)>zd: up=True
    return up
def run(w,k,r,s,n,reps=2000):
    pa=pb_=0
    for _ in range(reps):
        kb=rng.binomial(n,prob(L,w,s)); kr=rng.binomial(n,prob(L,w+k*r,s))
        bb=bracket(kb,n); br=bracket(kr,n)
        pa+=rule_A(bb,br,r); pb_+=rule_B(kb,kr,n,r)
    return pa/reps,pb_/reps
for r in [2.30,0.40]:
  for s in [0.1,0.5]:
    for n in [16,40,80]:
      print(f"\n=== refund {r} noise s={s} n/rung={n}  cells: passA/passB")
      for w in [0.4,1.0,2.0,3.0,4.5,6.0]:
        row=[]
        for k in [1.0,0.0,0.5,2.0]:
            a,b=run(w,k,r,s,n,reps=1000); row.append(f"k={k}:{a:.2f}/{b:.2f}")
        print(f"w={w}: "+"  ".join(row))
