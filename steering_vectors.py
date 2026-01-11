"""
Steering Vector Infrastructure for Two Claudes Conversation

This module provides abstractions for working with steering vectors (persona vectors)
to enable richer AI-to-AI communication. It supports:
- Anthropic Beta Steering API (when available)
- Simulated steering vectors for testing
- Predefined persona vectors for common traits

Based on Anthropic's persona vectors research:
https://www.anthropic.com/research/persona-vectors
"""

from typing import Dict, List, Optional, Any, Literal
from dataclasses import dataclass, asdict
import json
from enum import Enum


class SteeringMode(Enum):
    """Modes for applying steering vectors."""
    BETA_API = "beta_api"  # Use Anthropic Beta Steering API (requires access)
    SIMULATED = "simulated"  # Simulate via enhanced system prompts
    DISABLED = "disabled"  # No steering vectors


@dataclass
class SteeringVector:
    """
    Represents a steering vector (persona vector) that can modify model behavior.

    Attributes:
        name: Human-readable name (e.g., "analytical", "empathetic")
        vector_type: Category of the steering (tone, emotion, style, meta)
        strength: Coefficient for vector application (typically 0.5 to 5.0)
        layer: Target layer for application (if using Beta API)
        description: What this vector does
        metadata: Additional context about the vector
    """
    name: str
    vector_type: Literal["tone", "emotion", "style", "meta", "custom"]
    strength: float = 1.0
    layer: Optional[int] = None
    description: str = ""
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SteeringVector':
        """Create from dictionary."""
        return cls(**data)

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> 'SteeringVector':
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(json_str))


class PredefinedVectors:
    """
    Library of predefined steering vectors for common communication patterns.

    These vectors define different "personas" or communication styles that can
    be applied during AI-to-AI conversation. In simulated mode, they're translated
    to system prompt modifications. In Beta API mode, they'd map to actual vectors.
    """

    # Tone vectors
    ANALYTICAL = SteeringVector(
        name="analytical",
        vector_type="tone",
        strength=1.5,
        layer=20,
        description="Emphasizes logical reasoning, data, and systematic analysis"
    )

    CREATIVE = SteeringVector(
        name="creative",
        vector_type="tone",
        strength=1.5,
        layer=20,
        description="Emphasizes imagination, novel connections, and lateral thinking"
    )

    FORMAL = SteeringVector(
        name="formal",
        vector_type="tone",
        strength=1.2,
        layer=18,
        description="Emphasizes professional, structured, academic communication"
    )

    CASUAL = SteeringVector(
        name="casual",
        vector_type="tone",
        strength=1.2,
        layer=18,
        description="Emphasizes relaxed, conversational, accessible communication"
    )

    # Perspective vectors
    OPTIMISTIC = SteeringVector(
        name="optimistic",
        vector_type="emotion",
        strength=1.3,
        layer=22,
        description="Emphasizes positive possibilities and opportunities"
    )

    CAUTIOUS = SteeringVector(
        name="cautious",
        vector_type="emotion",
        strength=1.3,
        layer=22,
        description="Emphasizes risks, challenges, and careful consideration"
    )

    CURIOUS = SteeringVector(
        name="curious",
        vector_type="emotion",
        strength=1.4,
        layer=21,
        description="Emphasizes questions, exploration, and open-ended inquiry"
    )

    ASSERTIVE = SteeringVector(
        name="assertive",
        vector_type="emotion",
        strength=1.3,
        layer=21,
        description="Emphasizes confidence, decisiveness, and clear positions"
    )

    # Cognitive style vectors
    ABSTRACT = SteeringVector(
        name="abstract",
        vector_type="style",
        strength=1.5,
        layer=24,
        description="Emphasizes high-level concepts, patterns, and principles"
    )

    CONCRETE = SteeringVector(
        name="concrete",
        vector_type="style",
        strength=1.5,
        layer=24,
        description="Emphasizes specific examples, details, and practical applications"
    )

    PHILOSOPHICAL = SteeringVector(
        name="philosophical",
        vector_type="style",
        strength=1.4,
        layer=23,
        description="Emphasizes fundamental questions, ethics, and deeper meaning"
    )

    PRAGMATIC = SteeringVector(
        name="pragmatic",
        vector_type="style",
        strength=1.4,
        layer=23,
        description="Emphasizes practical solutions, efficiency, and actionable steps"
    )

    # Meta-communication vectors
    AGREEMENT = SteeringVector(
        name="agreement",
        vector_type="meta",
        strength=1.0,
        layer=19,
        description="Signal agreement with the other agent's points"
    )

    DISAGREEMENT = SteeringVector(
        name="disagreement",
        vector_type="meta",
        strength=1.0,
        layer=19,
        description="Signal respectful disagreement with the other agent's points"
    )

    BUILD_ON = SteeringVector(
        name="build_on",
        vector_type="meta",
        strength=1.2,
        layer=20,
        description="Signal intent to build upon and extend the other agent's ideas"
    )

    REDIRECT = SteeringVector(
        name="redirect",
        vector_type="meta",
        strength=1.2,
        layer=20,
        description="Signal intent to redirect conversation to a new angle"
    )

    UNCERTAINTY = SteeringVector(
        name="uncertainty",
        vector_type="meta",
        strength=1.1,
        layer=21,
        description="Signal uncertainty or need for clarification"
    )

    CONFIDENCE = SteeringVector(
        name="confidence",
        vector_type="meta",
        strength=1.1,
        layer=21,
        description="Signal high confidence in the response"
    )

    @classmethod
    def get_all(cls) -> Dict[str, SteeringVector]:
        """Get dictionary of all predefined vectors."""
        return {
            name: getattr(cls, name)
            for name in dir(cls)
            if isinstance(getattr(cls, name), SteeringVector)
        }

    @classmethod
    def get_by_type(cls, vector_type: str) -> Dict[str, SteeringVector]:
        """Get all vectors of a specific type."""
        all_vectors = cls.get_all()
        return {
            name: vector
            for name, vector in all_vectors.items()
            if vector.vector_type == vector_type
        }


