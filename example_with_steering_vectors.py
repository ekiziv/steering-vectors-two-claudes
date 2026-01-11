#!/usr/bin/env python3
"""
Example demonstrating steering vector communication between two Claudes.

This example shows how steering vectors enable richer AI-to-AI communication
beyond just text. Each Claude applies different steering vectors that influence
both its own behavior and signal intent to the other Claude.
"""

import os
from dotenv import load_dotenv
from conversation_manager import ConversationManager
from steering_vectors import PredefinedVectors, SteeringMode

# Load environment variables
load_dotenv()

# Create conversation manager with steering vectors enabled
# Agent A will be analytical and cautious
# Agent B will be creative and optimistic
manager = ConversationManager(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-4-5-20250929",
    agent_a_name="Analytical Claude",
    agent_b_name="Creative Claude",
    steering_mode=SteeringMode.SIMULATED,  # Use simulated steering (via prompts)
    agent_a_vectors=[
        PredefinedVectors.ANALYTICAL,
        PredefinedVectors.CAUTIOUS
    ],
    agent_b_vectors=[
        PredefinedVectors.CREATIVE,
        PredefinedVectors.OPTIMISTIC
    ],
    show_vectors=True  # Display which steering vectors are active
)

print("""
This conversation demonstrates steering vector communication:
- Analytical Claude uses 'analytical' and 'cautious' steering vectors
- Creative Claude uses 'creative' and 'optimistic' steering vectors
- These vectors influence both the content and style of responses
- In simulated mode, they work via enhanced system prompts
- In Beta API mode (when available), they'd directly modify model activations
""")

# Start a conversation about innovation
manager.start_conversation(
    initial_message="Let's discuss the future of human-AI collaboration. What possibilities excite you, and what challenges should we consider?",
    max_turns=8,
    save_to_file=True
)
