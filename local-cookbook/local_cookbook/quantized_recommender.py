"""Quantized model recommendations based on system specs."""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from local_cookbook.gpu_checker import GPUInfo
from local_cookbook.cpu_checker import MemoryInfo
from local_cookbook.model_db import MODEL_BACKEND_DB, get_model_names

console = Console()


@dataclass
class QuantizedModelRecommendation:
    """Recommendation for a quantized model."""
    model_name: str
    base_size: str  # e.g., "7B", "13B", "30B"
    quantization: str  # e.g., "FP16", "INT8", "INT4", "GPTQ-4bit"
    estimated_vram_gb: float
    estimated_ram_gb: float
    quality_tradeoff: str  # "High", "Medium", "Low"
    notes: str = ""
    ollama_name: Optional[str] = None
    vllm_name: Optional[str] = None
    llamacpp_name: Optional[str] = None
    model_family: Optional[str] = None  # e.g., "Qwen-7B", "GLM-4.6"


# Model size estimates (approximate VRAM requirements)
# Base sizes are for FP16, quantization reduces by factor
MODEL_SIZE_ESTIMATES = {
    "7B": {"fp16": 14.0, "int8": 7.0, "int4": 4.0, "gptq-4bit": 4.5, "awq-4bit": 4.5},
    "13B": {"fp16": 26.0, "int8": 13.0, "int4": 7.0, "gptq-4bit": 7.5, "awq-4bit": 7.5},
    "30B": {"fp16": 60.0, "int8": 30.0, "int4": 15.0, "gptq-4bit": 16.0, "awq-4bit": 16.0},
    "65B": {"fp16": 130.0, "int8": 65.0, "int4": 33.0, "gptq-4bit": 35.0, "awq-4bit": 35.0},
    "67B": {"fp16": 140.0, "int8": 70.0, "int4": 35.0, "gptq-4bit": 35.0, "awq-4bit": 35.0},
    "70B": {"fp16": 140.0, "int8": 70.0, "int4": 36.0, "gptq-4bit": 38.0, "awq-4bit": 38.0},
}

# Map model families to their sizes for lookup
MODEL_FAMILY_TO_SIZE = {
    "Llama-2-7B": "7B",
    "Llama-2-13B": "13B",
    "Qwen-7B": "7B",
    "Qwen-14B": "13B",
    "DeepSeek-7B": "7B",
    "DeepSeek-30B": "30B",
    "DeepSeek-V3.1": "67B",
    "GLM-4.6": "7B",
    "GLM-4.6-9B": "13B",
    "GLM-4.5V": "13B",
    "Mixtral-8x7B": "13B",
}


def generate_quantized_recommendations(
    gpu_info: GPUInfo,
    memory_info: MemoryInfo,
    target_quality: str = "balanced"  # "best", "balanced", "minimal"
) -> List[QuantizedModelRecommendation]:
    """Generate quantized model recommendations based on available resources."""
    recommendations = []
    
    available_vram = gpu_info.total_vram_gb if gpu_info.count > 0 else 0
    available_ram = memory_info.total_gb
    
    # Quality tradeoffs
    quality_priorities = {
        "best": ["fp16", "int8", "gptq-4bit", "awq-4bit", "int4"],
        "balanced": ["gptq-4bit", "awq-4bit", "int8", "int4", "fp16"],
        "minimal": ["int4", "gptq-4bit", "awq-4bit", "int8", "fp16"]
    }
    
    quant_priority = quality_priorities.get(target_quality, quality_priorities["balanced"])
    
    # Generate recommendations for each model family
    for model_family, model_size in MODEL_FAMILY_TO_SIZE.items():
        if model_size not in MODEL_SIZE_ESTIMATES:
            continue
            
        quant_options = MODEL_SIZE_ESTIMATES[model_size]
        
        for quant_type in quant_priority:
            if quant_type not in quant_options:
                continue
            
            vram_needed = quant_options[quant_type]
            ram_needed = vram_needed * 1.2  # RAM typically needs 20% more overhead
            
            # Check if this fits
            if available_vram > 0:
                fits_vram = available_vram >= vram_needed
            else:
                fits_vram = False  # No GPU
            
            fits_ram = available_ram >= ram_needed
            
            if fits_vram or (not available_vram and fits_ram):
                # Get model names for this family and quantization
                model_names = get_model_names(model_family, quant_type)
                
                # Determine quality
                if quant_type == "fp16":
                    quality = "High"
                elif quant_type == "int8":
                    quality = "High-Medium"
                elif quant_type in ["gptq-4bit", "awq-4bit"]:
                    quality = "Medium"
                else:  # int4
                    quality = "Medium-Low"
                
                # Format quantization name
                quant_name = quant_type.upper().replace("-", "-")
                if quant_name == "GPTQ-4BIT":
                    quant_name = "GPTQ-4bit"
                elif quant_name == "AWQ-4BIT":
                    quant_name = "AWQ-4bit"
                
                notes = []
                if not fits_vram and available_vram > 0:
                    notes.append("May need CPU offloading")
                elif not fits_vram:
                    notes.append("CPU-only mode")
                
                if quant_type in ["gptq-4bit", "awq-4bit"]:
                    notes.append("Good balance of quality and speed")
                elif quant_type == "int4":
                    notes.append("Maximum compression, some quality loss")
                
                if model_names:
                    notes.append(model_names.notes)
                
                recommendation = QuantizedModelRecommendation(
                    model_name=model_family,
                    base_size=model_size,
                    quantization=quant_name,
                    estimated_vram_gb=vram_needed,
                    estimated_ram_gb=ram_needed,
                    quality_tradeoff=quality,
                    notes="; ".join(notes) if notes else "Recommended",
                    ollama_name=model_names.ollama if model_names else None,
                    vllm_name=model_names.vllm if model_names else None,
                    llamacpp_name=model_names.llamacpp if model_names else None,
                    model_family=model_family
                )
                
                recommendations.append(recommendation)
    
    # Sort by model size (largest first) then by VRAM requirements
    recommendations.sort(key=lambda x: (
        int(x.base_size.replace("B", "")),
        x.estimated_vram_gb
    ), reverse=True)
    
    return recommendations


