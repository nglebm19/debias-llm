import json

import pytest

from agents import Diagnosis, Overlap, Synthesis, parse_case, run_medical_analysis
from cases import SAMPLE_CASES, get_case_description, strip_bias_note
from llm import LLMClient, LLMError


class FakeParsed:
	def __init__(self, parsed, stop_reason="end_turn"):
		self.parsed_output = parsed
		self.stop_reason = stop_reason


class FakeAnthropic:
	"""Stands in for anthropic.Anthropic; records every prompt it is sent."""

	def __init__(self):
		self.calls = []
		self.messages = self

	def parse(self, model, max_tokens, system, messages, output_format):
		self.calls.append({"system": system, "user": messages[0]["content"], "schema": output_format})
		if output_format is Diagnosis:
			return FakeParsed(Diagnosis(diagnosis="Dx", reasoning=["r"], differential=["d"]))
		if output_format is Overlap:
			return FakeParsed(Overlap(score="Low", rationale=["unrelated"]))
		return FakeParsed(Synthesis(
			most_likely_diagnosis="Final", agrees_with_agent1=False,
			differential=["d"], impact_of_past_disease="none", next_steps=["CT"],
		))


def make_llm(tmp_path, fake=None):
	return LLMClient(model="test-model", cache_dir=tmp_path, client=fake or FakeAnthropic())


def test_parse_case_sections():
	case = parse_case(strip_bias_note(get_case_description("case_1")))
	assert "Appendectomy" in case.pmh
	assert "Appendectomy" not in case.presentation
	assert "Abdomen: Soft" in case.exam
	assert "This case demonstrates" not in case.full


def test_parse_case_without_headers_falls_back_to_presentation():
	case = parse_case("just some free text")
	assert case.hpi == "just some free text"
	assert case.pmh == ""


def test_bias_note_stripped_from_all_sample_cases():
	for case_id in SAMPLE_CASES:
		assert "demonstrates" not in strip_bias_note(get_case_description(case_id))


def test_blind_agent_never_sees_past_history(tmp_path):
	fake = FakeAnthropic()
	result = run_medical_analysis(strip_bias_note(get_case_description("case_1")), make_llm(tmp_path, fake))
	assert result["status"] == "success"
	blind_call = next(c for c in fake.calls if "NOT given" in c["system"])
	assert "Appendectomy" not in blind_call["user"]
	assert "Past Medical History" not in blind_call["user"]
	overlap_call = next(c for c in fake.calls if c["schema"] is Overlap)
	assert "Appendectomy" in overlap_call["user"]


def test_pipeline_makes_four_calls_and_returns_structure(tmp_path):
	fake = FakeAnthropic()
	result = run_medical_analysis(strip_bias_note(get_case_description("case_2")), make_llm(tmp_path, fake))
	assert len(fake.calls) == 4
	assert set(result["structured"]) == {"agent1", "agent2_blind", "agent2_overlap", "agent3"}
	assert "Overlap Summary" in result["overlap"]


def test_cache_avoids_repeat_calls(tmp_path):
	fake = FakeAnthropic()
	llm = make_llm(tmp_path, fake)
	text = strip_bias_note(get_case_description("case_3"))
	run_medical_analysis(text, llm)
	first = len(fake.calls)
	run_medical_analysis(text, llm)
	assert len(fake.calls) == first


def test_refusal_becomes_llm_error(tmp_path):
	class Refusing(FakeAnthropic):
		def parse(self, **kw):
			return FakeParsed(None, stop_reason="refusal")
	with pytest.raises(LLMError):
		make_llm(tmp_path, Refusing()).generate("s", "u", Diagnosis)


def test_pipeline_reports_error_instead_of_raising(tmp_path):
	class Broken(FakeAnthropic):
		def parse(self, **kw):
			raise RuntimeError("no key")
	result = run_medical_analysis("x", make_llm(tmp_path, Broken()))
	assert result["status"] == "error"
	assert "no key" in result["error"]


def test_auto_mock_mode_when_no_api_key_and_no_client(tmp_path, monkeypatch):
	monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
	monkeypatch.delenv("DEBIAS_MOCK", raising=False)
	llm = LLMClient(cache_dir=tmp_path)  # no client injected -> auto-detects demo mode
	assert llm.mock is True

	result = run_medical_analysis(strip_bias_note(get_case_description("case_1")), llm)
	assert result["status"] == "success"
	assert result["mock"] is True
	assert "DEMO" in result["agent1"]


def test_injected_client_is_never_auto_mocked(tmp_path, monkeypatch):
	monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
	monkeypatch.delenv("DEBIAS_MOCK", raising=False)
	llm = make_llm(tmp_path, FakeAnthropic())
	assert llm.mock is False


def test_debias_mock_env_forces_mock_on(tmp_path, monkeypatch):
	monkeypatch.setenv("DEBIAS_MOCK", "1")
	llm = make_llm(tmp_path, FakeAnthropic())  # forced mock overrides the injected client
	assert llm.mock is True


def test_debias_mock_env_forces_mock_off(tmp_path, monkeypatch):
	monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
	monkeypatch.setenv("DEBIAS_MOCK", "0")
	llm = LLMClient(cache_dir=tmp_path)
	assert llm.mock is False
