#!/usr/bin/env python3
"""
Test script to verify the code structure without making API calls.
"""

import sys
from conversation_manager import ClaudeAgent, ConversationManager


def test_imports():
    """Test that all imports work."""
    print("✓ All imports successful")
    return True


def test_agent_initialization():
    """Test that ClaudeAgent can be initialized."""
    try:
        agent = ClaudeAgent(
            name="Test Agent",
            api_key="test_key",
            model="claude-sonnet-4-5-20250929",
            system_prompt="Test prompt"
        )
        assert agent.name == "Test Agent"
        assert agent.model == "claude-sonnet-4-5-20250929"
        assert agent.system_prompt == "Test prompt"
        assert len(agent.conversation_history) == 0
        print("✓ ClaudeAgent initialization works")
        return True
    except Exception as e:
        print(f"✗ ClaudeAgent initialization failed: {e}")
        return False


def test_manager_initialization():
    """Test that ConversationManager can be initialized."""
    try:
        manager = ConversationManager(
            api_key="test_key",
            model="claude-sonnet-4-5-20250929",
            agent_a_name="Agent A",
            agent_b_name="Agent B"
        )
        assert manager.agent_a.name == "Agent A"
        assert manager.agent_b.name == "Agent B"
        assert len(manager.full_conversation) == 0
        print("✓ ConversationManager initialization works")
        return True
    except Exception as e:
        print(f"✗ ConversationManager initialization failed: {e}")
        return False


def test_history_management():
    """Test conversation history methods."""
    try:
        agent = ClaudeAgent(
            name="Test Agent",
            api_key="test_key",
            model="claude-sonnet-4-5-20250929"
        )

        # Test history is empty
        assert len(agent.get_history()) == 0

        # Test reset (should not error even when empty)
        agent.reset_history()
        assert len(agent.get_history()) == 0

        print("✓ History management works")
        return True
    except Exception as e:
        print(f"✗ History management failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Testing Two Claudes Conversation App Structure")
    print("="*60 + "\n")

    tests = [
        test_imports,
        test_agent_initialization,
        test_manager_initialization,
        test_history_management
    ]

    results = []
    for test in tests:
        results.append(test())
        print()

    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    print("="*60 + "\n")

    if passed == total:
        print("✓ All structural tests passed!")
        print("\nThe code is ready to use. To run actual conversations:")
        print("1. Set up your .env file with ANTHROPIC_API_KEY")
        print("2. Run: python main.py")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
