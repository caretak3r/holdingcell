# Installation Guides

## System Requirements

- Python 3.9+
- Linux/Unix system
- NVIDIA GPU (optional, for GPU checks)
- At least 8GB RAM

## Local Cookbook Installation

```bash
cd ~/local-cookbook
uv sync
```

## Backend Installations

### vLLM

```bash
# With CUDA support
pip install vllm

# Verify installation
python -c "import vllm; print('vLLM installed successfully')"
```

**System Requirements:**
- CUDA-capable GPU
- CUDA 11.8+ or 12.1+
- Python 3.8+

### Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installation
ollama --version

# Start Ollama service (usually auto-starts)
ollama serve
```

**System Requirements:**
- macOS, Linux, or Windows
- 8GB+ RAM recommended
- GPU optional but recommended

### llama.cpp

```bash
# Clone repository
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp

# Build (Linux)
make

# Or use CMake
mkdir build && cd build
cmake ..
cmake --build . --config Release

# Verify installation
./llama-cli --help
```

**System Requirements:**
- C++ compiler (gcc/clang)
- CMake (optional)
- 4GB+ RAM

## Model Downloads

### Ollama Models

```bash
# DeepSeek
ollama pull deepseek-coder:33b

# Qwen
ollama pull qwen:7b
ollama pull qwen:14b

# GLM
ollama pull glm-4-9b
ollama pull glm-4v-9b

# Llama
ollama pull llama2:7b
ollama pull llama2:13b
```

### vLLM Models

vLLM automatically downloads models from Hugging Face. Examples:
- `deepseek-ai/DeepSeek-V3.1`
- `Qwen/Qwen-7B-Chat`
- `THUDM/glm-4-9b-chat`
- `meta-llama/Llama-2-7b-chat-hf`

### llama.cpp Models

Download GGUF files from Hugging Face or model repositories:
- Visit: https://huggingface.co/models?search=gguf
- Download appropriate quantization (q4_0, q8_0, etc.)
- Place in `models/` directory

## Troubleshooting

### vLLM Issues

- **CUDA not found**: Install CUDA toolkit
- **Out of memory**: Use smaller models or quantization
- **Import errors**: Ensure CUDA libraries are in PATH

### Ollama Issues

- **Service not running**: Run `ollama serve`
- **Model not found**: Check `ollama list` for available models
- **Port conflict**: Change port with `OLLAMA_HOST=0.0.0.0:11435`

### llama.cpp Issues

- **Build errors**: Ensure all dependencies installed
- **Model not found**: Check file path and permissions
- **Performance issues**: Adjust thread count with `-t` flag
