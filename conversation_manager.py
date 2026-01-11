"""
Conversation Manager for Two Claude Models

This module orchestrates conversations between two Claude AI instances,
with infrastructure for future steering vector integration.
"""

import os
from typing import List, Dict, Optional, Any
from anthropic import Anthropic
from datetime import datetime
import json


class ClaudeAgent:
    """Represents a single Claude AI agent in the conversation."""

    def __init__(
        self,
        name: str,
        api_key: str,
        model: str = "claude-sonnet-4-5-20250929",
        system_prompt: Optional[str] = None,
        steering_vector: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a Claude agent.

        Args:
            name: Identifier for this agent (e.g., "Claude A", "Claude B")
            api_key: Anthropic API key
            model: Model identifier to use
            system_prompt: Optional system prompt to customize behavior
            steering_vector: Optional steering vector parameters (for future use)
        """
        self.name = name
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt or "You are a helpful AI assistant engaging in a conversation."
        self.steering_vector = steering_vector
        self.conversation_history: List[Dict[str, str]] = []

    def respond(self, message: str) -> str:
        """
        Generate a response to the given message.

        Args:
            message: The message to respond to

        Returns:
            The agent's response
        """
        # Add the message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })

        # Prepare API call parameters
        api_params = {
            "model": self.model,
            "max_tokens": 1024,
            "system": self.system_prompt,
            "messages": self.conversation_history
        }

        # TODO: Add steering vector support when available in API
        # if self.steering_vector:
        #     api_params["steering_vector"] = self.steering_vector

        # Get response from Claude
        response = self.client.messages.create(**api_params)

        # Extract the response text
        response_text = response.content[0].text

        # Add to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response_text
        })

        return response_text

    def reset_history(self):
        """Clear the conversation history for this agent."""
        self.conversation_history = []

    def get_history(self) -> List[Dict[str, str]]:
        """Get the full conversation history."""
        return self.conversation_history.copy()


class ConversationManager:
    """Manages conversations between two Claude agents."""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4-5-20250929",
        agent_a_name: str = "Claude A",
        agent_b_name: str = "Claude B",
        agent_a_system: Optional[str] = None,
        agent_b_system: Optional[str] = None
    ):
        """
        Initialize the conversation manager.

        Args:
            api_key: Anthropic API key
            model: Model identifier to use for both agents
            agent_a_name: Name for the first agent
            agent_b_name: Name for the second agent
            agent_a_system: System prompt for agent A
            agent_b_system: System prompt for agent B
        """
        self.agent_a = ClaudeAgent(
            name=agent_a_name,
            api_key=api_key,
            model=model,
            system_prompt=agent_a_system
        )

        self.agent_b = ClaudeAgent(
            name=agent_b_name,
            api_key=api_key,
            model=model,
            system_prompt=agent_b_system
        )

        self.full_conversation: List[Dict[str, str]] = []

    def start_conversation(
        self,
        initial_message: str,
        max_turns: Optional[int] = None,
        save_to_file: bool = True
    ):
        """
        Start a conversation between the two agents.

        Args:
            initial_message: The message to start the conversation
            max_turns: Maximum number of turns (None for unlimited)
            save_to_file: Whether to save the conversation to a file
        """
        print(f"\n{'='*60}")
        print(f"Starting conversation between {self.agent_a.name} and {self.agent_b.name}")
        print(f"{'='*60}\n")

        # Start with the initial message to Agent A
        print(f"[INITIAL MESSAGE TO {self.agent_a.name}]\n{initial_message}\n")

        self.full_conversation.append({
            "speaker": "MODERATOR",
            "message": initial_message,
            "timestamp": datetime.now().isoformat()
        })

        current_message = initial_message
        current_agent = self.agent_a
        other_agent = self.agent_b
        turn_count = 0

        try:
            while True:
                # Check turn limit
                if max_turns and turn_count >= max_turns:
                    print(f"\n[CONVERSATION ENDED: Reached maximum of {max_turns} turns]")
                    break

                # Get response from current agent
                print(f"[{current_agent.name}]")
                response = current_agent.respond(current_message)
                print(f"{response}\n")
                print(f"{'-'*60}\n")

                # Record in full conversation
                self.full_conversation.append({
                    "speaker": current_agent.name,
                    "message": response,
                    "timestamp": datetime.now().isoformat(),
                    "turn": turn_count + 1
                })

                # Swap agents
                current_message = response
                current_agent, other_agent = other_agent, current_agent
                turn_count += 1

        except KeyboardInterrupt:
            print("\n\n[CONVERSATION INTERRUPTED BY MODERATOR]")

        print(f"\n{'='*60}")
        print(f"Conversation ended after {turn_count} turns")
        print(f"{'='*60}\n")

        # Save conversation if requested
        if save_to_file:
            self.save_conversation()

    def save_conversation(self, filename: Optional[str] = None):
        """
        Save the conversation to a JSON file.

        Args:
            filename: Optional filename (defaults to timestamped file)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"

        # Create directory if it doesn't exist
        os.makedirs("conversation_history", exist_ok=True)
        filepath = os.path.join("conversation_history", filename)

        # Save conversation
        with open(filepath, 'w') as f:
            json.dump(self.full_conversation, f, indent=2)

        print(f"Conversation saved to: {filepath}")

    def reset(self):
        """Reset both agents and clear conversation history."""
        self.agent_a.reset_history()
        self.agent_b.reset_history()
        self.full_conversation = []
