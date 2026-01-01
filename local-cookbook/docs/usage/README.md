# Usage Guides

## Local Cookbook - System Checker

### Basic Usage

```bash
cd ~/local-cookbook
uv run python -m local_cookbook.main check
```

### Check Specific Models

```bash
# Check only GLM models
uv run python -m local_cookbook.main check --llm glm-4.6 --llm glm-4.5v

# Check all models
uv run python -m local_cookbook.main check
```

### JSON Output

```bash
uv run python -m local_cookbook.main check --json > system_report.json
```

### Detailed Output

```bash
uv run python -m local_cookbook.main check --detailed
```

## LLM Comparisons - Benchmark Tool

### Basic Benchmark

```bash
cd ~/local-cookbook/llm-comparisons
uv sync
uv run python -m llm_comparisons.main benchmark
```

### Custom Model and Prompt

```bash
uv run python -m llm_comparisons.main benchmark \
  --model qwen-7b \
  --prompt "explain quantum computing"
```

### Specific Backends

```bash
# Test only Ollama
uv run python -m llm_comparisons.main benchmark --backend ollama

# Test multiple backends
uv run python -m llm_comparisons.main benchmark \
  --backend ollama \
  --backend vllm
```

### JSON Output

```bash
uv run python -m llm_comparisons.main benchmark --json
```

## Common Workflows

### 1. Check System Before Installing Models

```bash
# Step 1: Check system resources
cd ~/local-cookbook
uv run python -m local_cookbook.main check

# Step 2: Review quantized model recommendations
# (Output is shown in the check command)

# Step 3: Install recommended backend
# Follow installation guide in docs/installation/
```

### 2. Benchmark Different Backends

```bash
# Step 1: Check backend availability
cd ~/local-cookbook/llm-comparisons
uv run python -m llm_comparisons.main check-backends

# Step 2: Run benchmark
uv run python -m llm_comparisons.main benchmark

# Step 3: Compare results
# Review benchmark_results.json
```

### 3. Find Maximum Model Size

```bash
# Run system check
cd ~/local-cookbook
uv run python -m local_cookbook.main check

# Look for "Maximum Model Size You Can Run" section
# Use the provided pull commands
```

## Output Interpretation

### System Check Output

- **GPU Information**: Shows VRAM and GPU count
- **CPU Information**: Shows cores and architecture
- **Memory Information**: Shows RAM availability
- **LLM Compatibility**: Shows which models work
- **Quantized Recommendations**: Shows specific model names

### Benchmark Output

- **Performance Summary**: Time, tokens/s, tokens generated
- **Detailed Outputs**: Full model responses
- **Comparison Analysis**: Speed comparisons between backends

## Tips

1. **Run checks before installing**: Always check system compatibility first
2. **Use quantized models**: They require less VRAM/RAM
3. **Test with small prompts**: Start with short prompts for faster testing
4. **Save outputs**: Use `--json` flag to save results for later analysis
