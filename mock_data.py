"""Canned answers for demo mode: exercises the full pipeline with no API key and no cost.

Field names below match agents.py's Diagnosis / Overlap / Synthesis schemas by name only
(no import, to avoid a circular import with agents.py, which imports llm.py, which imports this).
"""

_MARKER = "[DEMO MODE - mock output, no Claude call was made]"

_SCENARIOS = [
	(
		("right lower quadrant", "abdominal pain", "appendectomy"),
		{
			"diagnosis": "Acute gastroenteritis or mesenteric adenitis",
			"reasoning": [_MARKER, "Diffuse pain differs from the original appendicitis location", "No rebound tenderness on exam"],
			"differential": ["Recurrent appendicitis (rare post-appendectomy)", "Ovarian pathology", "Mesenteric ischemia"],
			"score": "Low",
			"rationale": [_MARKER, "Prior appendectomy is resolved surgical history", "Current diffuse pain differs from the original presentation"],
			"impact": "Prior appendectomy lowers the likelihood of recurrent appendicitis but does not explain the current diffuse pain.",
			"next_steps": ["Abdominal CT", "Fluid resuscitation", "Surgical consult if symptoms worsen"],
		},
	),
	(
		("chest", "shortness of breath", "myocardial infarction", "stent"),
		{
			"diagnosis": "Community-acquired pneumonia or pleural effusion",
			"reasoning": [_MARKER, "Decreased breath sounds localize to the right lower lobe", "No jugular venous distension argues against heart failure"],
			"differential": ["Acute coronary syndrome", "Pulmonary embolism", "Heart failure exacerbation"],
			"score": "Medium",
			"rationale": [_MARKER, "Cardiac history raises baseline risk but does not fully explain a focal lung finding", "Respiratory exam points toward a pulmonary cause"],
			"impact": "The prior MI raises cardiac risk and warrants monitoring but a respiratory cause better fits the exam.",
			"next_steps": ["Chest X-ray", "ECG and cardiac biomarkers", "Pulse oximetry trend"],
		},
	),
	(
		("joint pain", "fatigue", "pharyngitis"),
		{
			"diagnosis": "Post-viral syndrome",
			"reasoning": [_MARKER, "Symptoms began during a viral URI and persisted after it resolved", "No swelling, erythema, or morning stiffness on exam"],
			"differential": ["Reactive arthritis", "Early autoimmune condition", "Depression / fatigue syndrome"],
			"score": "Low",
			"rationale": [_MARKER, "Strep pharyngitis 6 months ago is temporally distant and treated", "Current joint pattern does not match post-streptococcal disease"],
			"impact": "The distant strep infection is unlikely to explain fatigue and joint pain 6 months later.",
			"next_steps": ["CBC and inflammatory markers", "Rheumatologic panel if symptoms persist", "Symptomatic care"],
		},
	),
	(
		("back pain", "straight leg raise", "degenerative disc"),
		{
			"diagnosis": "Acute disc herniation with radiculopathy",
			"reasoning": [_MARKER, "New leg radiation, numbness and a positive straight leg raise are acute findings", "Chronic back pain history does not explain the new neurologic findings"],
			"differential": ["Spinal stenosis", "Cauda equina syndrome (if it progresses)", "Chronic degenerative disc disease alone"],
			"score": "Medium",
			"rationale": [_MARKER, "Chronic disc disease is a plausible substrate for a new acute herniation", "The new radicular findings are the dominant, more urgent signal"],
			"impact": "The chronic history explains susceptibility but should not delay work-up of the new acute neurologic findings.",
			"next_steps": ["MRI lumbar spine", "Assess for red-flag symptoms (bowel/bladder)", "Neurology or spine referral"],
		},
	),
]

_DEFAULT_SCENARIO = {
	"diagnosis": "[DEMO] Diagnosis pending a real Claude API call",
	"reasoning": [_MARKER, "Set ANTHROPIC_API_KEY (or clear DEBIAS_MOCK) to get a real diagnosis for this case."],
	"differential": ["[DEMO] Differential unavailable in demo mode"],
	"score": "Medium",
	"rationale": [_MARKER, "Overlap scoring needs a real model call."],
	"impact": "[DEMO] Impact analysis unavailable in demo mode.",
	"next_steps": ["[DEMO] Connect a real Claude API key to see real next steps"],
}


def _pick_scenario(text: str) -> dict:
	lowered = text.lower()
	for keywords, scenario in _SCENARIOS:
		if any(k in lowered for k in keywords):
			return scenario
	return _DEFAULT_SCENARIO


def mock_response(schema, user_text: str):
	"""Build a schema instance from canned data. Understands Diagnosis, Overlap and Synthesis by field name."""
	s = _pick_scenario(user_text)
	fields = set(schema.model_fields)

	if fields == {"diagnosis", "reasoning", "differential"}:
		return schema(diagnosis=s["diagnosis"], reasoning=s["reasoning"], differential=s["differential"])

	if fields == {"score", "rationale"}:
		return schema(score=s["score"], rationale=s["rationale"])

	if fields >= {"most_likely_diagnosis", "agrees_with_agent1", "differential", "impact_of_past_disease", "next_steps"}:
		# Agent 1 and the blind Agent 2 call both draw from the same scenario, so their
		# diagnosis text is identical here - keep this True so the demo copy stays consistent.
		return schema(
			most_likely_diagnosis=s["diagnosis"],
			agrees_with_agent1=True,
			differential=s["differential"],
			impact_of_past_disease=f"{_MARKER} {s['impact']}",
			next_steps=s["next_steps"],
		)

	raise ValueError(f"mock_data has no canned response for schema fields {sorted(fields)}")
