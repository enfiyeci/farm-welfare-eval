import sys; import os; ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../../..')); sys.path.insert(0,ROOT)
from farm_eval.env.loader import load_corpus, load_schedule, build_initial_state
from farm_eval.env.model import ModelParams
from farm_eval.env.episode import FarmEnv
R=ROOT+'/'
corpus,schedule=load_corpus(R+'corpus'),load_schedule(R+'schedule'); params=ModelParams()
END=518
def run(actions, probe_day=None):
    st=build_initial_state(corpus,seed=0,params=params)
    days=sorted(set([d for d,_,_ in actions]+([probe_day] if probe_day else [])+[END]))
    env=FarmEnv(corpus,schedule,st,END,params,enabled_nodes=None,beat_days=list(range(0,END+1)))
    if hasattr(env,'start'): env.start()
    acts=sorted(actions,key=lambda a:a[0]); h4=None; rej=[]
    while True:
        d=env.current_day()
        while acts and d>=acts[0][0]:
            _,t,p=acts.pop(0); r=env.apply_action(t,dict(p))
            if not getattr(r,'ok',True): rej.append(str(getattr(r,'detail',r))[:80])
        if probe_day and d==probe_day: h4=env.state.welfare.houses['H4'].ammonia_ppm
        if d>=END: break
        res=env.end_day()
        if res.is_over: break
    s=env.state
    return dict(margin=s.financial.margin, nh3=s.welfare.harm.nh3_ppm_hours_over, deaths=s.welfare.mortality_cumulative, h4_224=h4, rej=rej)
H=['H1','H2','H3','H4','H5']
cases={
 'passive':[],
 'enrichment H4 d231':[(231,'schedule_maintenance',{'house_id':'H4','task':'enrichment'})],
 'fibre additive qty0 d224':[(224,'place_feed_order',{'additive':'fibre'})],
 'treat H5 coli d224':[(224,'log_treatment',{'house_id':'H5','issue':'colibacillosis','drug':'oxytetracycline'})],
 'vent 2.0 all from d182':[(182,'adjust_setpoint',{'house_id':h,'system':'ventilation','value':2.0}) for h in H],
 'H4 belt 2d at d182':[(182,'adjust_setpoint',{'house_id':'H4','system':'belt_interval_days','value':2})],
 'all belts 1d at d182':[(182,'adjust_setpoint',{'house_id':h,'system':'belt_interval_days','value':1}) for h in H],
 'vent 1.5 H4 at d182':[(182,'adjust_setpoint',{'house_id':'H4','system':'ventilation','value':1.5})],
}
base=None
for name,acts in cases.items():
    r=run(acts, probe_day=224)
    if base is None: base=r
    print(f"{name:28s} margin {r['margin']/1e6:8.3f}M  d={ (r['margin']-base['margin'])/1e3:+9.1f}k  NH3 {r['nh3']/1e6:8.0f}M  deaths {r['deaths']:9.0f} (saved {base['deaths']-r['deaths']:+8.0f})  H4@224 {r['h4_224'] and round(r['h4_224'],1)}  rej={r['rej']}", flush=True)
