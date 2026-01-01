"""CPU and memory detection module."""

import psutil
import platform
import subprocess
from typing import Dict, Optional
from rich.console import Console

console = Console()


class CPUInfo:
    """CPU information container."""
    
    def __init__(self):
        self.physical_cores = 0
        self.logical_cores = 0
        self.model_name = "Unknown"
        self.architecture = platform.machine()
        self.frequency_mhz = 0.0
        self.max_frequency_mhz = 0.0
        
    def __repr__(self):
        return f"CPUInfo(physical={self.physical_cores}, logical={self.logical_cores}, model={self.model_name})"


class MemoryInfo:
    """Memory information container."""
    
    def __init__(self):
        self.total_gb = 0.0
        self.available_gb = 0.0
        self.used_gb = 0.0
        self.percent = 0.0
        
    def __repr__(self):
        return f"MemoryInfo(total={self.total_gb:.2f}GB, available={self.available_gb:.2f}GB)"


def get_cpu_info() -> CPUInfo:
    """Get CPU information."""
    cpu_info = CPUInfo()
    
    # Get core counts
    cpu_info.physical_cores = psutil.cpu_count(logical=False) or 0
    cpu_info.logical_cores = psutil.cpu_count(logical=True) or 0
    
    # Get CPU frequency
    try:
        freq = psutil.cpu_freq()
        if freq:
            cpu_info.frequency_mhz = freq.current or 0.0
            cpu_info.max_frequency_mhz = freq.max or 0.0
    except Exception:
        pass
    
    # Get CPU model name (platform-specific)
    try:
        if platform.system() == "Linux":
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line.lower():
                        cpu_info.model_name = line.split(":")[1].strip()
                        break
                    elif "Model name" in line:
                        cpu_info.model_name = line.split(":")[1].strip()
                        break
        elif platform.system() == "Darwin":  # macOS
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                cpu_info.model_name = result.stdout.strip()
    except Exception as e:
        console.print(f"[yellow]Warning: Could not get CPU model name: {e}[/yellow]")
    
    return cpu_info


def get_memory_info() -> MemoryInfo:
    """Get memory information."""
    memory_info = MemoryInfo()
    
    try:
        mem = psutil.virtual_memory()
        memory_info.total_gb = mem.total / (1024 ** 3)
        memory_info.available_gb = mem.available / (1024 ** 3)
        memory_info.used_gb = mem.used / (1024 ** 3)
        memory_info.percent = mem.percent
    except Exception as e:
        console.print(f"[yellow]Warning: Could not get memory info: {e}[/yellow]")
    
    return memory_info


def format_cpu_info(cpu_info: CPUInfo) -> str:
    """Format CPU information for display."""
    lines = [
        f"Model: {cpu_info.model_name}",
        f"Physical Cores: {cpu_info.physical_cores}",
        f"Logical Cores: {cpu_info.logical_cores}",
        f"Architecture: {cpu_info.architecture}"
    ]
    
    if cpu_info.frequency_mhz > 0:
        lines.append(f"Current Frequency: {cpu_info.frequency_mhz:.2f} MHz")
    if cpu_info.max_frequency_mhz > 0:
        lines.append(f"Max Frequency: {cpu_info.max_frequency_mhz:.2f} MHz")
    
    return "\n".join(lines)


def format_memory_info(memory_info: MemoryInfo) -> str:
    """Format memory information for display."""
    return (
        f"Total RAM: {memory_info.total_gb:.2f} GB\n"
        f"Available RAM: {memory_info.available_gb:.2f} GB\n"
        f"Used RAM: {memory_info.used_gb:.2f} GB ({memory_info.percent:.1f}%)"
    )
