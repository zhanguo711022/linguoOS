"""Placeholder for OpenAI provider.

Intentionally NOT implemented by default to comply with:
- do not connect to external network unless explicitly tasked
- keep /api/v1/* contracts stable

Implementations should live here when enabled.
"""


class OpenAIProvider:  # pragma: no cover
    name = "openai"

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("OpenAI provider is a placeholder.")