def print_quantized_recommendations(
    gpu_info: GPUInfo,
    memory_info: MemoryInfo
):
    """Print quantized model recommendations."""
    console.print("\n[bold cyan]Quantized Model Recommendations[/bold cyan]")
    console.print("=" * 80)
    
    if gpu_info.count > 0:
        console.print(f"[bold]Available VRAM:[/bold] {gpu_info.total_vram_gb:.2f} GB")
        console.print(f"[bold]Available RAM:[/bold] {memory_info.total_gb:.2f} GB\n")
    else:
        console.print("[yellow]No GPU detected - recommendations are for CPU-only mode[/yellow]")
        console.print(f"[bold]Available RAM:[/bold] {memory_info.total_gb:.2f} GB\n")
    
    # Get recommendations for different quality targets
    for quality_target in ["balanced", "best"]:
        target_name = "Best Quality" if quality_target == "best" else "Balanced"
        recommendations = generate_quantized_recommendations(
            gpu_info, memory_info, quality_target
        )
        
        if not recommendations:
            continue
        
        console.print(f"[bold yellow]{target_name} Recommendations:[/bold yellow]")
        
        table = Table(box=box.ROUNDED, show_header=True)
        table.add_column("Model", style="cyan", width=20)
        table.add_column("Size", style="cyan", width=8)
        table.add_column("Quant", style="green", width=12)
        table.add_column("VRAM", style="magenta", width=10)
        table.add_column("Quality", width=12)
        
        # Show top 8 recommendations for each quality target
        for rec in recommendations[:8]:
            vram_str = f"{rec.estimated_vram_gb:.1f}GB"
            
            table.add_row(
                rec.model_family or rec.model_name,
                rec.base_size,
                rec.quantization,
                vram_str,
                rec.quality_tradeoff
            )
        
        console.print(table)
        
        # Show backend-specific names
        console.print(f"\n[bold]Backend-Specific Model Names:[/bold]")
        for rec in recommendations[:8]:
            backend_info = []
            if rec.ollama_name:
                backend_info.append(f"[cyan]Ollama:[/cyan] {rec.ollama_name}")
            if rec.vllm_name:
                backend_info.append(f"[green]vLLM:[/green] {rec.vllm_name}")
            if rec.llamacpp_name:
                backend_info.append(f"[yellow]llama.cpp:[/yellow] {rec.llamacpp_name}")
            
            if backend_info:
                console.print(f"  [bold]{rec.model_family or rec.model_name}[/bold] ({rec.quantization}):")
                for info in backend_info:
                    console.print(f"    ? {info}")
        
        console.print()
    
    # Maximum model size recommendation
    max_recs = generate_quantized_recommendations(gpu_info, memory_info, "minimal")
    if max_recs:
        max_model = max_recs[0]
        console.print(f"[bold green]Maximum Model Size You Can Run:[/bold green]")
        console.print(f"  ? {max_model.model_family or max_model.model_name} ({max_model.base_size}) with {max_model.quantization} quantization")
        console.print(f"  ? Requires ~{max_model.estimated_vram_gb:.1f} GB VRAM / {max_model.estimated_ram_gb:.1f} GB RAM")
        
        if max_model.ollama_name or max_model.vllm_name or max_model.llamacpp_name:
            console.print(f"\n  [bold]Pull commands:[/bold]")
            if max_model.ollama_name:
                console.print(f"    [cyan]Ollama:[/cyan] ollama pull {max_model.ollama_name}")
            if max_model.vllm_name:
                console.print(f"    [green]vLLM:[/green] Use model: {max_model.vllm_name}")
            if max_model.llamacpp_name:
                console.print(f"    [yellow]llama.cpp:[/yellow] Download: {max_model.llamacpp_name}")
        console.print()
