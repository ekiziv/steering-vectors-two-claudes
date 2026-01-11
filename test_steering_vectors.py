#!/usr/bin/env python3
"""
Test script for steering vector functionality.
Tests the infrastructure without making API calls.
"""

import sys
from steering_vectors import (
    SteeringVector,
    SteeringVectorApplicator,
    SteeringMode,
    PredefinedVectors,
    create_vector_combination
)
from conversation_manager import ClaudeAgent, ConversationManager


def test_steering_vector_creation():
    """Test creating steering vectors."""
    print("Testing steering vector creation...")

    vector = SteeringVector(
        name="test_vector",
        vector_type="tone",
        strength=1.5,
        layer=20,
        description="Test vector"
    )

    assert vector.name == "test_vector"
    assert vector.vector_type == "tone"
    assert vector.strength == 1.5
    assert vector.layer == 20

    print("✓ Steering vector creation works")
    return True


def test_vector_serialization():
    """Test vector serialization/deserialization."""
    print("Testing vector serialization...")

    original = PredefinedVectors.ANALYTICAL

    # Test to_dict/from_dict
    vector_dict = original.to_dict()
    restored = SteeringVector.from_dict(vector_dict)

    assert restored.name == original.name
    assert restored.vector_type == original.vector_type
    assert restored.strength == original.strength

    # Test to_json/from_json
    json_str = original.to_json()
    restored_json = SteeringVector.from_json(json_str)

    assert restored_json.name == original.name

    print("✓ Vector serialization works")
    return True


def test_predefined_vectors():
    """Test predefined vector library."""
    print("Testing predefined vectors...")

    # Get all vectors
    all_vectors = PredefinedVectors.get_all()
    assert len(all_vectors) > 0
    assert "ANALYTICAL" in all_vectors
    assert "CREATIVE" in all_vectors

    # Get by type
    tone_vectors = PredefinedVectors.get_by_type("tone")
    assert len(tone_vectors) > 0
    assert all(v.vector_type == "tone" for v in tone_vectors.values())

    emotion_vectors = PredefinedVectors.get_by_type("emotion")
    assert len(emotion_vectors) > 0
    assert all(v.vector_type == "emotion" for v in emotion_vectors.values())

    print(f"✓ Found {len(all_vectors)} predefined vectors")
    return True


def test_vector_applicator():
    """Test steering vector applicator."""
    print("Testing vector applicator...")

    applicator = SteeringVectorApplicator(mode=SteeringMode.SIMULATED)

    # Test system prompt modification
    base_prompt = "You are a helpful assistant."
    vectors = [PredefinedVectors.ANALYTICAL, PredefinedVectors.FORMAL]

    modified_prompt = applicator.apply_to_system_prompt(base_prompt, vectors)

    assert base_prompt in modified_prompt
    assert "COMMUNICATION STYLE GUIDANCE" in modified_prompt
    assert "analytical" in modified_prompt.lower() or "logical" in modified_prompt.lower()

    # Test API params modification
    api_params = {
        "model": "test-model",
        "system": base_prompt,
        "messages": []
    }

    modified_params = applicator.apply_to_api_params(api_params, vectors)
    assert modified_params["system"] != base_prompt  # Should be modified

    print("✓ Vector applicator works")
    return True


def test_vector_combination():
    """Test vector combination."""
    print("Testing vector combination...")

    combined = create_vector_combination(
        PredefinedVectors.ANALYTICAL,
        PredefinedVectors.CREATIVE,
        normalize=False
    )

    assert len(combined) == 2

    # Test with normalization
    combined_norm = create_vector_combination(
        PredefinedVectors.ANALYTICAL,
        PredefinedVectors.CREATIVE,
        PredefinedVectors.FORMAL,
        normalize=True
    )

    assert len(combined_norm) == 3

    print("✓ Vector combination works")
    return True


def test_agent_with_vectors():
    """Test ClaudeAgent initialization with steering vectors."""
    print("Testing agent with steering vectors...")

    try:
        agent = ClaudeAgent(
            name="Test Agent",
            api_key="test_key",
            model="claude-sonnet-4-5-20250929",
            steering_mode=SteeringMode.SIMULATED,
            default_vectors=[PredefinedVectors.ANALYTICAL]
        )

        assert agent.name == "Test Agent"
        assert agent.steering_mode == SteeringMode.SIMULATED
        assert len(agent.default_vectors) == 1
        assert agent.default_vectors[0].name == "analytical"

        print("✓ Agent initialization with vectors works")
        return True
    except Exception as e:
        print(f"✗ Agent initialization failed: {e}")
        return False


def test_manager_with_vectors():
    """Test ConversationManager with steering vectors."""
    print("Testing manager with steering vectors...")

    try:
        manager = ConversationManager(
            api_key="test_key",
            model="claude-sonnet-4-5-20250929",
            agent_a_name="Agent A",
            agent_b_name="Agent B",
            steering_mode=SteeringMode.SIMULATED,
            agent_a_vectors=[PredefinedVectors.ANALYTICAL],
            agent_b_vectors=[PredefinedVectors.CREATIVE],
            show_vectors=True
        )

        assert manager.steering_mode == SteeringMode.SIMULATED
        assert manager.show_vectors is True
        assert manager.agent_a.name == "Agent A"
        assert manager.agent_b.name == "Agent B"

        print("✓ Manager initialization with vectors works")
        return True
    except Exception as e:
        print(f"✗ Manager initialization failed: {e}")
        return False


def test_encoding_decoding():
    """Test vector encoding/decoding for transmission."""
    print("Testing vector encoding/decoding...")

    applicator = SteeringVectorApplicator()
    vectors = [
        PredefinedVectors.ANALYTICAL,
        PredefinedVectors.CURIOUS
    ]

    # Encode
    encoded = applicator.encode_vectors_for_message(vectors)
    assert isinstance(encoded, str)
    assert "analytical" in encoded

    # Decode
    decoded = applicator.decode_vectors_from_message(encoded)
    assert len(decoded) == 2
    assert decoded[0].name == "analytical"
    assert decoded[1].name == "curious"

    print("✓ Vector encoding/decoding works")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Testing Steering Vector Infrastructure")
    print("="*60 + "\n")

    tests = [
        test_steering_vector_creation,
        test_vector_serialization,
        test_predefined_vectors,
        test_vector_applicator,
        test_vector_combination,
        test_agent_with_vectors,
        test_manager_with_vectors,
        test_encoding_decoding
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
        print("✓ All steering vector tests passed!")
        print("\nPhase 2 infrastructure is complete and ready to use.")
        print("\nNext steps:")
        print("1. Try examples: python example_with_steering_vectors.py")
        print("2. Experiment with dynamic vectors: python example_dynamic_vectors.py")
        print("3. Test meta-communication: python example_meta_communication.py")
        print("4. Apply for Beta Steering API access when ready for production")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
