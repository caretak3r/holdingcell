# LLM Comparisons

Benchmarking tool to compare different LLM backends (vLLM, llama.cpp, Ollama) on your system.

## Features

- **Multi-Backend Support**: Compare vLLM, llama.cpp, and Ollama
- **Configurable Models**: Easy to switch between different models
- **Performance Metrics**: Measure latency, tokens/second, and total time
- **Output Capture**: Record and compare model outputs
- **Rich Reports**: Beautiful formatted comparison reports

## Default Configuration

- **Model**: DeepSeek-V3.1
- **Test Prompt**: "build the game of life using python"

## Installation

```bash
cd llm-comparisons
uv sync
```

## Usage

### Run Benchmark

Run benchmark with default settings (DeepSeek-V3.1):
```bash
uv run python -m llm_comparisons.main benchmark
```

Or use the CLI entry point:
```bash
uv run llm-compare benchmark
```

### Custom Model and Prompt

```bash
uv run llm-compare benchmark --model qwen-7b --prompt "write a fibonacci function"
```

### Specific Backends

Test only specific backends:
```bash
uv run llm-compare benchmark --backend ollama --backend vllm
```

### JSON Output

```bash
uv run llm-compare benchmark --json
```

### List Available Models

```bash
uv run llm-compare list-models
```

### Check Backend Availability

```bash
uv run llm-compare check-backends
```

## Backend Setup

### vLLM

```bash
pip install vllm
```

### Ollama

Install from: https://ollama.ai

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Then pull your model
ollama pull deepseek-v3.1
```

### llama.cpp

Install from: https://github.com/ggerganov/llama.cpp

You'll need to download GGUF model files and configure the path in the model config.

## Output

The tool generates:
- **Performance Summary Table**: Time, tokens/s, tokens generated for each backend
- **Detailed Outputs**: Full model responses for comparison
- **Comparison Analysis**: Speed comparisons and backend advantages
- **JSON Report**: Saved to `benchmark_results.json` for further analysis

## Model Configuration

Models are configured in `llm_comparisons/config.py`. To add a new model:

```python
MODEL_CONFIGS["your-model"] = ModelConfig(
    name="Your Model Name",
    vllm_model_path="path/to/model",
    ollama_model_name="model-name",
    llamacpp_model_path="/path/to/model.gguf",
    notes="Description"
)
```

