# Design Document: Minimal Two-AI Conversation with Real Steering Vectors

## Goal
Create a minimal Python app where two open-source LLMs (via Ollama or direct transformers) converse and pass **actual steering vectors** between each other - not simulated via prompts.

## Problem Statement
Current implementation:
- ❌ Simulates steering vectors via system prompts (not real)
- ❌ Supports Anthropic API (not needed)
- ❌ Too many features (18 vectors, multiple modes, examples)
- ❌ Can't actually pass vectors with Ollama's chat API

**We need**: Minimal code that uses REAL steering vectors with open-source models.

---

## Research: Open-Source Steering Vector Libraries

### Option 1: `steering-vectors` Package ⭐ RECOMMENDED
- **Repo**: https://github.com/steering-vectors/steering-vectors
- **PyPI**: https://pypi.org/project/steering-vectors/
- **Docs**: https://steering-vectors.github.io/steering-vectors/
- **Supports**: LLaMA, Gemma, Mistral, Pythia, GPT models via HuggingFace
- **How it works**: Directly modifies model activations at specific layers
- **Status**: Actively maintained, comprehensive docs

### Option 2: `llm_steer`
- **Repo**: https://github.com/Mihaiii/llm_steer
- **Supports**: LLaMA, Mistral, Phi, StableLM
- **Includes**: Google Colab demo
- **Integration**: Works with HuggingFace transformers

### Option 3: Contrastive Activation Addition (CAA)
- **Repo**: https://github.com/nrimsky/CAA
- **Paper**: https://arxiv.org/abs/2312.06681
- **Method**: Compute steering vectors by averaging activation differences
- **Focus**: LLaMA 2

### Option 4: Dialz
- **Paper**: https://aclanthology.org/2025.acl-demo.35.pdf
- **Features**: Visualization capabilities
- **Tested on**: LLaMA 3.1 8B Instruct

**Decision**: Use `steering-vectors` - most mature, best docs, actively maintained.

---

## Architecture Design

### High-Level Flow

```
Agent A: Generate response with steering vector V1
    ↓
    Vector V1 extracted from model activations
    ↓
Agent B: Receives message + vector V1
    ↓
    Vector V1 applied to Agent B's model during generation
    ↓
Agent B: Generates response with steering vector V2
    ↓
    (repeat)
```

### Technical Approach

**NOT using Ollama** - Ollama's chat API doesn't expose model internals.

**Instead**: Use HuggingFace transformers directly with `steering-vectors` library.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from steering_vectors import train_steering_vector, apply_steering_vector

# Load model once
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B")

# Agent A generates with vector V1
output_a, vector_a = generate_with_vector(model, prompt, vector=None)

# Agent B generates with Agent A's vector applied
output_b, vector_b = generate_with_vector(model, output_a, vector=vector_a)
```

---

## What to Keep

### Core Files (Minimal)
1. **`minimal_conversation.py`** - Main script (single file, ~150 lines)
2. **`requirements.txt`** - Dependencies
3. **`README.md`** - Setup instructions

### Dependencies
```
torch>=2.0.0
transformers>=4.35.0
steering-vectors>=0.12.0
```

### Features
- Two AI agents using same model
- Extract steering vectors from Agent A's generation
- Apply vectors to Agent B's generation
- Simple conversation loop
- Save conversation to JSON

---

## What to Remove

### Delete These Files
- ❌ `model_backends.py` - Over-engineered backend abstraction
- ❌ `conversation_manager.py` - Complex manager with too many features
- ❌ `steering_vectors.py` - Simulated steering (not real)
- ❌ All Anthropic API code
- ❌ All example files (6 files)
- ❌ `test_*.py` files
- ❌ `main.py` (interactive CLI)
- ❌ `OLLAMA_SETUP.md`
- ❌ `STEERING_VECTORS.md` (outdated)

### Remove These Concepts
- ❌ Multiple backends (Ollama, Anthropic)
- ❌ Simulated steering mode
- ❌ 18 predefined vectors
- ❌ Dynamic vector selection
- ❌ Meta-communication
- ❌ Vector strength/layer configuration
- ❌ Interactive CLI

---

## Minimal Implementation Plan

### File Structure
```
steering-vectors-two-claudes/
├── minimal_conversation.py    # Single file implementation
├── requirements.txt
└── README.md
```

### Core Components

#### 1. Model Wrapper
```python
class LLMAgent:
    def __init__(self, name, model, tokenizer):
        self.name = name
        self.model = model
        self.tokenizer = tokenizer

    def generate(self, prompt, steering_vector=None):
        """Generate response, optionally applying steering vector."""
        # Use steering-vectors library to apply vector
        # Return (response_text, extracted_vector)
        pass
