# Command Reference

## Local Cookbook Commands

### System Check

```bash
# Basic check
uv run python -m local_cookbook.main check

# Check specific models
uv run python -m local_cookbook.main check --llm glm-4.6 --llm glm-4.5v

# Detailed output
uv run python -m local_cookbook.main check --detailed

# JSON output
uv run python -m local_cookbook.main check --json > report.json
```

### List Available Models

```bash
uv run python -m local_cookbook.main list-llms
```

**Available Models:**
- `gpt-oss` - GPT-OSS (Open Source GPT Models)
- `qwen` - Qwen (Alibaba)
- `deepseek` - DeepSeek
- `glm-4.6` - GLM-4.6 (Zhipu AI)
- `glm-4.5v` - GLM-4.5V (Zhipu AI Vision)

## LLM Comparisons Commands

### Benchmark

```bash
# Basic benchmark (default: DeepSeek-V3.1)
uv run python -m llm_comparisons.main benchmark

# Custom model
uv run python -m llm_comparisons.main benchmark --model qwen-7b

# Custom prompt
uv run python -m llm_comparisons.main benchmark --prompt "your prompt here"

# Specific backends
uv run python -m llm_comparisons.main benchmark --backend ollama --backend vllm

# JSON output
uv run python -m llm_comparisons.main benchmark --json

# Skip comparison analysis
uv run python -m llm_comparisons.main benchmark --no-comparison
```

### List Models

```bash
uv run python -m llm_comparisons.main list-models
```

### Check Backends

```bash
uv run python -m llm_comparisons.main check-backends
```

## Ollama Commands

### Pull Models

```bash
# DeepSeek
ollama pull deepseek-coder:33b
ollama pull deepseek-coder:7b

# Qwen
ollama pull qwen:7b
ollama pull qwen:14b

# GLM
ollama pull glm-4-6b
ollama pull glm-4-9b
ollama pull glm-4v-9b

# Llama
ollama pull llama2:7b
ollama pull llama2:13b

# Mixtral
ollama pull mixtral:8x7b
```

### List Installed Models

```bash
ollama list
```

### Run Model

```bash
ollama run glm-4-9b
```

### Remove Model

```bash
ollama rm model-name
```

## vLLM Commands

### Start Server

```bash
# Basic (default port 8000)
python -m vllm.entrypoints.openai.api_server --model deepseek-ai/DeepSeek-V3.1

# Custom port
python -m vllm.entrypoints.openai.api_server \
  --model deepseek-ai/DeepSeek-V3.1 \
  --port 8001

# With GPU limits
python -m vllm.entrypoints.openai.api_server \
  --model deepseek-ai/DeepSeek-V3.1 \
  --gpu-memory-utilization 0.9
```

### Test API

```bash
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-ai/DeepSeek-V3.1",
    "prompt": "Hello, how are you?",
    "max_tokens": 50
  }'
```

## llama.cpp Commands

### Run Model

```bash
# Basic
./llama-cli -m models/model.gguf -p "Your prompt"

# With options
./llama-cli \
  -m models/qwen-7b-q8_0.gguf \
  -p "Your prompt" \
  -n 2048 \
  -t 4 \
  --temp 0.7
```

### Quantization

```bash
# Convert to INT8
./quantize models/model.gguf models/model-q8_0.gguf q8_0

# Convert to INT4
./quantize models/model.gguf models/model-q4_0.gguf q4_0
```

## Useful Shell Aliases

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Local Cookbook shortcuts
alias lc-check='cd ~/local-cookbook && uv run python -m local_cookbook.main check'
alias lc-models='cd ~/local-cookbook && uv run python -m local_cookbook.main list-llms'

# LLM Comparisons shortcuts
alias llm-bench='cd ~/local-cookbook/llm-comparisons && uv run python -m llm_comparisons.main benchmark'
alias llm-backends='cd ~/local-cookbook/llm-comparisons && uv run python -m llm_comparisons.main check-backends'
```

## Quick Reference Card

```
???????????????????????????????????????????????????????????
? Local Cookbook Quick Reference                         ?
???????????????????????????????????????????????????????????
? Check System:                                           ?
?   lc-check                                              ?
?                                                         ?
? List Models:                                            ?
?   lc-models                                             ?
?                                                         ?
? Benchmark:                                              ?
?   llm-bench                                             ?
?                                                         ?
? Check Backends:                                         ?
?   llm-backends                                          ?
?                                                         ?
? Pull Models (Ollama):                                  ?
?   ollama pull glm-4v-9b                                ?
?   ollama pull deepseek-coder:33b                       ?
???????????????????????????????????????????????????????????
```
