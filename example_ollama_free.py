#!/usr/bin/env python3
"""
Example using FREE local models via Ollama.

This example demonstrates the two AI conversation with steering vectors
using completely free, locally-run models. No API key or payment required!

Prerequisites:
1. Install Ollama: https://ollama.ai
2. Start Ollama: ollama serve
3. Pull a model: ollama pull llama3.2
4. Run this script!
"""

from conversation_manager import ConversationManager
from steering_vectors import PredefinedVectors, SteeringMode
from model_backends import BackendType, create_backend, OLLAMA_MODELS
import sys


def check_ollama():
    """Check if Ollama is running and suggest models."""
    print("Checking Ollama availability...")

    backend = create_backend(BackendType.OLLAMA, model="llama3.2")

    if not backend.is_available():
        print("\n❌ Ollama is not running or not installed!")
        print("\nTo use free local models:")
        print("1. Install Ollama from: https://ollama.ai")
        print("2. Start it: ollama serve")
        print("3. Pull a model: ollama pull llama3.2")
        print("\nOr use Anthropic API (paid) - see example_simple.py")
        sys.exit(1)

    print("✓ Ollama is running!\n")
    return True


def main():
    """Run a conversation using free Ollama models."""

    check_ollama()

    print("="*60)
    print("FREE Two AI Conversation with Steering Vectors")
    print("Using Ollama - No API key required!")
    print("="*60)
    print()

    # Show available models
    print("Recommended free models:")
    for model_id, info in OLLAMA_MODELS.items():
        print(f"  - {model_id}: {info['name']} ({info['size']})")
        print(f"    {info['description']}")
    print()

    # Use a lightweight model
    model = "llama3.2"  # Fast 3B parameter model
    print(f"Using model: {model}")
    print("(Change this in the script if you want a different model)")
    print()

    # Create backend
    backend = create_backend(
        BackendType.OLLAMA,
        model=model
    )

    # Create conversation manager with steering vectors
    manager = ConversationManager(
        backend=backend,
        agent_a_name="Analytical AI",
        agent_b_name="Creative AI",
        steering_mode=SteeringMode.SIMULATED,
        agent_a_vectors=[
            PredefinedVectors.ANALYTICAL,
            PredefinedVectors.CAUTIOUS
        ],
        agent_b_vectors=[
            PredefinedVectors.CREATIVE,
            PredefinedVectors.OPTIMISTIC
        ],
        show_vectors=True
    )

    print("Starting conversation...")
    print("Press Ctrl+C to stop at any time")
    print()

    # Start conversation
    manager.start_conversation(
        initial_message="What are the most exciting possibilities for artificial intelligence in the next decade?",
        max_turns=8,
        save_to_file=True
    )

    print("\n" + "="*60)
    print("All done! This conversation was 100% free and local.")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("\nAnd that you have a model installed:")
        print("  ollama pull llama3.2")
