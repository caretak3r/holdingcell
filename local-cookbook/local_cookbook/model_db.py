"""Model database with specific names for each backend."""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ModelBackendNames:
    """Model names for different backends."""
    ollama: Optional[str] = None
    vllm: Optional[str] = None
    llamacpp: Optional[str] = None
    notes: str = ""


# Database of specific model names for each backend
MODEL_BACKEND_DB: Dict[str, Dict[str, ModelBackendNames]] = {
    # GPT-OSS variants
    "Llama-2-7B": {
        "fp16": ModelBackendNames(
            ollama="llama2:7b",
            vllm="meta-llama/Llama-2-7b-chat-hf",
            llamacpp="models/llama-2-7b.gguf",
            notes="Llama 2 7B base model"
        ),
        "int8": ModelBackendNames(
            ollama="llama2:7b",
            vllm="meta-llama/Llama-2-7b-chat-hf",
            llamacpp="models/llama-2-7b-q8_0.gguf",
            notes="INT8 quantized"
        ),
        "int4": ModelBackendNames(
            ollama="llama2:7b",
            vllm="meta-llama/Llama-2-7b-chat-hf",
            llamacpp="models/llama-2-7b-q4_0.gguf",
            notes="INT4 quantized"
        ),
    },
    "Llama-2-13B": {
        "fp16": ModelBackendNames(
            ollama="llama2:13b",
            vllm="meta-llama/Llama-2-13b-chat-hf",
            llamacpp="models/llama-2-13b.gguf",
            notes="Llama 2 13B base model"
        ),
        "int8": ModelBackendNames(
            ollama="llama2:13b",
            vllm="meta-llama/Llama-2-13b-chat-hf",
            llamacpp="models/llama-2-13b-q8_0.gguf",
            notes="INT8 quantized"
        ),
        "int4": ModelBackendNames(
            ollama="llama2:13b",
            vllm="meta-llama/Llama-2-13b-chat-hf",
            llamacpp="models/llama-2-13b-q4_0.gguf",
            notes="INT4 quantized"
        ),
    },
    
    # Qwen variants
    "Qwen-7B": {
        "fp16": ModelBackendNames(
            ollama="qwen:7b",
            vllm="Qwen/Qwen-7B-Chat",
            llamacpp="models/qwen-7b.gguf",
            notes="Qwen 7B base model"
        ),
        "int8": ModelBackendNames(
            ollama="qwen:7b",
            vllm="Qwen/Qwen-7B-Chat",
            llamacpp="models/qwen-7b-q8_0.gguf",
            notes="INT8 quantized"
        ),
        "int4": ModelBackendNames(
            ollama="qwen:7b",
            vllm="Qwen/Qwen-7B-Chat",
            llamacpp="models/qwen-7b-q4_0.gguf",
            notes="INT4 quantized"
        ),
    },
    "Qwen-14B": {
        "fp16": ModelBackendNames(
            ollama="qwen:14b",
            vllm="Qwen/Qwen-14B-Chat",
            llamacpp="models/qwen-14b.gguf",
            notes="Qwen 14B base model"
        ),
        "int8": ModelBackendNames(
            ollama="qwen:14b",
            vllm="Qwen/Qwen-14B-Chat",
            llamacpp="models/qwen-14b-q8_0.gguf",
            notes="INT8 quantized"
        ),
        "int4": ModelBackendNames(
            ollama="qwen:14b",
            vllm="Qwen/Qwen-14B-Chat",
            llamacpp="models/qwen-14b-q4_0.gguf",
            notes="INT4 quantized"
        ),
    },
    
    # DeepSeek variants
    "DeepSeek-7B": {
        "fp16": ModelBackendNames(
            ollama="deepseek-coder:7b",
            vllm="deepseek-ai/DeepSeek-V3.1",
            llamacpp="models/deepseek-7b.gguf",
            notes="DeepSeek 7B base model"
        ),
        "int8": ModelBackendNames(
            ollama="deepseek-coder:7b",
            vllm="deepseek-ai/DeepSeek-V3.1",
            llamacpp="models/deepseek-7b-q8_0.gguf",
            notes="INT8 quantized"
        ),
        "int4": ModelBackendNames(
            ollama="deepseek-coder:7b",
            vllm="deepseek-ai/DeepSeek-V3.1",
            llamacpp="models/deepseek-7b-q4_0.gguf",
            notes="INT4 quantized"
        ),
    },
    "DeepSeek-30B": {
        "fp16": ModelBackendNames(
            ollama="deepseek-coder:33b",
            vllm="deepseek-ai/DeepSeek-V3.1",
            llamacpp="models/deepseek-30b.gguf",
            notes="DeepSeek 30B base model"
        ),
        "int8": ModelBackendNames(
            ollama="deepseek-coder:33b",
            vllm="deepseek-ai/DeepSeek-V3.1",
            llamacpp="models/deepseek-30b-q8_0.gguf",
            notes="INT8 quantized"
        ),
        "int4": ModelBackendNames(
            ollama="deepseek-coder:33b",
            vllm="deepseek-ai/DeepSeek-V3.1",
            llamacpp="models/deepseek-30b-q4_0.gguf",
            notes="INT4 quantized"
        ),
    },
    "DeepSeek-V3.1": {
        "fp16": ModelBackendNames(
            ollama=None,
            vllm="deepseek-ai/DeepSeek-V3.1",
            llamacpp="bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF",
            notes="DeepSeek V3.1 67B base model - very large, requires 140GB+ VRAM"
        ),
        "int8": ModelBackendNames(
            ollama=None,
            vllm="deepseek-ai/DeepSeek-V3.1",
            llamacpp="bartowski/deepseek-ai_DeepSeek-V3.1-Base-Q8_0-GGUF",
            notes="Q8_0 quantized - best quality, ~70GB VRAM, good speed"
        ),
        "gptq-4bit": ModelBackendNames(
            ollama=None,
            vllm="deepseek-ai/DeepSeek-V3.1",
            llamacpp="bartowski/deepseek-ai_DeepSeek-V3.1-Base-Q4_K_M-GGUF",
            notes="Q4_K_M quantized - RECOMMENDED: fast, good quality, ~35GB VRAM, 2-5x faster than Q3_K_XL"
        ),
        "int4": ModelBackendNames(
            ollama=None,
            vllm="deepseek-ai/DeepSeek-V3.1",
            llamacpp="bartowski/deepseek-ai_DeepSeek-V3.1-Base-Q4_K_S-GGUF",
            notes="Q4_K_S quantized - fastest option, good quality, ~35GB VRAM"
        ),
    },
    
    # GLM-4.6 variants
    "GLM-4.6": {
        "fp16": ModelBackendNames(
            ollama="glm-4-6b",
            vllm="THUDM/glm-4-9b-chat",
            llamacpp="models/glm-4-6b.gguf",
            notes="GLM-4.6 base model (6B parameters)"
        ),
        "int8": ModelBackendNames(
            ollama="glm-4-6b",
            vllm="THUDM/glm-4-9b-chat",
            llamacpp="models/glm-4-6b-q8_0.gguf",
            notes="GLM-4.6 INT8 quantized"
        ),
        "int4": ModelBackendNames(
            ollama="glm-4-6b",
            vllm="THUDM/glm-4-9b-chat",
            llamacpp="models/glm-4-6b-q4_0.gguf",
            notes="GLM-4.6 INT4 quantized"
        ),
    },
    "GLM-4.6-9B": {
        "fp16": ModelBackendNames(
            ollama="glm-4-9b",
            vllm="THUDM/glm-4-9b-chat",
            llamacpp="models/glm-4-9b.gguf",
            notes="GLM-4.6 9B base model"
        ),
        "int8": ModelBackendNames(
            ollama="glm-4-9b",
            vllm="THUDM/glm-4-9b-chat",
            llamacpp="models/glm-4-9b-q8_0.gguf",
            notes="GLM-4.6 9B INT8 quantized"
        ),
        "int4": ModelBackendNames(
            ollama="glm-4-9b",
            vllm="THUDM/glm-4-9b-chat",
            llamacpp="models/glm-4-9b-q4_0.gguf",
            notes="GLM-4.6 9B INT4 quantized"
        ),
    },
    
    # GLM-4.5V variants
    "GLM-4.5V": {
        "fp16": ModelBackendNames(
            ollama="glm-4v-9b",
            vllm="THUDM/glm-4v-9b",
            llamacpp="models/glm-4v-9b.gguf",
            notes="GLM-4.5V vision model (9B parameters)"
        ),
        "int8": ModelBackendNames(
            ollama="glm-4v-9b",
            vllm="THUDM/glm-4v-9b",
            llamacpp="models/glm-4v-9b-q8_0.gguf",
            notes="GLM-4.5V INT8 quantized"
        ),
        "int4": ModelBackendNames(
            ollama="glm-4v-9b",
            vllm="THUDM/glm-4v-9b",
            llamacpp="models/glm-4v-9b-q4_0.gguf",
            notes="GLM-4.5V INT4 quantized"
        ),
    },
    
    # Mixtral variants (common large model)
    "Mixtral-8x7B": {
        "fp16": ModelBackendNames(
            ollama="mixtral:8x7b",
            vllm="mistralai/Mixtral-8x7B-Instruct-v0.1",
            llamacpp="models/mixtral-8x7b.gguf",
            notes="Mixtral 8x7B base model"
        ),
        "int8": ModelBackendNames(
            ollama="mixtral:8x7b",
            vllm="mistralai/Mixtral-8x7B-Instruct-v0.1",
            llamacpp="models/mixtral-8x7b-q8_0.gguf",
            notes="Mixtral INT8 quantized"
        ),
        "int4": ModelBackendNames(
            ollama="mixtral:8x7b",
            vllm="mistralai/Mixtral-8x7B-Instruct-v0.1",
            llamacpp="models/mixtral-8x7b-q4_0.gguf",
            notes="Mixtral INT4 quantized"
        ),
    },
}


def get_model_names(model_family: str, quantization: str) -> Optional[ModelBackendNames]:
    """Get model names for a specific model family and quantization."""
    if model_family not in MODEL_BACKEND_DB:
        return None
    
    quantizations = MODEL_BACKEND_DB[model_family]
    return quantizations.get(quantization, quantizations.get("fp16"))


def list_available_models_for_size(size: str) -> List[Tuple[str, str]]:
    """List available models for a given size (e.g., '7B', '13B')."""
    available = []
    for model_name, quants in MODEL_BACKEND_DB.items():
        if size in model_name:
            for quant_type in quants.keys():
                available.append((model_name, quant_type))
    return available
