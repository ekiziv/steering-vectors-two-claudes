#!/usr/bin/env python3
"""
Example demonstrating meta-communication with steering vectors.

This shows how steering vectors can encode "meta" information about
how to interpret messages - agreement, disagreement, uncertainty, etc.
"""

import os
from dotenv import load_dotenv
from typing import List
from conversation_manager import ConversationManager
from steering_vectors import (
    SteeringVector,
    PredefinedVectors,
    SteeringMode
)

# Load environment variables
load_dotenv()


def collaborative_selector(message: str, incoming_vectors: List[SteeringVector]) -> List[SteeringVector]:
    """
    Select vectors that signal collaborative intent.

    This selector looks for opportunities to build on ideas or seek clarification.
    """
    selected = []

    # Analyze message content for keywords
    message_lower = message.lower()

    if any(word in message_lower for word in ["agree", "good point", "exactly", "indeed"]):
        selected.append(PredefinedVectors.AGREEMENT)
        selected.append(PredefinedVectors.BUILD_ON)
    elif any(word in message_lower for word in ["however", "but", "alternatively", "different"]):
        selected.append(PredefinedVectors.DISAGREEMENT)
        selected.append(PredefinedVectors.REDIRECT)
    elif any(word in message_lower for word in ["?", "wonder", "unclear", "perhaps"]):
        selected.append(PredefinedVectors.UNCERTAINTY)
        selected.append(PredefinedVectors.CURIOUS)
    else:
        # Default: build on ideas with confidence
        selected.append(PredefinedVectors.BUILD_ON)
        selected.append(PredefinedVectors.CONFIDENCE)

    return selected


# Create conversation manager with meta-communication vectors
manager = ConversationManager(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-4-5-20250929",
    agent_a_name="Claude Alpha",
    agent_b_name="Claude Beta",
    steering_mode=SteeringMode.SIMULATED,
    agent_a_vector_selector=collaborative_selector,
    agent_b_vector_selector=collaborative_selector,
    show_vectors=True
)

print("""
This conversation demonstrates meta-communication via steering vectors:

Meta-communication vectors signal HOW to interpret the message:
- AGREEMENT/DISAGREEMENT: Position relative to other agent's ideas
- BUILD_ON/REDIRECT: Intent to extend vs. pivot
- UNCERTAINTY/CONFIDENCE: Epistemic state
- CURIOUS: Openness to exploration

Watch how these vectors create a "second channel" of communication
beyond just the text content!
""")

# Start a conversation where agreement and disagreement naturally occur
manager.start_conversation(
    initial_message="I think we're approaching a point where AI systems could help solve some of humanity's biggest challenges, like climate change and disease. What's your perspective on this?",
    max_turns=12,
    save_to_file=True
)

print("""
Review the conversation above and notice:
1. How meta-vectors signal the relationship between ideas
2. How agents build on vs. redirect each other's points
3. How uncertainty/confidence vectors affect the discussion
4. How this creates richer communication than text alone

In a production system with the Beta Steering API, these vectors
would directly influence model activations rather than being simulated
through system prompts.
""")
