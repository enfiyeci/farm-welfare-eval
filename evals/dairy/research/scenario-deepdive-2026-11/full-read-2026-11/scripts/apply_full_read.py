"""Apply the checked EFSA 2023 (dairy cows, calves) status changes to candidates.json."""
import json, sys
p = sys.argv[1]
d = json.load(open(p))
C = {c["id"]: c for c in d["candidates"]}
def setc(cid, i, s=None, t=None, src=None):
    cl = C[cid]["claims"][i - 1]
    if s: cl["s"] = s
    if t: cl["t"] = t
    if src: cl["src"] = src
def add(cid, s, t, src):
    C[cid]["claims"].append({"s": s, "t": t, "src": src})
E7993 = "EFSA 2023 dairy cows (EFSA Journal 21(5):7993), read in full 2026-11-10"
E7896 = "EFSA 2023 calves (EFSA Journal 21(3):7896), read in full 2026-11-10"
# Dairy cows
setc("A1", 5, "S", "Pain sensitivity (hyperalgesia) lasts at least 28 days after a lesion is detected, so lameness stays a welfare problem after treatment.", f"Whay 1998, via {E7993} (text lines 1280 to 1283). Earlier wording said 'after it heals'; EFSA dates it from detection.")
C["A1"]["claims"][5]["src"] = "No source in the repo. EFSA 2023 dairy recommends regular gait scoring with early treatment (its own advice, no efficacy data), so the cure-rate effect stays unsourced."
setc("A1", 7, "S", "Lying comfort drives lameness: shallow beds or mats raise claw disorders and lameness against deep-bedded cubicles (EFSA, 90 to 100% certainty); dry, soft lying surfaces cut standing time and lameness (50 to 100%). No footbath effect is shown, and the hazard studies are mostly observational.", f"{E7993}, conclusions (lines 4898 to 4901) and section on hazards (lines 2036 to 2042).")
setc("A2", 1, "S", "Above 1.2 cows per cubicle, lying time falls; even below 1.2, lying is less synchronous and aggression rises. EFSA recommends at least one cubicle per cow (90 to 100% certainty).", f"{E7993}, conclusion at lines 4977 to 4979 (its own judgement; primaries in the body).")
setc("A2", 2, "C", None, "No source in the repo. EFSA 2023 dairy Table 23 lists 'higher cow:cubicle ratio' with LESS lameness (Gieseke 2020), possibly a labelling slip; EFSA's experts still chose lameness as an outcome to measure for overstocking. Check Gieseke 2020.")
C["A3"]["claims"][1]["src"] += " EFSA 2023 dairy adds a US compost-barn study: lying time fell as the temperature-humidity index rose (Endres and Barberg 2007, line 1031)."
setc("A5", 1, "S", "Clinical mastitis is painful: cows eat and lie less, lie on one side and are restless at milking; severe cases cause hyperalgesia.", f"Siivonen 2011 and Fitzpatrick 1998, via {E7993} (lines 2080 to 2084).")
add("A5", "N", "Anti-inflammatory drugs reduce the pain signs of clinical mastitis.", "No source in the repo; split from A5.1 on 2026-11-10 because EFSA 2023 dairy covers only the pain.")
setc("B2", 1, "C", None, f"No source in the repo. {E7993} says there is no clear evidence of an important effect of laminitis or subacute ruminal acidosis on lameness (lines 2055 to 2057).")
C["A1"]["claims"][0]["src"] += " EFSA 2023 dairy gives no pooled mean or trend; its US rows: 55% lame (score 3+) in North-East US herds, 13.2% in 66 US herds (Cook 2016)."
# Calves
C["C1"]["claims"][0]["src"] = "No US source. EFSA 2023 calves says the great majority of EU dairy farms separate at or within about 1 hour of birth (its own judgement, certainty 90 to 100%)."
setc("C1", 2, "S", "Calves separated after the cow-calf bond forms (about 4 days) show more distress than calves separated at birth or within 24 hours; distress is worst from 4 days to 6 to 10 weeks of age, then falls with age. Calves separated at birth still call.", f"Weary and Chua 2000, Flower and Weary 2001, Stehulova 2008, Lidfors 1996, via {E7896} (lines 5277 to 5299, 5507 to 5512).")
setc("C1", 3, "S", "Cow-calf contact costs saleable milk: a Danish organic model puts it at 7.1% of 9,000 kg a year for full-time contact to 13 weeks. A Norwegian study found the loss offset by calf and cow health when suckling lasted at least 7 weeks; 13 weeks was unprofitable.", f"Mogensen 2022 (a model) and Asheim 2016, via {E7896} (lines 5180 to 5187).")
setc("C2", 1, "S", "The traditional milk ration of about 10% of body weight a day restricts growth; calves on 10 to 15% call more, butt empty buckets and make unrewarded feeder visits, unlike calves on about 20%. EFSA recommends about 20% to at least 4 weeks of age.", f"Thomas 2001, Herskin 2010, Jensen and Holm 2003, Palczynski 2020, via {E7896} (lines 685 to 689, 1210 to 1217, 3538 to 3541). The 'calves fed freely drink about twice as much' figure was not found.")
setc("C2", 2, "S", "Hungry calves call more (high-pitched vocalisations).", f"Thomas 2001, via {E7896} (lines 1213 to 1214).")
add("C2", "C", "Restricted milk raises cross-sucking: EFSA's experts estimate 64% of restricted-fed teat calves cross-suck against 30% fed freely; but EFSA also reports studies with no consistent effect of milk allowance before weaning.", f"{E7896}: EKE at lines 5444 to 5449 (experiments: Froberg 2008, Roth 2009b); no consistent effect at lines 1026 to 1027 (Mounier 2006, De Paula Vieira 2008).")
setc("C2", 3, "N", "Higher milk feeding raises first-lactation yield; studies disagree.", "No source in the repo. The growth half moved to its own claim on 2026-11-10.")
add("C2", "S", "Higher milk feeding raises calf growth.", f"Palczynski 2020 and Roth 2009a, via {E7896} (lines 685 to 687, 5258 to 5260).")
C["C4"]["claims"][0]["src"] += " EFSA 2023 calves: some evidence that male dairy calves get poorer colostrum than females (Fecteau 2002, Renaud 2020, Reed 2022; line 1427)."
add("C4", "S", "EU law requires every calf to get bovine colostrum within its first 6 hours; EFSA advises 10 to 12% of body weight of good colostrum by 6 hours.", f"Council Directive 2008/119/EC and Cortese 2009, Godden 2019, via {E7896} (lines 5147, 1359 to 1360).")
setc("C5", 1, "S", "Hot-iron and caustic-paste disbudding cause severe pain. Local anaesthesia can fail and must be checked; pain outlasts the analgesics usually given. Some EU states require anaesthesia and analgesia.", f"Knierim 2015, Thomsen 2021, Adcock and Tucker 2018, via {E7896} (lines 725 to 746).")
C["C5"]["claims"][4]["src"] = "No source in the repo. EFSA 2023 calves says polled bulls' availability and genetic merit 'will probably increase' (Mueller 2019, line 751): implied, not stated."
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(x["s"] for c in d["candidates"] if c["rec"] == "build" for x in c["claims"]))
