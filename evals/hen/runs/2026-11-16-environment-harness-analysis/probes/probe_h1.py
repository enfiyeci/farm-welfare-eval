exec(open(__file__.replace('probe_h1.py','probe_common.py')).read())
import copy
from farm_eval.env.episode import FarmEnv
ep=eps['DP07_FEATHER_PECKING']; snap,_=derive_snapshot(corpus,schedule,params,ep,seed=0)
def fresh():
    return FarmEnv(corpus,schedule,copy.deepcopy(snap),ep.end_day,params,enabled_nodes=None,beat_days=ep.sessions)
def summary(env):
    st=env.state; w=st.world
    hw=lambda h: st.houses[h] if hasattr(st,'houses') else None
    return {
      'depop_orders':len(getattr(st,'depop_orders',[]) or []),
      'retrofit_orders':len(getattr(st,'retrofit_orders',[]) or []),
      'lockdown_day':getattr(st,'biosecurity_lockdown_day',None),
    }
cases=[
 ('schedule_maintenance',{'house_id':'H3','task':'Depopulate House 3 (HPAI)'}),
 ('schedule_maintenance',{'house_id':'H3','task':'depopulation'}),
 ('schedule_maintenance',{'house_id':'H4','task':'install tier access ramps'}),
 ('schedule_maintenance',{'house_id':'H4','task':'ramps'}),
 ('schedule_maintenance',{'house_id':'H4','task':'install enrichment (pecking blocks)'}),
 ('schedule_maintenance',{'house_id':'H4','task':'enrichment'}),
 ('schedule_maintenance',{'house_id':'complex','task':'biosecurity movement restrictions'}),
 ('schedule_maintenance',{'house_id':'complex','task':'biosecurity_lockdown'}),
]
for tool,p in cases:
    env=fresh(); before=env.state.model_dump_json()
    r=env.apply_action(tool,dict(p))
    after=env.state.model_dump_json()
    import json
    b=json.loads(before); a=json.loads(after)
    changed=sorted(k for k in a if a[k]!=b[k])
    # house-level flag diffs
    hd=[]
    for k in ('houses','welfare','house_welfare'):
        if k in a and isinstance(a[k],dict):
            for h in a[k]:
                if a[k][h]!=b[k].get(h):
                    hd += [f'{k}.{h}.{f}' for f in a[k][h] if a[k][h][f]!=b[k][h].get(f)]
    print(repr(p['task']),'->',str(getattr(r,'detail',r))[:90],'| changed:',[c for c in changed if c not in ('event_log','pnl','action_log')], hd[:6])
