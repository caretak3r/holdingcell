# Local Cookbook

A comprehensive system resource checker and LLM compatibility analyzer. This cookbook provides scripts to check your system's GPU, CPU, memory, and VRAM capabilities before installing and running LLMs like GPT-OSS, Qwen, and DeepSeek.

## Features

- **GPU Detection**: Count GPUs, check VRAM, and identify GPU models
- **CPU Analysis**: Detect CPU cores, threads, and architecture
- **Memory Check**: System RAM and available memory
- **LLM Compatibility**: Check if your system meets requirements for:
  - GPT-OSS (Open Source GPT models)
  - Qwen (Alibaba's Qwen models)
  - DeepSeek (DeepSeek AI models)
- **Beautiful Reports**: Rich, formatted output with color-coded status indicators

## Installation

```bash
cd local-cookbook
uv sync
```

## Usage

### Installation

First, install dependencies:

```bash
cd local-cookbook
uv sync
```

### Python CLI

Basic system check:
```bash
uv run local-cookbook check
```

Detailed check with more information:
```bash
uv run local-cookbook check --detailed
```

JSON output (for scripting):
```bash
uv run local-cookbook check --json
```

Check specific LLMs only:
```bash
uv run local-cookbook check --llm gpt-oss --llm qwen
```

List all supported LLMs:
```bash
uv run local-cookbook list-llms
```

### Bash Script

Quick system check:
```bash
./check-system.sh
```

### Example Output

The tool will show:
- **GPU Information**: Count, models, total VRAM
- **CPU Information**: Model, cores, architecture, frequency
- **Memory Information**: Total, available, and used RAM
- **LLM Compatibility**: Detailed compatibility check for each LLM with:
  - Pass/Warning/Fail status for each resource
  - Minimum vs Recommended requirements
  - Warnings and recommendations
  - Notes about quantization support

## Requirements

- Python 3.9+
- NVIDIA GPU (for GPU checks) - will gracefully degrade if not available
- Linux/Unix system
