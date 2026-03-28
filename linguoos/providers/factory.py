from linguoos.config import settings
from linguoos.providers.anthropic_provider import AnthropicProvider
from linguoos.providers.mock import MockProvider
from linguoos.providers.openai_provider import OpenAIProvider


def get_provider():
    name = settings.provider.lower()
    if name == "mock":
        return MockProvider()
    if name == "openai":
        return OpenAIProvider()
    if name == "anthropic":
        return AnthropicProvider()
    raise ValueError(f"Unknown provider: {settings.provider}")
