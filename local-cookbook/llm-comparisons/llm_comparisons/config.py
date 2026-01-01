"""Base classes and configuration for LLM comparisons."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum
import time


class BackendType(str, Enum):
    """Supported backend types."""
    VLLM = "vllm"
    LLAMACPP = "llama.cpp"
    OLLAMA = "ollama"


@dataclass
class BenchmarkResult:
    """Result from a single benchmark run."""
    backend: BackendType
    model: str
    prompt: str
    output: str
    time_seconds: float
    tokens_generated: Optional[int] = None
    tokens_per_second: Optional[float] = None
    error: Optional[str] = None
    setup_time_seconds: Optional[float] = None
    
    def __post_init__(self):
        """Calculate tokens per second if tokens are available."""
        if self.tokens_generated and self.time_seconds > 0:
            self.tokens_per_second = self.tokens_generated / self.time_seconds


@dataclass
class ModelConfig:
    """Configuration for a model."""
    name: str
    vllm_model_path: Optional[str] = None
    ollama_model_name: Optional[str] = None
    llamacpp_model_path: Optional[str] = None
    notes: str = ""


# Model configurations
MODEL_CONFIGS: Dict[str, ModelConfig] = {
    "deepseek-v3.1": ModelConfig(
        name="DeepSeek-V3.1",
        vllm_model_path="deepseek-ai/DeepSeek-V3.1",
        ollama_model_name="deepseek-v3.1",
        llamacpp_model_path=None,  # Will need to be configured
        notes="DeepSeek V3.1 model - default comparison model"
    ),
    "qwen-7b": ModelConfig(
        name="Qwen-7B",
        vllm_model_path="Qwen/Qwen-7B-Chat",
        ollama_model_name="qwen:7b",
        llamacpp_model_path=None,
        notes="Qwen 7B model"
    ),
    "gpt-oss": ModelConfig(
        name="GPT-OSS",
        vllm_model_path="meta-llama/Llama-2-7b-chat-hf",
        ollama_model_name="llama2:7b",
        llamacpp_model_path=None,
        notes="Open source GPT-style model"
    ),
}

# Default test prompt
DEFAULT_PROMPT = "build the game of life using python"
