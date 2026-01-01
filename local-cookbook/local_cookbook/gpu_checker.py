"""GPU detection and VRAM checking module."""

import subprocess
import re
from typing import Dict, List, Optional, Tuple
from rich.console import Console

console = Console()


class GPUInfo:
    """GPU information container."""
    
    def __init__(self):
        self.count = 0
        self.gpus: List[Dict[str, any]] = []
        self.total_vram_gb = 0.0
        self.has_nvidia = False
        
    def __repr__(self):
        return f"GPUInfo(count={self.count}, total_vram_gb={self.total_vram_gb:.2f})"


def check_nvidia_smi() -> bool:
    """Check if nvidia-smi is available."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_gpu_info_nvidia_smi() -> GPUInfo:
    """Get GPU information using nvidia-smi."""
    gpu_info = GPUInfo()
    
    if not check_nvidia_smi():
        return gpu_info
    
    try:
        # Get GPU count and basic info
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=count,name,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return gpu_info
        
        gpu_info.has_nvidia = True
        lines = result.stdout.strip().split('\n')
        
        for idx, line in enumerate(lines):
            if not line.strip():
                continue
                
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 3:
                gpu_name = parts[1]
                memory_total_mb = int(parts[2])
                memory_total_gb = memory_total_mb / 1024.0
                
                gpu_info.gpus.append({
                    'index': idx,
                    'name': gpu_name,
                    'vram_gb': memory_total_gb,
                    'vram_mb': memory_total_mb
                })
                gpu_info.total_vram_gb += memory_total_gb
        
        gpu_info.count = len(gpu_info.gpus)
        
        # Get detailed info for each GPU
        for idx, gpu in enumerate(gpu_info.gpus):
            try:
                result_detailed = subprocess.run(
                    [
                        "nvidia-smi",
                        "-i", str(idx),
                        "--query-gpu=driver_version,compute_cap",
                        "--format=csv,noheader"
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result_detailed.returncode == 0:
                    parts = result_detailed.stdout.strip().split(',')
                    if len(parts) >= 2:
                        gpu['driver_version'] = parts[0].strip()
                        gpu['compute_capability'] = parts[1].strip()
            except Exception:
                pass
        
    except Exception as e:
        console.print(f"[yellow]Warning: Could not get detailed GPU info: {e}[/yellow]")
    
    return gpu_info


def get_gpu_info() -> GPUInfo:
    """Get GPU information using the best available method."""
    gpu_info = get_gpu_info_nvidia_smi()
    
    # Fallback: try to detect via other methods
    if gpu_info.count == 0:
        # Check for GPU devices in /dev
        try:
            result = subprocess.run(
                ["ls", "/dev/nvidia*"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0 and result.stdout.strip():
                # GPUs detected but nvidia-smi might not be installed
                gpu_count = len([line for line in result.stdout.strip().split('\n') 
                                if 'nvidia' in line and 'card' in line])
                if gpu_count > 0:
                    gpu_info.has_nvidia = True
                    gpu_info.count = gpu_count
                    console.print("[yellow]GPUs detected but detailed info unavailable. Install nvidia-smi for full details.[/yellow]")
        except Exception:
            pass
    
    return gpu_info


def format_gpu_info(gpu_info: GPUInfo) -> str:
    """Format GPU information for display."""
    if gpu_info.count == 0:
        return "No GPUs detected"
    
    lines = [
        f"GPU Count: {gpu_info.count}",
        f"Total VRAM: {gpu_info.total_vram_gb:.2f} GB"
    ]
    
    for gpu in gpu_info.gpus:
        gpu_str = f"  GPU {gpu['index']}: {gpu['name']} ({gpu['vram_gb']:.2f} GB)"
        if 'driver_version' in gpu:
            gpu_str += f" [Driver: {gpu['driver_version']}]"
        lines.append(gpu_str)
    
    return "\n".join(lines)
