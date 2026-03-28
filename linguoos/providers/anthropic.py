"""Placeholder for Anthropic provider.

Intentionally NOT implemented by default to comply with:
- do not connect to external network unless explicitly tasked
- keep /api/v1/* contracts stable

Implementations should live here when enabled.
"""


class AnthropicProvider:  # pragma: no cover
    name = "anthropic"

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Anthropic provider is a placeholder.")
