# Documentation Index

Complete documentation for Local Cookbook project.

## ?? Documentation Structure

```
docs/
??? README.md                 # Main documentation index
??? installation/             # Installation guides
?   ??? README.md             # Backend installation (vLLM, Ollama, llama.cpp)
??? usage/                    # Usage guides
?   ??? README.md             # How to use the tools
??? models/                   # Model information
?   ??? README.md             # Model database and specifications
??? commands/                 # Command reference
?   ??? README.md             # Complete command reference
?   ??? backend-check.md      # Quick backend check guide
??? examples/                 # Example outputs
    ??? README.md             # Sample outputs and use cases
```

## ?? Quick Start

1. **Install**: See `installation/README.md`
2. **Check System**: `uv run python -m local_cookbook.main check`
3. **View Models**: `uv run python -m local_cookbook.main list-llms`
4. **Benchmark**: See `usage/README.md`

## ?? Documentation Sections

### Installation
- [Installation Guide](installation/README.md)
  - vLLM installation
  - Ollama installation
  - llama.cpp installation
  - Model downloads
  - Troubleshooting

### Usage
- [Usage Guide](usage/README.md)
  - Local Cookbook commands
  - LLM Comparisons commands
  - Common workflows
  - Output interpretation

### Models
- [Model Database](models/README.md)
  - Supported models
  - Quantization guide
  - VRAM requirements
  - Model recommendations by VRAM

### Commands
- [Command Reference](commands/README.md)
  - All available commands
  - Quick reference card
  - Shell aliases
- [Backend Check](commands/backend-check.md)
  - Pull commands by VRAM
  - Quick reference

### Examples
- [Example Outputs](examples/README.md)
  - Sample system check output
  - Benchmark examples
  - Common use cases
  - Sample scripts

## ?? Finding Information

### By Task

**I want to...**
- **Check my system**: See `usage/README.md` ? Basic Usage
- **Install a backend**: See `installation/README.md`
- **Find what models I can run**: See `models/README.md` ? Model Recommendations
- **Pull a model**: See `commands/backend-check.md`
- **Benchmark backends**: See `usage/README.md` ? LLM Comparisons
- **See example outputs**: See `examples/README.md`

### By Backend

**vLLM:**
- Installation: `installation/README.md` ? vLLM
- Model names: `models/README.md` ? vLLM Model Names
- Commands: `commands/README.md` ? vLLM Commands

**Ollama:**
- Installation: `installation/README.md` ? Ollama
- Model names: `models/README.md` ? Ollama Pull Commands
- Commands: `commands/README.md` ? Ollama Commands

**llama.cpp:**
- Installation: `installation/README.md` ? llama.cpp
- Model paths: `models/README.md` ? llama.cpp Model Paths
- Commands: `commands/README.md` ? llama.cpp Commands

## ?? Quick Reference

### Essential Commands

```bash
# System check
cd ~/local-cookbook
uv run python -m local_cookbook.main check

# List models
uv run python -m local_cookbook.main list-llms

# Benchmark
cd ~/local-cookbook/llm-comparisons
uv run python -m llm_comparisons.main benchmark

# Pull models
ollama pull deepseek-coder:33b
ollama pull glm-4v-9b
```

### Your System (24GB VRAM)

**Maximum Models:**
- DeepSeek-30B (GPTQ-4bit)
- GLM-4.5V (INT8)

**Pull Commands:**
```bash
ollama pull deepseek-coder:33b
ollama pull glm-4v-9b
```

See `commands/backend-check.md` for complete list.

## ?? Related Documentation

- Main project README: `../README.md`
- LLM Comparisons README: `../llm-comparisons/README.md`

## ?? Need Help?

1. Check the relevant section above
2. Review `examples/README.md` for sample outputs
3. Check `installation/README.md` ? Troubleshooting
