"""
Conversation Manager for Two AI Models

This module orchestrates conversations between two AI instances,
with infrastructure for steering vector integration.

Supports multiple backends:
- Anthropic API (paid, cloud-based)
- Ollama (free, local models)
"""

import os
from typing import List, Dict, Optional, Any, Callable, Union
from datetime import datetime
import json

from steering_vectors import (
    SteeringVector,
    SteeringVectorApplicator,
    SteeringMode,
    PredefinedVectors
)

from model_backends import (
    ModelBackend,
    BackendType,
    create_backend
)


class AIAgent:
    """Represents a single AI agent in the conversation (supports multiple backends)."""

    def __init__(
        self,
        name: str,
        backend: Optional[ModelBackend] = None,
        api_key: Optional[str] = None,  # For backward compatibility
        model: str = "claude-sonnet-4-5-20250929",
        system_prompt: Optional[str] = None,
        steering_mode: SteeringMode = SteeringMode.SIMULATED,
        default_vectors: Optional[List[SteeringVector]] = None,
        vector_selector: Optional[Callable[[str, List[SteeringVector]], List[SteeringVector]]] = None
    ):
        """
        Initialize an AI agent.

        Args:
            name: Identifier for this agent (e.g., "Agent A", "Agent B")
            backend: ModelBackend instance (new way - recommended)
            api_key: Anthropic API key (old way - for backward compatibility)
            model: Model identifier to use
            system_prompt: Optional system prompt to customize behavior
            steering_mode: Mode for applying steering vectors (BETA_API, SIMULATED, DISABLED)
            default_vectors: Default steering vectors to apply to all responses
            vector_selector: Optional function to dynamically select vectors based on context
        """
        self.name = name

        # Handle backend - either passed directly or created from api_key
        if backend is not None:
            self.backend = backend
        elif api_key is not None:
            # Backward compatibility: create Anthropic backend from api_key
            self.backend = create_backend(
                BackendType.ANTHROPIC,
                api_key=api_key,
                model=model
            )
        else:
            raise ValueError("Either 'backend' or 'api_key' must be provided")

        self.model = model
        self.base_system_prompt = system_prompt or "You are a helpful AI assistant engaging in a conversation."
        self.steering_mode = steering_mode
        self.default_vectors = default_vectors or []
        self.vector_selector = vector_selector
        self.applicator = SteeringVectorApplicator(mode=steering_mode)
        self.conversation_history: List[Dict[str, str]] = []
        self.last_outgoing_vectors: List[SteeringVector] = []
        self.last_incoming_vectors: List[SteeringVector] = []

    def respond(
        self,
        message: str,
        incoming_vectors: Optional[List[SteeringVector]] = None
    ) -> tuple[str, List[SteeringVector]]:
        """
        Generate a response to the given message.

        Args:
            message: The message to respond to
            incoming_vectors: Optional steering vectors from the other agent

        Returns:
            Tuple of (response text, outgoing steering vectors)
        """
        # Store incoming vectors
        self.last_incoming_vectors = incoming_vectors or []

        # Add the message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })

        # Determine which steering vectors to apply
        vectors_to_apply = self.default_vectors.copy()

        # If we have a vector selector function, let it choose/modify vectors
        if self.vector_selector:
            selected = self.vector_selector(message, self.last_incoming_vectors)
            vectors_to_apply.extend(selected)

        # Apply steering vectors to system prompt
        system_prompt_with_vectors = self.applicator.apply_to_system_prompt(
            self.base_system_prompt,
            vectors_to_apply
        )

        # Get response from backend
        response_text = self.backend.generate(
            messages=self.conversation_history,
            system_prompt=system_prompt_with_vectors,
            max_tokens=1024
        )

        # Add to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response_text
        })

        # Store outgoing vectors for next turn
        self.last_outgoing_vectors = vectors_to_apply

        return response_text, vectors_to_apply

    def reset_history(self):
        """Clear the conversation history for this agent."""
        self.conversation_history = []
        self.last_outgoing_vectors = []
        self.last_incoming_vectors = []

    def get_history(self) -> List[Dict[str, str]]:
        """Get the full conversation history."""
        return self.conversation_history.copy()

    def get_vector_history(self) -> Dict[str, List[SteeringVector]]:
        """Get the steering vector history."""
        return {
            "last_outgoing": self.last_outgoing_vectors,
            "last_incoming": self.last_incoming_vectors
        }


