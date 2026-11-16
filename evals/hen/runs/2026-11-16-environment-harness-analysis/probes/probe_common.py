import sys,json,pathlib; import os; ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../../..')); sys.path.insert(0,ROOT)
from farm_eval.env.loader import load_corpus, load_schedule
from farm_eval.env.model import ModelParams
from farm_eval.env.snapshot import derive_snapshot
from farm_eval.judge.discrimination import evaluate_episode, ArmPlan, DO_NOTHING_PLAN
from scripts.regen_node_episodes import default_arm_episodes
R=ROOT+'/'
corpus,schedule=load_corpus(R+'corpus'),load_schedule(R+'schedule')
params=ModelParams(); refs=json.loads(pathlib.Path(R+'farm_eval/judge/node_reference.json').read_text())
eps={e.episode_id:e for e in default_arm_episodes()}
def run(eid, plans):
    ep=eps[eid]; snap,_=derive_snapshot(corpus,schedule,params,ep,seed=0)
    r=evaluate_episode(corpus,schedule,params,ep,snap,plans,refs[eid])
    for n,a in r.arms.items():
        print(eid,n,'lower',None if a.lower is None else round(a.lower,2),'upper',None if a.upper is None else round(a.upper,2),[(c.name,round(c.lower,2)) for c in a.criteria], flush=True)
occ=lambda env:[h for h,c in env.state.world.bird_count.items() if c>0]
