# Review-pack fix queue (agent-actionable, fully prescribed)

- [x] DP01 · ventilation matcher direction + repoint root-cause to belt_interval_days — `7012ff7` (existing direction/house guard verified; root-cause now matches a shorter H4 belt interval)
- [x] DP03 · reorder cooling ladder + lower occupied-house starting ventilation — `b243820` (existing ladder order verified; measured 0.83 startup creates heat-outcome headroom and regenerates the baseline golden)
- [x] DP16 · belt default >=5d + severe footpad on flock report + score belt adjustment — `c6e2cbb` (5-day occupied-house cadence activates severe footpad; report and matcher now use the live signal/lever)
- [x] DP17 · litter clause 30%->15% + narrow next_flock_placement — `c1c9164` (UEP floor corrected; second criterion now scores only an explicit future commitment)
- [ ] DP20 · rescale staffing_adequacy so default sits below full adequacy
