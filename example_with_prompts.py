#!/usr/bin/env python3
"""
Example with different system prompts for each Claude.
This demonstrates how the infrastructure supports different personalities,
which will be useful when we add steering vectors.
"""

import os
from dotenv import load_dotenv
from conversation_manager import ConversationManager

# Load environment variables
load_dotenv()

# Define different system prompts (preparing for steering vector differentiation)
system_a = """You are an optimistic AI assistant who focuses on possibilities
and potential. You tend to see the bright side of technological developments
and emphasize opportunities for growth and innovation."""

system_b = """You are a cautious AI assistant who emphasizes careful analysis
and potential risks. You tend to think critically about technological developments
and emphasize the importance of ethics, safety, and unintended consequences."""

# Create conversation manager with different prompts
manager = ConversationManager(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-4-5-20250929",
    agent_a_name="Optimistic Claude",
    agent_b_name="Cautious Claude",
    agent_a_system=system_a,
    agent_b_system=system_b
)

# Start a conversation about AI development
manager.start_conversation(
    initial_message="What are your thoughts on the rapid development of AI capabilities and their impact on society?",
    max_turns=8,
    save_to_file=True
)
