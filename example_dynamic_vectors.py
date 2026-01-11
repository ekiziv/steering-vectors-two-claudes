#!/usr/bin/env python3
"""
Example demonstrating dynamic steering vector selection.

This shows how agents can adapt their communication style by dynamically
selecting steering vectors based on the conversation context and the
vectors received from the other agent.
"""

import os
from dotenv import load_dotenv
from typing import List
from conversation_manager import ConversationManager
from steering_vectors import (
    SteeringVector,
    PredefinedVectors,
    SteeringMode,
    create_vector_combination
)

# Load environment variables
load_dotenv()


def agent_a_selector(message: str, incoming_vectors: List[SteeringVector]) -> List[SteeringVector]:
    """
    Agent A dynamically selects vectors based on context.

    This agent responds to the other agent's vectors:
    - If receiving CREATIVE, balance with ANALYTICAL
    - If receiving OPTIMISTIC, balance with CAUTIOUS
    - If receiving ABSTRACT, provide CONCRETE examples
    """
    selected = []

    if incoming_vectors:
        vector_names = [v.name for v in incoming_vectors]

        # Balance creative with analytical
        if "creative" in vector_names:
            selected.append(PredefinedVectors.ANALYTICAL)

        # Balance optimistic with cautious
        if "optimistic" in vector_names:
            selected.append(PredefinedVectors.CAUTIOUS)

        # Balance abstract with concrete
        if "abstract" in vector_names:
            selected.append(PredefinedVectors.CONCRETE)

    # Add curiosity to keep the conversation flowing
    selected.append(PredefinedVectors.CURIOUS)

    return selected


def agent_b_selector(message: str, incoming_vectors: List[SteeringVector]) -> List[SteeringVector]:
    """
    Agent B dynamically selects vectors to complement Agent A.

    This agent tries to add creativity and positivity:
    - If receiving ANALYTICAL, add CREATIVE perspective
    - If receiving CAUTIOUS, add OPTIMISTIC viewpoint
    - If receiving CONCRETE, lift to ABSTRACT
    """
    selected = []

    if incoming_vectors:
        vector_names = [v.name for v in incoming_vectors]

        # Add creativity to analytical thinking
        if "analytical" in vector_names:
            selected.append(PredefinedVectors.CREATIVE)

        # Add optimism to caution
        if "cautious" in vector_names:
            selected.append(PredefinedVectors.OPTIMISTIC)

        # Add abstract thinking to concrete
        if "concrete" in vector_names:
            selected.append(PredefinedVectors.ABSTRACT)

    # Add philosophical depth
    selected.append(PredefinedVectors.PHILOSOPHICAL)

    return selected


# Create conversation manager with dynamic vector selection
manager = ConversationManager(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-4-5-20250929",
    agent_a_name="Responsive Claude",
    agent_b_name="Complementary Claude",
    steering_mode=SteeringMode.SIMULATED,
    agent_a_vector_selector=agent_a_selector,
    agent_b_vector_selector=agent_b_selector,
    show_vectors=True
)

print("""
This conversation demonstrates dynamic steering vector selection:
- Responsive Claude balances the other's style (creative↔analytical, optimistic↔cautious)
- Complementary Claude adds complementary perspectives
- Vectors change dynamically based on incoming signals
- This creates a richer, more nuanced conversation

Watch how the steering vectors adapt throughout the conversation!
""")

# Start a conversation about a complex topic
manager.start_conversation(
    initial_message="What role should AI systems play in making important societal decisions, such as healthcare resource allocation or criminal justice?",
    max_turns=10,
    save_to_file=True
)
