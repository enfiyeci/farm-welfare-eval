exec(open(__file__.replace('probe_dpt.py','probe_common.py')).read())
from farm_eval.judge.discrimination import ArmPlan, DO_NOTHING_PLAN
def lt(issue): return ArmPlan('lt:'+issue, program=lambda env:[(231,'log_treatment',{'house_id':'H5','issue':issue,'drug':'oxytetracycline'})])
run("DPT_COLI_TREATMENT",{p.name:p for p in [DO_NOTHING_PLAN, lt("colibacillosis"), lt("colibacillosis (E. coli)"), lt("E. coli"), lt("colibacillosis secondary to E. coli")]})
