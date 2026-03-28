from __future__ import annotations

from linguoos import config
from linguoos.providers.mock import MockProvider


def get_provider():
    """Provider factory.

    Default: mock provider.

    NOTE: Real providers (openai/anthropic) are intentionally not implemented
    to preserve the 'no outbound network' constraint unless explicitly tasked.
    """

    name = (config.PROVIDER or "mock").lower()
    if name == "mock":
        return MockProvider()

    # Placeholders for future integrations.
    if name in {"openai", "anthropic"}:
        raise NotImplementedError(
            f"Provider '{name}' is a placeholder. Implement under linguoos/providers/ explicitly when allowed."
        )

    raise ValueError(f"Unknown provider: {name}")
