# Two AI Conversation App with Steering Vectors

An interactive Python application where two AI models converse with each other using **steering vectors** for richer AI-to-AI communication.

**✨ NEW: Now supports 100% FREE local models via Ollama!** No API key, no payment, no limits.

Implementing this idea: https://x.com/nostalgebraist/status/2006179998885945541

## Overview

This project enables two AI instances to have conversations with each other using **steering vectors** - a technique for modifying AI behavior by intervening in the activation space. The human user acts as the moderator, starting conversations and optionally stopping them.

**Steering vectors are now fully implemented!** The AIs can communicate not just through text, but also through "vectors" that convey tone, intent, emotion, and meta-information.

## Features

- **🆓 FREE Local Models**: Run completely free using Ollama (no API costs!)
- **💳 Cloud Models**: Or use Anthropic's Claude API (paid)
- **Two AI Instances**: Two separate AI models conversing with each other
- **Steering Vector Communication** 🚀: Agents pass steering vectors to each other, enabling richer communication
  - 18 predefined vectors (analytical, creative, optimistic, cautious, etc.)
  - Dynamic vector selection based on context
  - Meta-communication (agreement, uncertainty, confidence signals)
- **Multiple Steering Modes**:
  - SIMULATED (via enhanced prompts - works now)
  - BETA_API (ready for Anthropic's Beta Steering API)
  - DISABLED (traditional text-only)
- **Interactive Moderation**: Start conversations with custom prompts and stop at any time (Ctrl+C)
- **Conversation History**: Automatically saves all conversations with vector data to JSON files
- **Flexible Configuration**: Support for different models, system prompts, and turn limits
- **Multiple Usage Modes**: Interactive CLI or programmatic Python usage

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd steering-vectors-two-claudes
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **Choose your model backend:**

### Option A: FREE Local Models (Recommended for Getting Started)

**No API key needed!**

1. Install Ollama: https://ollama.ai
2. Start Ollama: `ollama serve`
3. Pull a model: `ollama pull llama3.2`
4. Run the example: `python example_ollama_free.py`

See [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for detailed instructions.

### Option B: Anthropic API (Paid, Cloud-based)

1. Get an API key from: https://console.anthropic.com
2. Set up your API key:
```bash
cp .env.example .env
# Edit .env and add your API key
```

## Quick Start

### FREE Local Models (Ollama)

```bash
# Make sure Ollama is running
ollama serve

# Pull a model (one-time)
ollama pull llama3.2

# Run the example
python example_ollama_free.py
```

That's it! No payment, no API key, fully private and local.

### Anthropic API (Paid)

Run the interactive CLI:
```bash
python main.py
```

Follow the prompts to:
1. Enter an initial message to start the conversation
2. Set a maximum number of turns (or unlimited)
3. Choose a model (Sonnet, Opus, or Haiku)
4. Watch the conversation unfold!

Press `Ctrl+C` at any time to stop the conversation as the moderator.

### Simple Example

Run a quick pre-configured conversation:
```bash
python example_simple.py
```

### Example with Different Personalities

See how different system prompts affect the conversation:
```bash
python example_with_prompts.py
```

### Steering Vector Examples 🚀 NEW

**Steering vectors** enable richer AI-to-AI communication beyond just text!

Run conversations with steering vectors (simulated mode):
```bash
# Fixed steering vectors (analytical vs. creative personalities)
python example_with_steering_vectors.py

# Dynamic steering vectors (agents adapt based on context)
python example_dynamic_vectors.py

# Meta-communication (agreement, uncertainty, confidence signals)
python example_meta_communication.py
```

These examples demonstrate how steering vectors create a "second channel" of communication, allowing the Claudes to convey tone, intent, and meta-information alongside their text messages.

## Programmatic Usage

```python
from dotenv import load_dotenv
import os
from conversation_manager import ConversationManager

load_dotenv()

# Create conversation manager
manager = ConversationManager(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-4-5-20250929",
    agent_a_name="Claude A",
    agent_b_name="Claude B"
)

# Start conversation
manager.start_conversation(
    initial_message="Hello! Let's discuss quantum computing.",
    max_turns=10,
    save_to_file=True
)
```

### With Steering Vectors

```python
from dotenv import load_dotenv
import os
from conversation_manager import ConversationManager
from steering_vectors import PredefinedVectors, SteeringMode

load_dotenv()

# Create manager with steering vectors
manager = ConversationManager(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-4-5-20250929",
    agent_a_name="Analytical Claude",
    agent_b_name="Creative Claude",
    steering_mode=SteeringMode.SIMULATED,  # or BETA_API when available
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

# Start conversation with vector communication
manager.start_conversation(
    initial_message="Let's explore the future of AI.",
    max_turns=10,
    save_to_file=True
)
```

## Project Structure

```
steering-vectors-two-claudes/
├── conversation_manager.py          # Core conversation logic
├── steering_vectors.py              # Steering vector infrastructure
├── main.py                          # Interactive CLI
├── example_simple.py                # Simple usage example
├── example_with_prompts.py          # Example with different personalities
├── example_with_steering_vectors.py # Steering vectors example
├── example_dynamic_vectors.py       # Dynamic vector selection example
├── example_meta_communication.py    # Meta-communication example
├── test_structure.py                # Basic structure tests
├── test_steering_vectors.py         # Steering vector tests
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
├── STEERING_VECTORS.md              # Documentation on steering vectors
└── conversation_history/            # Saved conversations (auto-created)
```

## Architecture

### ClaudeAgent Class
Represents a single Claude AI instance with:
- Conversation history management
- API interaction handling
- **Steering vector application and tracking**
- Dynamic vector selection via callback functions
- Multiple steering modes (BETA_API, SIMULATED, DISABLED)

### ConversationManager Class
Orchestrates conversations between two agents:
- Turn-based conversation flow with vector passing
- Moderator controls (start/stop)
- Conversation persistence with vector data
- Agent coordination
- Vector visualization during conversations

### Steering Vector System
Complete infrastructure for steering vector communication:
- **SteeringVector**: Data structure for vectors (name, type, strength, layer)
- **PredefinedVectors**: Library of 18 ready-to-use vectors
- **SteeringVectorApplicator**: Applies vectors via prompts (SIMULATED) or API (BETA_API)
- **Vector passing**: Agents receive vectors from the other agent and can respond to them
- **Dynamic selection**: Callback functions for context-aware vector choice

## Steering Vectors: Now Implemented! 🚀

**Steering vectors** are now fully implemented in simulated mode! This technique enables AI models to communicate not just through text, but also through "vectors" that modify behavior and convey implicit information.

See `STEERING_VECTORS.md` for comprehensive technical details on:
- What steering vectors are and how they work
- AI-to-AI communication via steering vectors
- Implementation status (Phases 1-3 complete!)
- Future plans (learned communication, research applications)
- How to get Anthropic Beta Steering API access

## Models Available

- **Claude Sonnet 4.5** (default): Balanced performance and speed
- **Claude Opus 4.5**: Most capable, higher cost
- **Claude Haiku 3.5**: Faster, lower cost

## Conversation History

All conversations are automatically saved to `conversation_history/` as timestamped JSON files. Each entry includes:
- Speaker name
- Message content
- Timestamp
- Turn number

## Moderator Controls

As the moderator, you can:
- Start conversations with custom initial messages
- Set maximum turn limits
- Stop conversations at any time with `Ctrl+C`
- Review saved conversation histories

## Contributing

Contributions welcome! Especially interested in:
- Steering vector implementation
- Advanced conversation patterns
- Analysis tools for conversation dynamics
- UI improvements

## License

MIT License
