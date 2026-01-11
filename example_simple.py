#!/usr/bin/env python3
"""
Simple example of running a conversation between two Claudes.
"""

import os
from dotenv import load_dotenv
from conversation_manager import ConversationManager

# Load environment variables
load_dotenv()

# Create conversation manager
manager = ConversationManager(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-4-5-20250929",
    agent_a_name="Claude A",
    agent_b_name="Claude B"
)

# Start a simple conversation
manager.start_conversation(
    initial_message="Hello! What are your thoughts on creativity in artificial intelligence?",
    max_turns=6,  # 3 exchanges each
    save_to_file=True
)
