"""Thin Claude client: structured output, on-disk response cache, injectable for tests."""
import hashlib
import json
import logging
import os
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from mock_data import mock_response

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

DEFAULT_MODEL = "claude-haiku-4-5"
DEFAULT_CACHE_DIR = Path(__file__).parent / ".cache" / "llm"


class LLMError(RuntimeError):
	"""Raised when the model call fails or returns no usable structured output."""


class LLMClient:
	def __init__(self, model=None, cache_dir=None, client=None, max_tokens=2000, mock=None):
		self.model = model or os.environ.get("DEBIAS_MODEL", DEFAULT_MODEL)
		self.max_tokens = max_tokens
		self._client = client
		if cache_dir is None and os.environ.get("DEBIAS_CACHE", "1") != "0":
			cache_dir = DEFAULT_CACHE_DIR
		self.cache_dir = Path(cache_dir) if cache_dir else None

		# Demo mode: no ANTHROPIC_API_KEY yet -> serve canned answers instead of failing.
		# DEBIAS_MOCK=1 forces it on, DEBIAS_MOCK=0 forces it off (real call, errors without a key).
		# An explicitly injected `client` (tests) always means real mode, regardless of env.
		if mock is None:
			flag = os.environ.get("DEBIAS_MOCK", "auto").lower()
			if flag == "1":
				mock = True
			elif flag == "0":
				mock = False
			else:
				mock = client is None and not os.environ.get("ANTHROPIC_API_KEY")
		self.mock = mock
		if self.mock:
			self.model = "mock"  # separate cache namespace so a later real key never reads mock output

	def _get_client(self):
		if self._client is None:
			import anthropic
			self._client = anthropic.Anthropic()
		return self._client

	def _cache_path(self, system, user, schema) -> Path:
		assert self.cache_dir is not None
		key = json.dumps(
			[self.model, system, user, schema.__name__, schema.model_json_schema()],
			sort_keys=True,
		)
		digest = hashlib.sha256(key.encode()).hexdigest()
		return self.cache_dir / f"{digest}.json"

	def generate(self, system: str, user: str, schema: type[T]) -> T:
		"""Return a validated `schema` instance. Identical calls are served from the cache."""
		path = self._cache_path(system, user, schema) if self.cache_dir else None
		if path and path.exists():
			return schema.model_validate_json(path.read_text())

		if self.mock:
			result: T = mock_response(schema, user)
		else:
			try:
				response = self._get_client().messages.parse(
					model=self.model,
					max_tokens=self.max_tokens,
					system=system,
					messages=[{"role": "user", "content": user}],
					output_format=schema,
				)
			except Exception as e:
				raise LLMError(f"Claude API call failed: {e}") from e

			if response.stop_reason == "refusal" or response.parsed_output is None:
				raise LLMError(f"No structured output (stop_reason={response.stop_reason})")

			result = response.parsed_output

		if path:
			path.parent.mkdir(parents=True, exist_ok=True)
			path.write_text(result.model_dump_json())
		return result


_default_client = None


def get_client() -> LLMClient:
	"""Process-wide client so the SDK client is built once."""
	global _default_client
	if _default_client is None:
		_default_client = LLMClient()
	return _default_client
