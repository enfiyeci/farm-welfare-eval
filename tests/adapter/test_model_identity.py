from farm_eval.models import model_family, same_model_family


def test_model_family_uses_provider_prefixes():
    assert model_family("anthropic/claude-sonnet-5-5") == "anthropic"
    assert model_family("anthropic/vertex/claude-opus-5-5") == "anthropic"
    assert model_family("google/gemini-3.8-flash") == "google"
    assert model_family("openai/gpt-6") == "openai"
    assert model_family("mockllm/model") == "other"


def test_same_family_does_not_equate_unrecognised_providers():
    assert same_model_family("anthropic/a", "anthropic/b") is True
    assert same_model_family("anthropic/a", "google/b") is False
    assert same_model_family("mockllm/a", "mockllm/b") is False
