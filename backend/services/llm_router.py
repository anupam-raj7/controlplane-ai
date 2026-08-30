"""
Chooses which model to call based on prompt complexity, then calls it through LiteLLM.

LiteLLM gives one unified interface across providers (OpenAI, Anthropic, etc.), so swapping
or adding a provider only means changing the model name string, not the calling code.
"""

import os
import time

import litellm

from config import settings

# LiteLLM reads provider credentials from environment variables (GROQ_API_KEY,
# OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, etc.) rather than a single shared
# argument, so we mirror whatever is set in .env into the process environment once at
# import time. This means you only ever need to set the ONE key you're actually using.
for _env_name, _value in [
    ("OPENAI_API_KEY", settings.openai_api_key),
    ("ANTHROPIC_API_KEY", settings.anthropic_api_key),
    ("GROQ_API_KEY", settings.groq_api_key),
    ("GEMINI_API_KEY", settings.gemini_api_key),
]:
    if _value:
        os.environ[_env_name] = _value

# A simple, explainable complexity heuristic. In production you'd likely swap this for a small
# classifier, but a heuristic is transparent and good enough to demonstrate routing behavior.
COMPLEXITY_KEYWORDS = [
    "analyze",
    "compare",
    "design",
    "architecture",
    "strategy",
    "prove",
    "derive",
    "optimize",
    "explain in depth",
    "step by step",
]


def pick_model(prompt: str, force_model: str | None = None) -> str:
    """Return the model name to use for this prompt."""
    if force_model:
        return force_model

    word_count = len(prompt.split())
    has_complex_keyword = any(keyword in prompt.lower() for keyword in COMPLEXITY_KEYWORDS)

    if word_count > 60 or has_complex_keyword:
        return settings.capable_model
    return settings.cheap_model


def call_model(prompt: str, model: str) -> dict:
    """
    Calls the chosen model via LiteLLM and returns the response text, token counts, an
    estimated cost, and latency. Falls back to a clearly-labeled stub response if no API key
    is configured, so the rest of the pipeline can still be demoed without live credentials.
    """
    has_any_key = any(
        [settings.openai_api_key, settings.anthropic_api_key, settings.groq_api_key, settings.gemini_api_key]
    )
    if not has_any_key:
        return _stub_response(prompt, model)

    start = time.perf_counter()
    try:
        # No api_key= argument needed here — LiteLLM picks the right key up from the
        # environment variables set above, based on the "<provider>/<model>" prefix.
        completion = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        latency_ms = int((time.perf_counter() - start) * 1000)

        text = completion["choices"][0]["message"]["content"]
        usage = completion.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)

        try:
            cost = litellm.completion_cost(completion_response=completion)
        except Exception:
            cost = 0.0

        return {
            "text": text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": round(cost, 6),
            "latency_ms": latency_ms,
        }
    except Exception as exc:  # noqa: BLE001 - surface any provider error as a stub, not a crash
        return _stub_response(prompt, model, error=str(exc))


def _stub_response(prompt: str, model: str, error: str | None = None) -> dict:
    """Used when no API key is set, or a live call fails, so the demo keeps working."""
    note = f" (stub — no API key configured{': ' + error if error else ''})"
    return {
        "text": f"[Simulated response to: '{prompt[:80]}...']{note}",
        "input_tokens": len(prompt.split()),
        "output_tokens": 20,
        "estimated_cost_usd": 0.0,
        "latency_ms": 5,
    }
