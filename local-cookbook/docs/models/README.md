# Model Database

## Supported Models

### GPT-OSS (Open Source GPT Models)

**Variants:**
- Llama-2-7B
- Llama-2-13B

**Requirements:**
- Min VRAM: 4GB (7B), 8GB (13B)
- Recommended VRAM: 8GB (7B), 16GB (13B)
- Min RAM: 8GB (7B), 16GB (13B)

**Ollama:**
```bash
ollama pull llama2:7b
ollama pull llama2:13b
```

**vLLM:**
- `meta-llama/Llama-2-7b-chat-hf`
- `meta-llama/Llama-2-13b-chat-hf`

**llama.cpp:**
- `models/llama-2-7b.gguf` (FP16)
- `models/llama-2-7b-q8_0.gguf` (INT8)
- `models/llama-2-7b-q4_0.gguf` (INT4)

### Qwen (Alibaba)

**Variants:**
- Qwen-7B
- Qwen-14B

**Requirements:**
- Min VRAM: 6GB (7B), 12GB (14B)
- Recommended VRAM: 12GB (7B), 24GB (14B)
- Supports 4-bit quantization

**Ollama:**
```bash
ollama pull qwen:7b
ollama pull qwen:14b
```

**vLLM:**
- `Qwen/Qwen-7B-Chat`
- `Qwen/Qwen-14B-Chat`

**llama.cpp:**
- `models/qwen-7b.gguf` (FP16)
- `models/qwen-7b-q8_0.gguf` (INT8)
- `models/qwen-7b-q4_0.gguf` (INT4)

### DeepSeek

**Variants:**
- DeepSeek-7B
- DeepSeek-30B (67B available)

**Requirements:**
- Min VRAM: 8GB (7B), 16GB (30B)
- Recommended VRAM: 16GB (7B), 32GB (30B)
- Best with high VRAM

**Ollama:**
```bash
ollama pull deepseek-coder:7b
ollama pull deepseek-coder:33b  # 30B model
```

**vLLM:**
- `deepseek-ai/DeepSeek-V3.1`

**llama.cpp:**
- `models/deepseek-7b.gguf`
- `models/deepseek-30b.gguf`

### GLM-4.6 (Zhipu AI)

**Variants:**
- GLM-4.6 (6B)
- GLM-4.6-9B

**Requirements:**
- Min VRAM: 8GB (6B), 12GB (9B)
- Recommended VRAM: 16GB (6B), 20GB (9B)
- Supports various quantization formats

**Ollama:**
```bash
ollama pull glm-4-6b
ollama pull glm-4-9b
```

**vLLM:**
- `THUDM/glm-4-9b-chat`

**llama.cpp:**
- `models/glm-4-6b.gguf`
- `models/glm-4-9b.gguf`

### GLM-4.5V (Zhipu AI Vision)

**Variants:**
- GLM-4.5V (9B)

**Requirements:**
- Min VRAM: 12GB
- Recommended VRAM: 20GB
- Vision-language model (requires more VRAM)

**Ollama:**
```bash
ollama pull glm-4v-9b
```

**vLLM:**
- `THUDM/glm-4v-9b`

**llama.cpp:**
- `models/glm-4v-9b.gguf`
- `models/glm-4v-9b-q8_0.gguf` (INT8)
- `models/glm-4v-9b-q4_0.gguf` (INT4)

### Mixtral-8x7B

**Variants:**
- Mixtral-8x7B

**Requirements:**
- Min VRAM: 26GB
- Recommended VRAM: 40GB
- Mixture of Experts architecture

**Ollama:**
```bash
ollama pull mixtral:8x7b
```

**vLLM:**
- `mistralai/Mixtral-8x7B-Instruct-v0.1`

**llama.cpp:**
- `models/mixtral-8x7b.gguf`

## Quantization Guide

### Quantization Types

1. **FP16**: Full precision, highest quality, largest size
2. **INT8**: 8-bit integer, good quality/size balance
3. **INT4**: 4-bit integer, smallest size, some quality loss
4. **GPTQ-4bit**: 4-bit GPTQ quantization, good quality/speed balance
5. **AWQ-4bit**: 4-bit AWQ quantization, optimized for inference

### VRAM Requirements by Size

| Model Size | FP16 | INT8 | INT4 | GPTQ-4bit | AWQ-4bit |
|------------|------|------|------|-----------|----------|
| 7B         | 14GB | 7GB  | 4GB  | 4.5GB     | 4.5GB    |
| 13B        | 26GB | 13GB | 7GB  | 7.5GB     | 7.5GB    |
| 30B        | 60GB | 30GB | 15GB | 16GB      | 16GB     |
| 65B        | 130GB| 65GB | 33GB | 35GB      | 35GB     |

### Choosing Quantization

- **Best Quality**: FP16 or INT8
- **Balanced**: GPTQ-4bit or AWQ-4bit (recommended)
- **Maximum Compression**: INT4

## Model Recommendations by VRAM

### 8GB VRAM
- 7B models with INT4 or GPTQ-4bit

### 16GB VRAM
- 7B models with FP16
- 13B models with INT8
- 13B models with GPTQ-4bit
- GLM-4.6-9B with INT8

### 24GB VRAM (Your System)
- 30B models with GPTQ-4bit or AWQ-4bit
- 30B models with INT4
- 13B models with INT8
- GLM-4.5V with INT8

### 32GB+ VRAM
- 30B models with INT8
- 30B models with FP16 (if 60GB+)
- 65B+ models with quantization
