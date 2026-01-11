# Steering Vectors: Technical Overview

## What Are Steering Vectors?

**Steering vectors** are a technique for modifying the behavior of large language models (LLMs) by intervening directly in their internal activation space. Rather than changing the model's weights or using different prompts, steering vectors add or subtract specific directions in the model's hidden states to influence its outputs.

### Key Concepts

1. **Activation Space**: The high-dimensional vector space where a model represents concepts internally
2. **Steering Vector**: A direction in this space that corresponds to a particular behavioral trait or concept
3. **Intervention**: Adding or subtracting the steering vector from the model's activations at specific layers

## How They Work

```
Normal Inference:
Input → [Layer 1] → [Layer 2] → ... → [Layer N] → Output

With Steering Vector:
Input → [Layer 1] → [Layer 2 + α·v] → ... → [Layer N] → Output
                     ↑
                steering vector v with strength α
```

## Advantages Over Traditional Prompting

1. **More Precise Control**: Direct manipulation of internal representations
2. **Composable**: Multiple steering vectors can be combined
3. **Efficient**: No need to add lengthy prompts or examples
4. **Subtle Modifications**: Can create nuanced behavioral changes

## AI-to-AI Communication via Steering Vectors

The novel idea this project aims to implement: **Two AI models communicating by passing steering vectors to each other**.

### Traditional AI Communication
```
AI A generates text → AI B reads text → AI B responds
```

### Steering Vector Communication
```
AI A generates:
  - Text message
  - Steering vector (encoding intent, emotion, emphasis, etc.)

AI B receives:
  - Text message (explicit)
  - Steering vector (implicit communication channel)
  - Applies steering vector to its own processing

AI B responds with its own text + steering vector
```

### Potential Benefits

1. **Richer Communication**: Beyond just text, models can communicate implicit context
2. **Efficient Information Transfer**: Some concepts may be easier to encode as vectors than text
3. **Novel Interaction Patterns**: Models might develop their own "language" in vector space
4. **Emotional/Tonal Channels**: Steering vectors could convey tone, confidence, uncertainty
5. **Meta-Communication**: Information about how to interpret the text message

## Implementation Plans

### Phase 1: Current Status ✅
- Basic two-Claude conversation infrastructure
- System prompt differentiation
- Conversation management and logging
- Steering vector parameter placeholders in code

### Phase 2: Steering Vector Infrastructure 🔄
- Research Anthropic API steering vector support
- Implement steering vector extraction from responses
- Implement steering vector application to inputs
- Create steering vector encoding/decoding utilities

### Phase 3: Manual Steering Vectors 📋
- Create predefined steering vectors for different "tones":
  - Analytical vs. Creative
  - Optimistic vs. Cautious
  - Abstract vs. Concrete
  - Questioning vs. Assertive
- Allow agents to select which vectors to apply
- Test impact on conversation dynamics

### Phase 4: Learned Communication 🎯
- Experiment with agents learning which steering vectors to use
- Analyze patterns in vector usage
- Investigate emergent communication strategies
- Study how vectors affect the other agent's responses

### Phase 5: Research Applications 🔬
- Compare text-only vs. text+vector communication efficiency
- Study whether models develop conventions in vector space
- Investigate if steering vectors enable more nuanced collaboration
- Publish findings and open-source learnings

## Technical Challenges

1. **API Availability**: Steering vectors may not be exposed in the Anthropic API yet
2. **Vector Discovery**: Finding meaningful steering vectors requires research
3. **Stability**: Ensuring steering vectors work reliably across conversations
4. **Interpretability**: Understanding what information vectors encode
5. **Optimization**: Learning which vectors to use when

## Alternative Approaches (If API Unavailable)

If the Anthropic API doesn't directly support steering vectors:

1. **System Prompt Encoding**: Use special tokens/formats in system prompts to simulate vector communication
2. **Metadata Channels**: Pass structured metadata alongside text messages
3. **Local Model Fine-tuning**: Use open-source models where we have full control
4. **Anthropic Research Collaboration**: Partner with Anthropic to explore this capability

## Research Questions

1. Can steering vectors enable more efficient AI-to-AI collaboration?
2. Will models develop consistent "meanings" for different vectors?
3. How does vector communication compare to natural language in information density?
4. Can models learn to use vectors they haven't been explicitly trained on?
5. What types of information are best communicated via vectors vs. text?

## Related Work

- **Representation Engineering** (Zou et al., 2023)
- **Activation Addition** (Turner et al., 2023)
- **Contrastive Activation Addition** (CAA)
- **Sparse Autoencoders** for interpretability

## Next Steps

1. Contact Anthropic about steering vector API capabilities
2. Research existing steering vector libraries and techniques
3. Create prototype with simulated steering vectors
4. Design experiments to test different communication patterns
5. Build analysis tools to study vector usage patterns

## Contributing

If you're interested in helping with steering vector implementation:

1. Research steering vector extraction techniques
2. Explore Anthropic API documentation for relevant features
3. Suggest experiments for testing vector communication
4. Contribute analysis tools for conversation dynamics
5. Share relevant papers and research

---

**Note**: This is an experimental research project. Steering vector implementation may require collaboration with Anthropic or use of alternative approaches depending on API capabilities.
