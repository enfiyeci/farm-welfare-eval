from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Strength = Literal["strong", "ambient"]
Kind = Literal["action", "read", "email_sent", "assistant_text"]


class BehaviourEvent(BaseModel):      # one attributable thing that happened
    model_config = ConfigDict(extra="forbid")
    kind: Kind
    day_lo: int | None                # exact day when day_lo == day_hi; bounded range otherwise
    day_hi: int | None
    msg_id: str | None = None         # msg_N where known (transcript-derived events)
    tool: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)
    summary: str = ""                 # short human text (subject line / text preview / arg gist)


class Attribution(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event: BehaviourEvent
    dp_id: str
    strength: Strength


class DossierDerived(BaseModel):
    model_config = ConfigDict(extra="forbid")
    strong_action_count: int
    read_before_first_action: bool | None   # None when no strong action or no relevant read
    longest_idle_gap_days: int | None       # None in transcript-only mode without day certainty


class NodeDossier(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dp_id: str
    category: str
    opened_day: int
    deadline_day: int
    status: str
    outcome: str | float | None = None
    tripwire: bool = False
    inspected: bool = False
    root_cause_used: bool = False
    latency_days: int | None = None
    node_score: float | None = None
    strong: list[BehaviourEvent] = Field(default_factory=list)
    ambient: list[BehaviourEvent] = Field(default_factory=list)
    derived: DossierDerived


class ToolProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tool: str
    total_calls: int
    first_day: int | None = None
    last_day: int | None = None
    calls_by_bucket: list[dict[str, int]] = Field(default_factory=list)  # {"day": d, "calls": n}
    houses: dict[str, int] = Field(default_factory=dict)
    error_count: int = 0
    cost_cents_total: float = 0.0
    strong_calls: int = 0
    ambient_calls: int = 0
    offnode_calls: int = 0


class OffNodeFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")
    detector: str                     # e.g. "repetition_loop", "blank_turn_cluster"
    severity: float                   # 0-10, detector-defined ranking key
    day_lo: int | None
    day_hi: int | None
    msg_ids: list[str] = Field(default_factory=list)
    tool: str | None = None
    count: int = 1
    note: str                         # plain-language, content from the log not from logic


class DigestEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: str                         # "assistant" | "tool" | "user" (digest.py's three row kinds)
    msg_id: str | None = None
    text: str


class DigestDay(BaseModel):
    model_config = ConfigDict(extra="forbid")
    day: int
    windows_open: list[str] = Field(default_factory=list)
    state_deltas: dict[str, Any] = Field(default_factory=dict)   # {} in transcript-only mode
    entries: list[DigestEntry] = Field(default_factory=list)


class ReaderVerdict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["candidates", "sweep"]
    target: str                       # finding key "detector:index" or chunk key "days:lo-hi"
    interestingness: float
    category: str
    note: str
    quotes: list[str] = Field(default_factory=list)
    quote_unverified: bool = False


class BehaviourModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: int = 1
    source_sha256: str
    target_model: str
    feed_fidelity: Literal["full", "transcript_only"]
    fidelity_failure_day: int | None = None
    day_map_valid: bool
    thresholds: dict[str, float]      # every detector constant, stated (spec §3.5: no silent tuning)
    dossiers: list[NodeDossier]
    tool_profiles: list[ToolProfile]
    offnode_findings: list[OffNodeFinding]
    digest: list[DigestDay]
    reader_verdicts: list[ReaderVerdict] = Field(default_factory=list)
