"""LLM requirements checker module."""

from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table

from local_cookbook.gpu_checker import GPUInfo
from local_cookbook.cpu_checker import CPUInfo, MemoryInfo

console = Console()


@dataclass
class LLMRequirement:
    """LLM system requirements."""
    name: str
    min_vram_gb: float
    recommended_vram_gb: float
    min_ram_gb: float
    recommended_ram_gb: float
    min_cpu_cores: int
    recommended_cpu_cores: int
    quantization_support: bool = True
    notes: str = ""


# LLM Requirements Database
LLM_REQUIREMENTS: Dict[str, LLMRequirement] = {
    "gpt-oss": LLMRequirement(
        name="GPT-OSS (Open Source GPT Models)",
        min_vram_gb=4.0,
        recommended_vram_gb=8.0,
        min_ram_gb=8.0,
        recommended_ram_gb=16.0,
        min_cpu_cores=4,
        recommended_cpu_cores=8,
        quantization_support=True,
        notes="7B models need ~8GB VRAM, 13B need ~16GB VRAM. Quantization reduces VRAM needs."
    ),
    "qwen": LLMRequirement(
        name="Qwen (Alibaba)",
        min_vram_gb=6.0,
        recommended_vram_gb=12.0,
        min_ram_gb=12.0,
        recommended_ram_gb=24.0,
        min_cpu_cores=4,
        recommended_cpu_cores=8,
        quantization_support=True,
        notes="Qwen-7B needs ~8GB VRAM, Qwen-14B needs ~16GB VRAM. Supports 4-bit quantization."
    ),
    "deepseek": LLMRequirement(
        name="DeepSeek",
        min_vram_gb=8.0,
        recommended_vram_gb=16.0,
        min_ram_gb=16.0,
        recommended_ram_gb=32.0,
        min_cpu_cores=6,
        recommended_cpu_cores=12,
        quantization_support=True,
        notes="DeepSeek-7B needs ~10GB VRAM, DeepSeek-67B needs ~80GB VRAM. Better with high VRAM."
    ),
    "glm-4.6": LLMRequirement(
        name="GLM-4.6 (Zhipu AI)",
        min_vram_gb=8.0,
        recommended_vram_gb=16.0,
        min_ram_gb=16.0,
        recommended_ram_gb=32.0,
        min_cpu_cores=6,
        recommended_cpu_cores=12,
        quantization_support=True,
        notes="GLM-4.6 is a large language model. Supports various quantization formats."
    ),
    "glm-4.5v": LLMRequirement(
        name="GLM-4.5V (Zhipu AI Vision)",
        min_vram_gb=12.0,
        recommended_vram_gb=20.0,
        min_ram_gb=20.0,
        recommended_ram_gb=40.0,
        min_cpu_cores=8,
        recommended_cpu_cores=16,
        quantization_support=True,
        notes="GLM-4.5V is a vision-language model. Requires more VRAM due to vision processing."
    ),
}


def check_llm_compatibility(
    gpu_info: GPUInfo,
    cpu_info: CPUInfo,
    memory_info: MemoryInfo,
    llm_name: str
) -> Dict[str, Any]:
    """Check if system meets requirements for a specific LLM."""
    if llm_name not in LLM_REQUIREMENTS:
        return {
            "compatible": False,
            "error": f"Unknown LLM: {llm_name}"
        }
    
    req = LLM_REQUIREMENTS[llm_name]
    results = {
        "llm_name": req.name,
        "requirements": req,
        "checks": {},
        "compatible": True,
        "recommended": True,
        "warnings": []
    }
    
    # Check VRAM
    if gpu_info.count > 0:
        vram_check = "pass"
        if gpu_info.total_vram_gb < req.min_vram_gb:
            vram_check = "fail"
            results["compatible"] = False
            results["warnings"].append(
                f"Insufficient VRAM: {gpu_info.total_vram_gb:.2f}GB < {req.min_vram_gb}GB minimum"
            )
        elif gpu_info.total_vram_gb < req.recommended_vram_gb:
            vram_check = "warning"
            results["recommended"] = False
            results["warnings"].append(
                f"VRAM below recommended: {gpu_info.total_vram_gb:.2f}GB < {req.recommended_vram_gb}GB recommended"
            )
        
        results["checks"]["vram"] = {
            "status": vram_check,
            "available": gpu_info.total_vram_gb,
            "minimum": req.min_vram_gb,
            "recommended": req.recommended_vram_gb
        }
    else:
        results["checks"]["vram"] = {
            "status": "no_gpu",
            "available": 0,
            "minimum": req.min_vram_gb,
            "recommended": req.recommended_vram_gb
        }
        results["warnings"].append("No GPU detected - LLM will run on CPU (much slower)")
        # CPU-only mode requirements are more lenient
        if memory_info.total_gb < req.min_ram_gb * 1.5:
            results["compatible"] = False
    
    # Check RAM
    ram_check = "pass"
    if memory_info.total_gb < req.min_ram_gb:
        ram_check = "fail"
        results["compatible"] = False
        results["warnings"].append(
            f"Insufficient RAM: {memory_info.total_gb:.2f}GB < {req.min_ram_gb}GB minimum"
        )
    elif memory_info.total_gb < req.recommended_ram_gb:
        ram_check = "warning"
        results["recommended"] = False
        results["warnings"].append(
            f"RAM below recommended: {memory_info.total_gb:.2f}GB < {req.recommended_ram_gb}GB recommended"
        )
    
    results["checks"]["ram"] = {
        "status": ram_check,
        "available": memory_info.total_gb,
        "minimum": req.min_ram_gb,
        "recommended": req.recommended_ram_gb
    }
    
    # Check CPU cores
    cpu_check = "pass"
    if cpu_info.physical_cores < req.min_cpu_cores:
        cpu_check = "warning"
        results["recommended"] = False
        results["warnings"].append(
            f"CPU cores below recommended: {cpu_info.physical_cores} < {req.recommended_cpu_cores} recommended"
        )
    
    results["checks"]["cpu"] = {
        "status": cpu_check,
        "available": cpu_info.physical_cores,
        "minimum": req.min_cpu_cores,
        "recommended": req.recommended_cpu_cores
    }
    
    return results


def generate_compatibility_report(
    gpu_info: GPUInfo,
    cpu_info: CPUInfo,
    memory_info: MemoryInfo,
    llm_names: List[str] = None
) -> Dict[str, Any]:
    """Generate compatibility report for all or specified LLMs."""
    if llm_names is None:
        llm_names = list(LLM_REQUIREMENTS.keys())
    
    report = {
        "system_info": {
            "gpu": {
                "count": gpu_info.count,
                "total_vram_gb": gpu_info.total_vram_gb,
                "gpus": gpu_info.gpus
            },
            "cpu": {
                "physical_cores": cpu_info.physical_cores,
                "logical_cores": cpu_info.logical_cores,
                "model": cpu_info.model_name,
                "architecture": cpu_info.architecture
            },
            "memory": {
                "total_gb": memory_info.total_gb,
                "available_gb": memory_info.available_gb,
                "used_percent": memory_info.percent
            }
        },
        "llm_compatibility": {}
    }
    
    for llm_name in llm_names:
        if llm_name in LLM_REQUIREMENTS:
            report["llm_compatibility"][llm_name] = check_llm_compatibility(
                gpu_info, cpu_info, memory_info, llm_name
            )
    
    return report
