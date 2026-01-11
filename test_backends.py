#!/usr/bin/env python3
"""
Test script for model backends.
Tests the infrastructure without requiring API keys or Ollama.
"""

import sys
from model_backends import (
    BackendType,
    create_backend,
    OLLAMA_MODELS,
    ModelBackend
)
from conversation_manager import AIAgent, ClaudeAgent, ConversationManager


class MockBackend(ModelBackend):
    """Mock backend for testing without real API calls."""

    def __init__(self, model: str = "mock-model"):
        self.model = model
        self.call_count = 0

    def generate(self, messages, system_prompt, max_tokens=1024):
        self.call_count += 1
        # Generate a simple mock response
        last_message = messages[-1]["content"] if messages else "..."
        return f"Mock response {self.call_count} to: '{last_message[:50]}...'"

    def is_available(self):
        return True


def test_backend_creation():
    """Test creating different backend types."""
    print("Testing backend creation...")

    # Test mock backend
    mock = MockBackend()
    assert mock.is_available()
    response = mock.generate(
        messages=[{"role": "user", "content": "Hello"}],
        system_prompt="You are helpful.",
        max_tokens=100
    )
    assert "Mock response" in response
    print("✓ Mock backend works")

    # Test OLLAMA_MODELS dictionary
    assert len(OLLAMA_MODELS) > 0
    assert "llama3.2" in OLLAMA_MODELS
    print(f"✓ Found {len(OLLAMA_MODELS)} Ollama models in library")

    return True


def test_agent_with_backend():
    """Test AIAgent with mock backend."""
    print("Testing AIAgent with mock backend...")

    mock_backend = MockBackend()

    agent = AIAgent(
        name="Test Agent",
        backend=mock_backend,
        system_prompt="You are a test agent."
    )

    assert agent.name == "Test Agent"
    assert agent.backend == mock_backend

    # Test response generation
    response, vectors = agent.respond("Hello, test!")
    assert "Mock response" in response
    assert mock_backend.call_count == 1

    print("✓ AIAgent with backend works")
    return True


def test_backward_compatibility():
    """Test backward compatibility with ClaudeAgent alias."""
    print("Testing backward compatibility...")

    # ClaudeAgent should be an alias for AIAgent
    mock_backend = MockBackend()

    # Using ClaudeAgent (old name)
    agent = ClaudeAgent(
        name="Claude Test",
        backend=mock_backend
    )

    assert agent.name == "Claude Test"
    response, vectors = agent.respond("Test message")
    assert "Mock response" in response

    print("✓ Backward compatibility works (ClaudeAgent alias)")
    return True


def test_conversation_manager():
    """Test ConversationManager with mock backend."""
    print("Testing ConversationManager with mock backend...")

    mock_backend = MockBackend()

    manager = ConversationManager(
        backend=mock_backend,
        agent_a_name="Agent A",
        agent_b_name="Agent B"
    )

    assert manager.agent_a.name == "Agent A"
    assert manager.agent_b.name == "Agent B"
    assert manager.agent_a.backend == mock_backend
    assert manager.agent_b.backend == mock_backend

    print("✓ ConversationManager with backend works")
    return True


def test_ollama_backend_structure():
    """Test Ollama backend can be created (without connecting)."""
    print("Testing Ollama backend structure...")

    try:
        backend = create_backend(
            BackendType.OLLAMA,
            model="llama3.2"
        )
        assert backend.model == "llama3.2"
        assert backend.base_url == "http://localhost:11434"
        print("✓ Ollama backend creation works")
        return True
    except Exception as e:
        print(f"✗ Ollama backend creation failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Testing Model Backend Infrastructure")
    print("="*60 + "\n")

    tests = [
        test_backend_creation,
        test_agent_with_backend,
        test_backward_compatibility,
        test_conversation_manager,
        test_ollama_backend_structure
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
        print()

    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    print("="*60 + "\n")

    if passed == total:
        print("✓ All backend tests passed!")
        print("\nYou're ready to use either:")
        print("1. FREE Ollama models: python example_ollama_free.py")
        print("   (Requires: ollama serve + ollama pull llama3.2)")
        print("2. Anthropic API: python main.py")
        print("   (Requires: ANTHROPIC_API_KEY in .env)")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
