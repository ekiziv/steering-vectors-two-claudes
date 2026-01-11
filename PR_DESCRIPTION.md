# Two AI Conversation App with Steering Vectors + FREE Ollama Support

This PR implements a complete Two AI Conversation application where AI models communicate through both text and steering vectors, with support for both FREE local models (Ollama) and paid cloud API (Anthropic).

## 🎉 Major Features

### ✨ **NEW: 100% FREE Local Models via Ollama**
- No API key required
- No payment needed
- Unlimited conversations
- Complete privacy (runs locally)
- 6 recommended models included

### 🚀 **Steering Vector Communication**
- 18 predefined vectors for rich AI-to-AI communication
- Tone vectors: Analytical, Creative, Formal, Casual
- Emotion vectors: Optimistic, Cautious, Curious, Assertive
- Style vectors: Abstract, Concrete, Philosophical, Pragmatic
- Meta vectors: Agreement, Disagreement, Build On, Redirect, Uncertainty, Confidence

### 🔧 **Flexible Backend System**
- Support for multiple AI providers
- Easy switching between free and paid models
- Backward compatible with existing code

## 📦 What's Included

### Core Infrastructure
- **model_backends.py**: Abstraction layer supporting Ollama and Anthropic
- **steering_vectors.py**: Complete steering vector system with 18 predefined vectors
- **conversation_manager.py**: Enhanced to support multiple backends and vector passing

### Examples
- **example_ollama_free.py**: Demo using FREE local models
- **example_with_steering_vectors.py**: Fixed personality vectors
- **example_dynamic_vectors.py**: Context-aware dynamic vector selection
- **example_meta_communication.py**: Meta-communication demonstrations
- **example_simple.py**: Basic conversation example
- **example_with_prompts.py**: Different personality prompts

### Documentation
- **OLLAMA_SETUP.md**: Complete setup guide for free local models
- **STEERING_VECTORS.md**: Technical deep-dive on steering vectors
- **README.md**: Updated with free and paid options

### Testing
- **test_structure.py**: Basic structure tests
- **test_steering_vectors.py**: Steering vector infrastructure tests (8/8 passing)
- **test_backends.py**: Backend abstraction tests (5/5 passing)

## 🔬 Technical Highlights

### Phase 1: Basic Infrastructure ✅
- Two AI conversation system
- Conversation management and logging
- Interactive CLI with moderator controls

### Phase 2: Steering Vector Infrastructure ✅
- SteeringVector class with serialization
- SteeringVectorApplicator for multiple modes (BETA_API, SIMULATED, DISABLED)
- Vector encoding/decoding for transmission
- Vector passing between agents

### Phase 3: Predefined Vector Library ✅
- 18 ready-to-use steering vectors
- Static and dynamic vector selection
- Meta-communication capabilities

### Phase 4: Multi-Backend Support ✅
- OllamaBackend for FREE local models
- AnthropicBackend for paid cloud API
- Factory pattern for easy backend creation
- Fully backward compatible

## 📊 Testing Status

All tests passing:
- ✅ Basic structure tests (4/4)
- ✅ Steering vector tests (8/8)
- ✅ Backend tests (5/5)

## 🚀 Quick Start

### Option 1: FREE with Ollama
```bash
# Install Ollama from https://ollama.ai
ollama serve
ollama pull llama3.2
python example_ollama_free.py
```

### Option 2: Paid with Anthropic API
```bash
# Add ANTHROPIC_API_KEY to .env
python main.py
```

## 📚 Example Usage

```python
from model_backends import BackendType, create_backend
from conversation_manager import ConversationManager
from steering_vectors import PredefinedVectors, SteeringMode

# FREE Ollama backend
backend = create_backend(BackendType.OLLAMA, model="llama3.2")

# Create conversation with steering vectors
manager = ConversationManager(
    backend=backend,
    agent_a_name="Analytical AI",
    agent_b_name="Creative AI",
    steering_mode=SteeringMode.SIMULATED,
    agent_a_vectors=[PredefinedVectors.ANALYTICAL],
    agent_b_vectors=[PredefinedVectors.CREATIVE],
    show_vectors=True
)

manager.start_conversation(
    initial_message="Let's explore AI!",
    max_turns=10
)
```

## 🔄 Backward Compatibility

All existing code continues to work:
```python
# Old code still works!
manager = ConversationManager(api_key="your-key")
```

## 📖 Documentation

- See [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for detailed Ollama setup
- See [STEERING_VECTORS.md](STEERING_VECTORS.md) for technical details
- See [README.md](README.md) for complete usage guide

## 🎯 Future Phases

- **Phase 4**: Learned Communication - Agents learn which vectors to use
- **Phase 5**: Research Applications - Study communication patterns

## ✅ Ready to Merge

- All tests passing
- Documentation complete
- Backward compatible
- Multiple usage examples
- Comprehensive setup guides

This implementation enables rich AI-to-AI communication with a "second channel" beyond text, using completely free local models or paid cloud APIs as needed.