class SteeringVectorApplicator:
    """
    Handles application of steering vectors to API calls.

    Supports multiple modes:
    - Beta API: Uses Anthropic's Beta Steering API (when available)
    - Simulated: Translates vectors into system prompt modifications
    - Disabled: No steering applied
    """

    def __init__(self, mode: SteeringMode = SteeringMode.SIMULATED):
        self.mode = mode

    def apply_to_system_prompt(
        self,
        base_prompt: str,
        vectors: List[SteeringVector]
    ) -> str:
        """
        Apply steering vectors by modifying the system prompt.

        This is used in SIMULATED mode to approximate steering vector effects
        through prompt engineering.

        Args:
            base_prompt: The original system prompt
            vectors: List of steering vectors to apply

        Returns:
            Modified system prompt
        """
        if not vectors or self.mode == SteeringMode.DISABLED:
            return base_prompt

        # Build steering instructions
        steering_instructions = []

        for vector in vectors:
            if vector.strength > 0:
                strength_desc = self._strength_to_description(vector.strength)
                steering_instructions.append(
                    f"- {strength_desc} {vector.description}"
                )

        if not steering_instructions:
            return base_prompt

        # Append to system prompt
        modified_prompt = f"""{base_prompt}

COMMUNICATION STYLE GUIDANCE:
{chr(10).join(steering_instructions)}

Apply these style guidelines naturally in your response."""

        return modified_prompt

    def _strength_to_description(self, strength: float) -> str:
        """Convert numeric strength to descriptive text."""
        if strength >= 2.0:
            return "Strongly"
        elif strength >= 1.5:
            return "Significantly"
        elif strength >= 1.0:
            return "Moderately"
        elif strength >= 0.5:
            return "Slightly"
        else:
            return "Minimally"

    def apply_to_api_params(
        self,
        api_params: Dict[str, Any],
        vectors: List[SteeringVector],
        beta_api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Apply steering vectors to API parameters.

        Args:
            api_params: Base API parameters
            vectors: List of steering vectors to apply
            beta_api_key: Beta API access key (if available)

        Returns:
            Modified API parameters
        """
        if self.mode == SteeringMode.DISABLED or not vectors:
            return api_params

        if self.mode == SteeringMode.SIMULATED:
            # Modify system prompt
            api_params["system"] = self.apply_to_system_prompt(
                api_params.get("system", ""),
                vectors
            )

        elif self.mode == SteeringMode.BETA_API:
            # TODO: Apply via Beta Steering API when available
            # This would involve adding beta headers and steering parameters
            # based on Anthropic's Beta API documentation

            if not beta_api_key:
                raise ValueError("Beta API key required for BETA_API mode")

            # Placeholder for future Beta API integration
            api_params["extra_headers"] = api_params.get("extra_headers", {})
            api_params["extra_headers"]["anthropic-beta"] = "steering-2025-08-01"

            # Add steering vector specifications
            # Format TBD based on actual Beta API documentation
            api_params["steering"] = {
                "vectors": [
                    {
                        "name": v.name,
                        "strength": v.strength,
                        "layer": v.layer or 20  # Default layer
                    }
                    for v in vectors
                ]
            }

        return api_params

    def encode_vectors_for_message(
        self,
        vectors: List[SteeringVector]
    ) -> str:
        """
        Encode steering vectors into a format that can be transmitted
        between agents.

        Args:
            vectors: List of steering vectors

        Returns:
            JSON-encoded string representation
        """
        return json.dumps([v.to_dict() for v in vectors], indent=2)

    def decode_vectors_from_message(
        self,
        encoded: str
    ) -> List[SteeringVector]:
        """
        Decode steering vectors from a transmitted message.

        Args:
            encoded: JSON-encoded steering vectors

        Returns:
            List of SteeringVector objects
        """
        try:
            vector_dicts = json.loads(encoded)
            return [SteeringVector.from_dict(v) for v in vector_dicts]
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            print(f"Warning: Failed to decode steering vectors: {e}")
            return []


def create_vector_combination(
    *vectors: SteeringVector,
    normalize: bool = False
) -> List[SteeringVector]:
    """
    Combine multiple steering vectors.

    Args:
        *vectors: Variable number of SteeringVector objects
        normalize: Whether to normalize strengths (average them)

    Returns:
        List of vectors (potentially with adjusted strengths)
    """
    if not vectors:
        return []

    result = list(vectors)

    if normalize and len(vectors) > 1:
        # Normalize strengths to prevent over-steering
        avg_strength = sum(v.strength for v in vectors) / len(vectors)
        scaling_factor = 1.0 / (avg_strength / 1.5)  # Target average ~1.5

        result = [
            SteeringVector(
                name=v.name,
                vector_type=v.vector_type,
                strength=v.strength * scaling_factor,
                layer=v.layer,
                description=v.description,
                metadata=v.metadata
            )
            for v in vectors
        ]

    return result
