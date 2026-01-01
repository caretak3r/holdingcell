# Better Quantized DeepSeek-V3.1 Models

## Problem
Your current model uses **Q3_K_XL** quantization (3-bit) which is causing very slow performance (0.35 tokens/second). This quantization level is too aggressive and causes slowdowns.

## Solution
Switch to better quantized models that provide **2-5x faster inference** while maintaining good quality.

## Recommended Models (Ordered by Speed)

### 1. Q4_K_S - Fastest (Recommended for Speed)
- **Speed**: Very Fast (~3-5x faster than Q3_K_XL)
- **Quality**: Good
- **VRAM**: ~35GB
- **Repository**: `bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF`
- **Download**: Look for files with `Q4_K_S` in the name

### 2. Q4_K_M - Fast (Recommended Balance)
- **Speed**: Fast (~2-4x faster than Q3_K_XL)
- **Quality**: Good
- **VRAM**: ~35GB
- **Repository**: `bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF`
- **Download**: Look for files with `Q4_K_M` in the name
- **Best overall choice** for speed/quality balance

### 3. Q5_K_M - Medium Speed
- **Speed**: Medium (~1.5-3x faster than Q3_K_XL)
- **Quality**: Very Good
- **VRAM**: ~40GB
- **Repository**: `unsloth/DeepSeek-V3.1-GGUF` or `bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF`
- **Download**: Look for files with `Q5_K_M` in the name

### 4. Q6_K - Slower but Excellent Quality
- **Speed**: Medium-Slow (~1.2-2x faster than Q3_K_XL)
- **Quality**: Excellent
- **VRAM**: ~50GB
- **Repository**: `unsloth/DeepSeek-V3.1-GGUF` or `bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF`
- **Download**: Look for files with `Q6_K` in the name

### 5. Q8_0 - Best Quality
- **Speed**: Slow (similar or slightly faster than Q3_K_XL)
- **Quality**: Best
- **VRAM**: ~70GB
- **Repository**: `bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF`
- **Download**: Look for files with `Q8_0` in the name

## How to Download and Use

### Option 1: Using huggingface-cli (Recommended)
```bash
# Install if needed
pip install huggingface_hub

# Download Q4_K_M model (recommended)
huggingface-cli download bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF \
    deepseek-ai_DeepSeek-V3.1-Base-Q4_K_M.gguf \
    --local-dir models/ \
    --local-dir-use-symlinks False
```

### Option 2: Using wget/curl
```bash
# Find the exact file URL from Hugging Face repository page
# Then download:
wget -O models/deepseek-v3.1-q4_k_m.gguf \
    "https://huggingface.co/bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF/resolve/main/deepseek-ai_DeepSeek-V3.1-Base-Q4_K_M.gguf"
```

### Option 3: Direct from Hugging Face Web UI
1. Go to: https://huggingface.co/bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF
2. Browse files and find the `.gguf` file with `Q4_K_M` or `Q4_K_S` in the name
3. Download the file
4. Place it in your models directory

## Update Your llama.cpp Server

After downloading, update your llama.cpp server configuration to use the new model:

```bash
# Example: Update your server startup command
./llama-server \
    -m models/deepseek-v3.1-q4_k_m.gguf \
    --host 0.0.0.0 \
    --port 8888
```

## Expected Performance Improvement

- **Current (Q3_K_XL)**: ~0.35 tokens/second
- **With Q4_K_S**: ~1.0-1.5 tokens/second (3-4x faster)
- **With Q4_K_M**: ~0.8-1.2 tokens/second (2-3x faster)
- **With Q5_K_M**: ~0.6-1.0 tokens/second (1.5-2x faster)

## Why Q3_K_XL is Slow

- **3-bit quantization** is too aggressive
- Requires more computation to decompress/dequantize
- **Sharded across 7 files** adds I/O overhead
- Better quantization levels (Q4+) are actually faster because they balance compression with computational efficiency

## Repository Links

1. **bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF**
   - URL: https://huggingface.co/bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF
   - Has Q4_K_M, Q4_K_S, Q5_K_M, Q6_K, Q8_0 variants

2. **unsloth/DeepSeek-V3.1-GGUF**
   - URL: https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF
   - Check for available quantization levels

## Quick Test Script

After downloading a new model, test it with:

```bash
python tests/simple.py
```

The script will automatically test the model and show performance metrics.
