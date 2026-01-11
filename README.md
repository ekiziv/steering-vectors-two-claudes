# Two Claudes Conversation App

An interactive Python application where two Claude AI models converse with each other, with infrastructure for future steering vector integration.

Implementing this idea: https://x.com/nostalgebraist/status/2006179998885945541

## Overview

This project enables two separate Claude AI instances to have conversations with each other. The human user acts as the moderator, starting conversations and optionally stopping them. The infrastructure is designed to eventually support **steering vectors** - techniques for modifying model behavior by intervening in the activation space.

## Features

- **Two Claude Instances**: Run two separate Claude models that converse with each other
- **Interactive Moderation**: Start conversations with custom prompts and stop at any time (Ctrl+C)
- **Conversation History**: Automatically saves all conversations to JSON files
- **Flexible Configuration**: Support for different models, system prompts, and turn limits
- **Steering Vector Ready**: Infrastructure in place for future steering vector implementation
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

3. Set up your Anthropic API key:
```bash
cp .env.example .env
# Edit .env and add your API key
```

## Quick Start

### Interactive Mode

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

## Project Structure

```
steering-vectors-two-claudes/
├── conversation_manager.py    # Core conversation logic
├── main.py                    # Interactive CLI
├── example_simple.py          # Simple usage example
├── example_with_prompts.py    # Example with different personalities
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── STEERING_VECTORS.md       # Documentation on steering vectors
└── conversation_history/     # Saved conversations (auto-created)
```

## Architecture

### ClaudeAgent Class
Represents a single Claude AI instance with:
- Conversation history management
- API interaction handling
- Steering vector support (infrastructure ready)

### ConversationManager Class
Orchestrates conversations between two agents:
- Turn-based conversation flow
- Moderator controls (start/stop)
- Conversation persistence
- Agent coordination

## Future: Steering Vectors

The codebase includes infrastructure for **steering vectors** - a technique for modifying AI model behavior by intervening in the activation space. See `STEERING_VECTORS.md` for details on:
- What steering vectors are
- How they enable AI-to-AI communication
- Implementation plans for this project

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
