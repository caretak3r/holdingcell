# Quick Start Guide

Get started with Local Cookbook in 5 minutes!

## Step 1: Check Your System

```bash
cd ~/local-cookbook
uv sync
uv run python -m local_cookbook.main check
```

This will show:
- Your GPU, CPU, and RAM
- Which models are compatible
- **Maximum model size you can run**
- **Pull commands for each backend**

## Step 2: Install a Backend (Choose One)

### Option A: Ollama (Easiest)

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Option B: vLLM (Best Performance)

```bash
pip install vllm
```

### Option C: llama.cpp (Lightweight)

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp && make
```

## Step 3: Pull a Model

Based on your system check, use the recommended pull commands:

**For 24GB VRAM (RTX 3090):**
```bash
# Maximum size
ollama pull deepseek-coder:33b
ollama pull glm-4v-9b

# Or smaller/faster
ollama pull glm-4-9b
ollama pull qwen:14b
```

## Step 4: Test Your Setup

```bash
# Test Ollama
ollama run glm-4-9b

# Test vLLM (if installed)
python -m vllm.entrypoints.openai.api_server --model THUDM/glm-4-9b-chat
```

## Step 5: Benchmark (Optional)

```bash
cd ~/local-cookbook/llm-comparisons
uv sync
uv run python -m llm_comparisons.main benchmark
```

## What's Next?

- **Full Documentation**: See `docs/README.md`
- **Model Database**: See `docs/models/README.md`
- **Command Reference**: See `docs/commands/README.md`
- **Examples**: See `docs/examples/README.md`

## Quick Commands Cheat Sheet

```bash
# System check
cd ~/local-cookbook && uv run python -m local_cookbook.main check

# List models
uv run python -m local_cookbook.main list-llms

# Benchmark
cd ~/local-cookbook/llm-comparisons
uv run python -m llm_comparisons.main benchmark

# Pull models
ollama pull deepseek-coder:33b
ollama pull glm-4v-9b
```

## Troubleshooting

### vLLM not found
```bash
pip install vllm
```

### Ollama not found
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Models not downloading
- Check internet connection
- Verify model names are correct
- Check disk space

For more help, see `docs/installation/README.md` ? Troubleshooting
