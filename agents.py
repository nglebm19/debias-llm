import logging
import re
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel

from llm import LLMClient, get_client

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Case parsing
# ---------------------------------------------------------------------------

_SECTION_KEYS = {
	"patient": "demographics",
	"chief complaint": "chief_complaint",
	"history of present illness": "hpi",
	"past medical history": "pmh",
	"physical examination": "exam",
}


@dataclass
class Case:
	demographics: str = ""
	chief_complaint: str = ""
	hpi: str = ""
	pmh: str = ""
	exam: str = ""

	@property
	def presentation(self) -> str:
		"""Everything except past medical history: what Agent 2 may see in its blind step."""
		parts = [
			("Patient", self.demographics),
			("Chief Complaint", self.chief_complaint),
			("History of Present Illness", self.hpi),
			("Physical Examination", self.exam),
		]
		return "\n\n".join(f"{title}:\n{body}" for title, body in parts if body)

	@property
	def full(self) -> str:
		pmh = f"\n\nPast Medical History:\n{self.pmh}" if self.pmh else ""
		return self.presentation + pmh


def parse_case(text: str) -> Case:
	"""Split case text into sections. Text without recognised headers is treated as the presentation."""
	sections: dict[str, list[str]] = {}
	current = None
	for line in text.splitlines():
		m = re.match(r"^\s*([A-Za-z ]+?)\s*:\s*(.*)$", line)
		key = _SECTION_KEYS.get(m.group(1).strip().lower()) if m else None
		if m and key:
			current = key
			sections[current] = [m.group(2)] if m.group(2) else []
		elif current:
			sections[current].append(line)
	if not sections:
		return Case(hpi=text.strip())
	return Case(**{k: "\n".join(v).strip() for k, v in sections.items()})


# ---------------------------------------------------------------------------
# Structured outputs
# ---------------------------------------------------------------------------

class Diagnosis(BaseModel):
	diagnosis: str
	reasoning: list[str]
	differential: list[str]


class Overlap(BaseModel):
	score: Literal["High", "Medium", "Low"]
	rationale: list[str]


class Synthesis(BaseModel):
	most_likely_diagnosis: str
	agrees_with_agent1: bool
	differential: list[str]
	impact_of_past_disease: str
	next_steps: list[str]


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

_DISCLAIMER = "This is an educational demo, not clinical advice."

_A1_SYSTEM = f"""You are Agent 1 (Diagnostician), an experienced clinician. Given the full case, including past medical history, give your single most likely diagnosis, the key findings supporting it, and a short differential. {_DISCLAIMER}"""

_A2_BLIND_SYSTEM = f"""You are Agent 2 (Independent Devil's Advocate), a critical clinician. You are deliberately NOT given the patient's past medical history. Diagnose using only the current symptoms and physical exam. Do not guess or assume a past history. {_DISCLAIMER}"""

_A2_OVERLAP_SYSTEM = f"""You are Agent 2 (Independent Devil's Advocate). You already made a diagnosis from current symptoms and exam alone. Now you are shown the past medical history. Rate the overlap between the past medical history and the current presentation:
- High: the past condition plausibly explains or directly relates to the current symptoms.
- Medium: partial or indirect relationship (e.g. risk factor, complication).
- Low: past condition is resolved or unrelated to the current presentation.
Explain the rating and say whether the past history is likely to bias a clinician who sees it. {_DISCLAIMER}"""

_A3_SYSTEM = f"""You are Agent 3 (Synthesizer). You receive the full case, Agent 1's diagnosis (made with past history) and Agent 2's blind diagnosis plus its overlap rating. Weigh the two, decide the most likely diagnosis, and explain how the past disease does or does not affect it. If overlap is Low, be cautious about letting past history drive the diagnosis. Set agrees_with_agent1 to whether your final diagnosis matches Agent 1's. {_DISCLAIMER}"""


def _fmt_dx(dx: Diagnosis) -> str:
	return (
		f"Diagnosis: {dx.diagnosis}\n"
		f"Reasoning: {'; '.join(dx.reasoning)}\n"
		f"Differential: {'; '.join(dx.differential)}"
	)


def diagnostician_agent(case: Case, llm: LLMClient) -> Diagnosis:
	"""Agent 1: full case (HPI + PMH + exam)."""
	return llm.generate(_A1_SYSTEM, case.full, Diagnosis)


