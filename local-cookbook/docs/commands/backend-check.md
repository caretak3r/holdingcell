# Quick Reference: Pull Commands

Quick reference for pulling models with different backends.

## Ollama Pull Commands

### For Your System (24GB VRAM)

```bash
# Maximum size models
ollama pull deepseek-coder:33b      # DeepSeek-30B
ollama pull glm-4v-9b               # GLM-4.5V vision model

# Recommended models
ollama pull glm-4-9b                # GLM-4.6 9B
ollama pull qwen:14b                 # Qwen 14B
ollama pull llama2:13b               # Llama-2 13B

# Smaller models (faster)
ollama pull qwen:7b                  # Qwen 7B
ollama pull glm-4-6b                 # GLM-4.6 6B
ollama pull deepseek-coder:7b        # DeepSeek 7B
```

## vLLM Model Names

### For Your System (24GB VRAM)

```python
# Maximum size models
"deepseek-ai/DeepSeek-V3.1"          # DeepSeek-30B
"THUDM/glm-4v-9b"                     # GLM-4.5V

# Recommended models
"THUDM/glm-4-9b-chat"                 # GLM-4.6 9B
"Qwen/Qwen-14B-Chat"                  # Qwen 14B
"meta-llama/Llama-2-13b-chat-hf"     # Llama-2 13B

# Smaller models
"Qwen/Qwen-7B-Chat"                   # Qwen 7B
"meta-llama/Llama-2-7b-chat-hf"      # Llama-2 7B
```

**Usage:**
```bash
python -m vllm.entrypoints.openai.api_server --model "deepseek-ai/DeepSeek-V3.1"
```

## llama.cpp Model Paths

### For Your System (24GB VRAM)

```bash
# Download from Hugging Face, then use:
models/deepseek-30b.gguf              # DeepSeek-30B FP16
models/deepseek-30b-q8_0.gguf         # DeepSeek-30B INT8
models/deepseek-30b-q4_0.gguf         # DeepSeek-30B INT4

models/glm-4v-9b.gguf                 # GLM-4.5V FP16
models/glm-4v-9b-q8_0.gguf            # GLM-4.5V INT8
models/glm-4v-9b-q4_0.gguf            # GLM-4.5V INT4

models/glm-4-9b.gguf                  # GLM-4.6 9B FP16
models/qwen-14b-q8_0.gguf            # Qwen 14B INT8
models/llama-2-13b-q8_0.gguf         # Llama-2 13B INT8
```

**Usage:**
```bash
./llama-cli -m models/deepseek-30b-q8_0.gguf -p "Your prompt"
```

## Recommended Workflow

1. **Check system**: `uv run python -m local_cookbook.main check`
2. **Review recommendations**: Look at "Maximum Model Size You Can Run"
3. **Pull model**: Use the provided pull commands
4. **Test**: Run a simple prompt to verify
5. **Benchmark**: Compare backends if multiple are available

## By VRAM Size

### 8GB VRAM
```bash
ollama pull qwen:7b
ollama pull glm-4-6b
```

### 16GB VRAM
```bash
ollama pull qwen:14b
ollama pull glm-4-9b
ollama pull llama2:13b
```

### 24GB VRAM (Your System)
```bash
ollama pull deepseek-coder:33b
ollama pull glm-4v-9b
```

### 32GB+ VRAM
```bash
ollama pull mixtral:8x7b
# Can run FP16 models
```