# Backward compatibility alias
ClaudeAgent = AIAgent


class ConversationManager:
    """Manages conversations between two AI agents with steering vector support."""

    def __init__(
        self,
        backend: Optional[ModelBackend] = None,
        api_key: Optional[str] = None,  # For backward compatibility
        model: str = "claude-sonnet-4-5-20250929",
        agent_a_name: str = "Agent A",
        agent_b_name: str = "Agent B",
        agent_a_system: Optional[str] = None,
        agent_b_system: Optional[str] = None,
        steering_mode: SteeringMode = SteeringMode.SIMULATED,
        agent_a_vectors: Optional[List[SteeringVector]] = None,
        agent_b_vectors: Optional[List[SteeringVector]] = None,
        agent_a_vector_selector: Optional[Callable[[str, List[SteeringVector]], List[SteeringVector]]] = None,
        agent_b_vector_selector: Optional[Callable[[str, List[SteeringVector]], List[SteeringVector]]] = None,
        show_vectors: bool = True
    ):
        """
        Initialize the conversation manager.

        Args:
            backend: ModelBackend instance to use for both agents (new way - recommended)
            api_key: Anthropic API key (old way - for backward compatibility)
            model: Model identifier to use for both agents
            agent_a_name: Name for the first agent
            agent_b_name: Name for the second agent
            agent_a_system: System prompt for agent A
            agent_b_system: System prompt for agent B
            steering_mode: Mode for steering vectors (BETA_API, SIMULATED, DISABLED)
            agent_a_vectors: Default steering vectors for agent A
            agent_b_vectors: Default steering vectors for agent B
            agent_a_vector_selector: Dynamic vector selector for agent A
            agent_b_vector_selector: Dynamic vector selector for agent B
            show_vectors: Whether to display steering vectors during conversation

        Examples:
            # Using Ollama (free, local)
            backend = create_backend(BackendType.OLLAMA, model="llama3.2")
            manager = ConversationManager(backend=backend)

            # Using Anthropic (paid, backward compatible)
            manager = ConversationManager(api_key="your-key")
        """
        self.agent_a = AIAgent(
            name=agent_a_name,
            backend=backend,
            api_key=api_key,
            model=model,
            system_prompt=agent_a_system,
            steering_mode=steering_mode,
            default_vectors=agent_a_vectors,
            vector_selector=agent_a_vector_selector
        )

        self.agent_b = AIAgent(
            name=agent_b_name,
            backend=backend,
            api_key=api_key,
            model=model,
            system_prompt=agent_b_system,
            steering_mode=steering_mode,
            default_vectors=agent_b_vectors,
            vector_selector=agent_b_vector_selector
        )

        self.steering_mode = steering_mode
        self.show_vectors = show_vectors
        self.full_conversation: List[Dict[str, Any]] = []

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
        if self.steering_mode != SteeringMode.DISABLED:
            print(f"Steering mode: {self.steering_mode.value}")
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
        incoming_vectors: List[SteeringVector] = []

        try:
            while True:
                # Check turn limit
                if max_turns and turn_count >= max_turns:
                    print(f"\n[CONVERSATION ENDED: Reached maximum of {max_turns} turns]")
                    break

                # Get response from current agent (with steering vectors)
                print(f"[{current_agent.name}]")
                response, outgoing_vectors = current_agent.respond(
                    current_message,
                    incoming_vectors
                )
                print(f"{response}\n")

                # Show steering vectors if enabled
                if self.show_vectors and outgoing_vectors and self.steering_mode != SteeringMode.DISABLED:
                    print(f"[Steering Vectors: {', '.join(v.name for v in outgoing_vectors)}]")

                print(f"{'-'*60}\n")

                # Record in full conversation
                self.full_conversation.append({
                    "speaker": current_agent.name,
                    "message": response,
                    "timestamp": datetime.now().isoformat(),
                    "turn": turn_count + 1,
                    "steering_vectors": [v.to_dict() for v in outgoing_vectors] if outgoing_vectors else []
                })

                # Swap agents and pass vectors
                current_message = response
                incoming_vectors = outgoing_vectors
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