```

#### 2. Conversation Loop
```python
def run_conversation(agent_a, agent_b, initial_message, max_turns=5):
    """Run conversation with vector passing."""
    message = initial_message
    vector = None

    for turn in range(max_turns):
        # Agent A responds
        response_a, vector_a = agent_a.generate(message, steering_vector=vector)
        print(f"{agent_a.name}: {response_a}")

        # Agent B responds with A's vector
        response_b, vector_b = agent_b.generate(response_a, steering_vector=vector_a)
        print(f"{agent_b.name}: {response_b}")

        message = response_b
        vector = vector_b
```

#### 3. Training Vectors (Optional)
```python
def train_vector(model, tokenizer, positive_prompts, negative_prompts):
    """Train a steering vector from example prompts."""
    # Use steering-vectors library
    pass
```

---

## Implementation Questions

### Q1: Which Model?
**Options**:
- LLaMA 3.2 1B (smallest, fastest)
- LLaMA 3.2 3B (better quality)
- Mistral 7B (highest quality)

**Recommendation**: LLaMA 3.2 3B - good balance

### Q2: Where to Get Steering Vectors?
**Two approaches**:

A. **Pre-compute vectors** (simpler)
```python
# Train once, save to disk
vector_analytical = train_vector(
    positive=["Think analytically...", "Use logic..."],
    negative=["Think creatively...", "Use intuition..."]
)
vector_analytical.save("vectors/analytical.pt")
```

B. **Extract from each generation** (dynamic)
```python
# Extract vector from Agent A's generation process
_, vector = agent_a.generate(message)
# Pass to Agent B
agent_b.generate(response, steering_vector=vector)
```

**Recommendation**: Start with approach B (dynamic extraction)

### Q3: Which Layer for Steering?
**Research suggests**: Middle layers (15-20 for 32-layer models)

**Approach**: Make it configurable, default to layer 16

---

## Success Criteria

A successful minimal implementation:
1. ✅ Uses REAL steering vectors (not prompt simulation)
2. ✅ Single file under 200 lines
3. ✅ Works with open-source models (no API keys)
4. ✅ Vectors actually affect behavior
5. ✅ Clear demonstration of vector passing
6. ✅ No unnecessary abstractions

---

## Next Steps

1. **Delete old code** - Remove all files listed above
2. **Install dependencies** - `pip install torch transformers steering-vectors`
3. **Download model** - LLaMA 3.2 3B via HuggingFace
4. **Implement minimal_conversation.py** - Single file
5. **Test** - Verify vectors affect behavior
6. **Document** - Simple README with setup

---

## References

- Steering Vectors Library: https://github.com/steering-vectors/steering-vectors
- Documentation: https://steering-vectors.github.io/steering-vectors/
- LLM Steer: https://github.com/Mihaiii/llm_steer
- CAA Paper: https://arxiv.org/abs/2312.06681
- Dialz Toolkit: https://aclanthology.org/2025.acl-demo.35.pdf
- Medium Article: https://evoailabs.medium.com/steering-llms-like-a-neuroscientist-changing-ai-behavior-without-fine-tuning-6d8a6168892c

---

## Estimated Complexity

- **Lines of Code**: ~150 (single file)
- **Dependencies**: 3 (torch, transformers, steering-vectors)
- **Files**: 3 (main script, requirements, README)
- **Concepts**: 2 (generate with vector, pass vector between agents)

This is a **10x simplification** from current codebase.
