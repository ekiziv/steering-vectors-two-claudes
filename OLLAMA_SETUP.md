# Ollama Setup Guide - Free Local AI Models

This guide shows you how to run the Two AI Conversation app **completely free** using local models via Ollama. No API keys, no payment required!

## Why Use Ollama?

- ✅ **100% Free** - No API costs whatsoever
- ✅ **Private** - Everything runs locally on your machine
- ✅ **Fast** - No network latency
- ✅ **Unlimited** - No rate limits or quotas
- ✅ **Easy** - Simple setup process

## Step 1: Install Ollama

### macOS
```bash
# Download and install from website
open https://ollama.ai
# Or use Homebrew
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows
Download the installer from: https://ollama.ai

## Step 2: Start Ollama

```bash
ollama serve
```

Keep this terminal open. Ollama runs as a local server on port 11434.

## Step 3: Pull a Model

Open a new terminal and download a model:

```bash
# Recommended for most users (3B parameters, 2GB download)
ollama pull llama3.2

# Alternative models:
ollama pull llama3.2:1b      # Smaller, faster (1.3GB)
ollama pull mistral          # High quality (4.1GB)
ollama pull llama3.1         # More capable (4.7GB)
ollama pull qwen2.5          # Strong reasoning (4.7GB)
```

**Tip**: Start with `llama3.2` - it's fast, capable, and only 2GB.

## Step 4: Run the Example

```bash
# In the project directory
python example_ollama_free.py
```

That's it! The two AIs will start conversing using your local model.

## Available Models

Here are recommended models with their characteristics:

| Model | Size | Download | Best For |
|-------|------|----------|----------|
| `llama3.2` | 3B | 2GB | General use, good balance |
| `llama3.2:1b` | 1B | 1.3GB | Testing, very fast |
| `llama3.1` | 8B | 4.7GB | Better quality responses |
| `mistral` | 7B | 4.1GB | Strong reasoning |
| `qwen2.5` | 7B | 4.7GB | General capabilities |
| `phi3.5` | 3.8B | 2.2GB | Compact but capable |

### Choosing a Model

**For Testing / Slower Machines:**
- Use `llama3.2:1b` (1.3GB) - Very fast

**For Daily Use:**
- Use `llama3.2` (2GB) - Great balance

**For Best Quality:**
- Use `llama3.1` or `mistral` (4-5GB) - Higher quality

**System Requirements:**
- Minimum: 8GB RAM
- Recommended: 16GB RAM
- Disk Space: 2-10GB per model

## Usage Examples

### Basic Conversation (Free)

```python
from conversation_manager import ConversationManager
from model_backends import BackendType, create_backend

# Create Ollama backend
backend = create_backend(
    BackendType.OLLAMA,
    model="llama3.2"
)

# Create manager
manager = ConversationManager(backend=backend)

# Start conversation
manager.start_conversation(
    initial_message="Hello! Let's discuss AI.",
    max_turns=10
)
```

### With Steering Vectors (Free)

```python
from conversation_manager import ConversationManager
from model_backends import BackendType, create_backend
from steering_vectors import PredefinedVectors, SteeringMode

# Create backend
backend = create_backend(BackendType.OLLAMA, model="llama3.2")

# Create manager with steering vectors
manager = ConversationManager(
    backend=backend,
    agent_a_name="Analytical AI",
    agent_b_name="Creative AI",
    steering_mode=SteeringMode.SIMULATED,
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

manager.start_conversation(
    initial_message="Let's explore the future of AI.",
    max_turns=8
)
```

## Troubleshooting

### "Ollama is not running"

Make sure you started the Ollama server:
```bash
ollama serve
```

### "Model not found"

Pull the model first:
```bash
ollama pull llama3.2
```

### List installed models

```bash
ollama list
```

### Remove a model

```bash
ollama rm llama3.2
```

### Connection issues

Check if Ollama is listening on the right port:
```bash
curl http://localhost:11434/api/tags
```

### Performance is slow

Try a smaller model:
```bash
ollama pull llama3.2:1b
# Then change model="llama3.2:1b" in your script
```

Or ensure Ollama is using your GPU (if available):
- Ollama automatically uses GPU if CUDA/Metal/ROCm is available
- Check Ollama startup logs for "CUDA" or "Metal" mentions

## Comparing Ollama vs. Anthropic API

| Feature | Ollama (Free) | Anthropic API (Paid) |
|---------|---------------|---------------------|
| Cost | $0 | ~$3-15 per million tokens |
| Setup | Install locally | API key only |
| Speed | Fast (local) | Variable (network) |
| Privacy | 100% private | Sent to cloud |
| Rate Limits | None | Yes (tier-based) |
| Quality | Good | Excellent |
| Model Choice | Open-source models | Claude 3.5/4.5 |

**Recommendation**: Start with Ollama for free experimentation, switch to Anthropic API if you need Claude's specific capabilities.

## Advanced Configuration

### Custom Ollama URL

If running Ollama on a different machine or port:

```python
backend = create_backend(
    BackendType.OLLAMA,
    model="llama3.2",
    base_url="http://192.168.1.100:11434"
)
```

### Environment Variables

Create a `.env` file:
```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

Then use in code:
```python
import os
from dotenv import load_dotenv

load_dotenv()

backend = create_backend(
    BackendType.OLLAMA,
    model=os.getenv("OLLAMA_MODEL", "llama3.2"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)
```

## Next Steps

Once you have Ollama working:

1. **Try different models**: Experiment with various models to find your favorite
2. **Explore steering vectors**: Run `example_with_steering_vectors.py`
3. **Dynamic vectors**: Try `example_dynamic_vectors.py`
4. **Meta-communication**: Run `example_meta_communication.py`
5. **Build your own**: Create custom conversation scenarios

## Resources

- **Ollama Website**: https://ollama.ai
- **Ollama Models**: https://ollama.ai/library
- **Ollama GitHub**: https://github.com/ollama/ollama
- **Model Cards**: Research specific models on Hugging Face

## Getting Help

If you encounter issues:

1. Check Ollama logs: Look at the terminal where `ollama serve` is running
2. Verify model: `ollama list`
3. Test manually: `ollama run llama3.2 "Hello"`
4. Check this project's issues: [GitHub Issues](https://github.com/yourusername/repo/issues)

Happy conversing! 🚀
