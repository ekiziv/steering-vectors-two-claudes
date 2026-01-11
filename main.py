#!/usr/bin/env python3
"""
Main entry point for the Two Claudes Conversation App.

This script provides an interactive CLI for managing conversations
between two Claude AI instances.
"""

import os
import sys
from dotenv import load_dotenv
from conversation_manager import ConversationManager


def main():
    """Main function to run the conversation app."""
    # Load environment variables
    load_dotenv()

    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key (see .env.example)")
        sys.exit(1)

    print("\n" + "="*60)
    print("Two Claudes Conversation App")
    print("="*60 + "\n")

    # Get user input for conversation setup
    print("Configuration:")
    print("-" * 60)

    # Initial message
    print("\nEnter the initial message to start the conversation:")
    initial_message = input("> ").strip()

    if not initial_message:
        initial_message = "Hello! Let's have an interesting conversation about artificial intelligence and consciousness."
        print(f"Using default: {initial_message}")

    # Max turns
    print("\nEnter maximum number of turns (or press Enter for unlimited):")
    max_turns_input = input("> ").strip()

    max_turns = None
    if max_turns_input:
        try:
            max_turns = int(max_turns_input)
        except ValueError:
            print("Invalid number, using unlimited turns.")

    # Model selection
    print("\nSelect model:")
    print("1. Claude Sonnet 4.5 (default, recommended)")
    print("2. Claude Opus 4.5 (more capable, slower)")
    print("3. Claude Haiku 3.5 (faster, less expensive)")
    model_choice = input("> ").strip()

    model_map = {
        "1": "claude-sonnet-4-5-20250929",
        "2": "claude-opus-4-5-20251101",
        "3": "claude-3-5-haiku-20241022",
        "": "claude-sonnet-4-5-20250929"
    }

    model = model_map.get(model_choice, "claude-sonnet-4-5-20250929")
    print(f"Using model: {model}")

    # System prompts (same for now, but infrastructure for different ones)
    system_prompt = "You are a helpful AI assistant engaging in a conversation with another AI. Be thoughtful, curious, and engage meaningfully with the topics discussed."

    # Create conversation manager
    manager = ConversationManager(
        api_key=api_key,
        model=model,
        agent_a_name="Claude A",
        agent_b_name="Claude B",
        agent_a_system=system_prompt,
        agent_b_system=system_prompt
    )

    print("\n" + "="*60)
    print("Press Ctrl+C at any time to stop the conversation (as moderator)")
    print("="*60 + "\n")

    input("Press Enter to start the conversation...")

    # Start the conversation
    manager.start_conversation(
        initial_message=initial_message,
        max_turns=max_turns,
        save_to_file=True
    )

    # Post-conversation options
    print("\nWhat would you like to do?")
    print("1. Start a new conversation")
    print("2. Exit")

    choice = input("> ").strip()

    if choice == "1":
        manager.reset()
        main()
    else:
        print("\nThank you for using Two Claudes Conversation App!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
