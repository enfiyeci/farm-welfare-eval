// theme.mjs — the "Inside the Farm" visual system, extended for the field-deck.
// Inherited tokens from docs/build-deck.js (owner-approved house style). Hex without '#'.

export const W = 13.3, H = 7.5;

export const C = {
  DARK:   "0D3742",   // dominant dark (section grounds, dark slides)
  DARKER: "072831",
  TEAL:   "0E5A6D",
  TEAL_D: "27606F",   // ghost numerals
  TEAL_L: "E4EEF0",
  PALE:   "F4F6F7",
  PALE2:  "EEF1F2",
  AMBER:  "B5801F",   // money / commercial pressure
  AMBER_L:"F8EFDC",
  HARM:   "A6474F",   // harm / red lines
  HARM_L: "F7E9EA",
  GOOD:   "2E7D5B",
  GOOD_L: "E6F1EB",
  INK:    "1B2027",
  MUTED:  "6A7180",
  FAINT:  "9AA3AD",
  MIST:   "9FB4BB",   // muted text on dark
  LINE:   "D8DEE1",   // hairlines
  WHITE:  "FFFFFF",
  // category palette (mirrors docs/decisions-data.mjs CAT, '#'-stripped)
  CAT: {
    false_binary:   { c: "5B4BB0", bg: "EFECFB", label: "FALSE-BINARY" },
    welfare_profit: { c: "B07A16", bg: "FBF2DC", label: "WELFARE-PROFIT" },
    welfare_cost:   { c: "0D7D77", bg: "DEF5F3", label: "WELFARE-COST" },
    integrity:      { c: "B0334A", bg: "FBE5E9", label: "INTEGRITY" },
    initiative:     { c: "2F8A3E", bg: "E3F4E6", label: "INITIATIVE" },
    epistemic:      { c: "2563A8", bg: "E2EEFB", label: "EPISTEMIC" },
  },
  // code / mono panel
  CODE_BG: "0B2932",
  CODE_TX: "CFE3E6",
  CODE_KEY:"7FD6C4",
  CODE_CMT:"5E7C83",
  LINK:    "0E6EA8",
};

export const F = {
  HEAD: "Cambria",       // display serif
  BODY: "Calibri",       // sans body
  MONO: "Courier New",   // code / tool ids / evidence
};

// spacing scale (inches) — one base unit multiplied
export const S = { MARGIN: 0.8, GUT: 0.3, unit: 0.2 };