def blind_da_agent(case: Case, llm: LLMClient) -> Diagnosis:
	"""Agent 2, step 1: diagnosis from symptoms + exam only. PMH never enters this prompt."""
	return llm.generate(_A2_BLIND_SYSTEM, case.presentation, Diagnosis)


def overlap_agent(case: Case, blind: Diagnosis, llm: LLMClient) -> Overlap:
	"""Agent 2, step 2: reveal PMH and score overlap with the current presentation."""
	user = (
		f"{case.presentation}\n\n"
		f"Your blind diagnosis:\n{_fmt_dx(blind)}\n\n"
		f"Past Medical History:\n{case.pmh or 'None recorded'}"
	)
	return llm.generate(_A2_OVERLAP_SYSTEM, user, Overlap)


def synthesizer_agent(case: Case, a1: Diagnosis, blind: Diagnosis, overlap: Overlap, llm: LLMClient) -> Synthesis:
	"""Agent 3: combine both perspectives."""
	user = (
		f"{case.full}\n\n"
		f"--- Agent 1 (saw past history) ---\n{_fmt_dx(a1)}\n\n"
		f"--- Agent 2 (blind to past history) ---\n{_fmt_dx(blind)}\n"
		f"Overlap with past history: {overlap.score}\n"
		f"Overlap rationale: {'; '.join(overlap.rationale)}"
	)
	return llm.generate(_A3_SYSTEM, user, Synthesis)


# ---------------------------------------------------------------------------
# Rendering (markdown for the UI)
# ---------------------------------------------------------------------------

def _bullets(items: list[str]) -> str:
	return "\n".join(f"- {i}" for i in items)


def render_diagnosis(dx: Diagnosis) -> str:
	return (
		f"**Diagnosis:** {dx.diagnosis}\n\n"
		f"**Reasoning:**\n{_bullets(dx.reasoning)}\n\n"
		f"**Differential:**\n{_bullets(dx.differential)}"
	)


def render_agent2(blind: Diagnosis, overlap: Overlap) -> str:
	return (
		f"**Diagnosis from symptoms + exam only:** {blind.diagnosis}\n\n"
		f"{_bullets(blind.reasoning)}\n\n"
		f"**Overlap with past history:** {overlap.score}\n\n"
		f"{_bullets(overlap.rationale)}"
	)


def render_synthesis(s: Synthesis) -> str:
	return (
		f"**Most likely diagnosis:** {s.most_likely_diagnosis}\n\n"
		f"**Differential:**\n{_bullets(s.differential)}\n\n"
		f"**Impact of past disease:** {s.impact_of_past_disease}\n\n"
		f"**Next steps:**\n{_bullets(s.next_steps)}"
	)


def render_overlap_summary(a1: Diagnosis, blind: Diagnosis, overlap: Overlap, s: Synthesis) -> str:
	if a1.diagnosis.strip().lower() == blind.diagnosis.strip().lower():
		agreement = "Agents 1 and 2 reached the same diagnosis."
	else:
		agreement = f"Agents disagree: **{a1.diagnosis}** (with history) vs **{blind.diagnosis}** (without)."
	changed = "Final answer kept Agent 1's diagnosis." if s.agrees_with_agent1 else "Final answer departs from Agent 1."
	return f"**Overlap Summary**\n\n- Score: {overlap.score}\n- {agreement}\n- {changed}"


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_medical_analysis(case_text: str, llm: LLMClient | None = None) -> dict:
	"""Run the 3-agent pipeline. Returns markdown per agent plus the structured results."""
	llm = llm or get_client()
	try:
		case = parse_case(case_text)
		a1 = diagnostician_agent(case, llm)
		blind = blind_da_agent(case, llm)
		overlap = overlap_agent(case, blind, llm)
		synth = synthesizer_agent(case, a1, blind, overlap, llm)
		return {
			"status": "success",
			"mock": llm.mock,
			"agent1": render_diagnosis(a1),
			"agent2": render_agent2(blind, overlap),
			"agent3": render_synthesis(synth),
			"overlap": render_overlap_summary(a1, blind, overlap, synth),
			"structured": {
				"agent1": a1.model_dump(),
				"agent2_blind": blind.model_dump(),
				"agent2_overlap": overlap.model_dump(),
				"agent3": synth.model_dump(),
			},
		}
	except Exception as e:
		logger.error(f"Pipeline error: {e}")
		return {"status": "error", "error": str(e)}
