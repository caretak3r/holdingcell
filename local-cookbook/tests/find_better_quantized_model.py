#!/usr/bin/env python3
"""Find better quantized DeepSeek 3.1 models for faster inference."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import requests
import json

console = Console()


def find_better_quantized_models():
    """Find better quantized DeepSeek 3.1 models."""
    console.print("[bold cyan]Searching for better quantized DeepSeek-V3.1 models...[/bold cyan]\n")
    
    # Recommended quantization levels (better than Q3_K_XL)
    # Ordered by speed/quality balance
    recommended_quants = {
        "Q4_K_S": {"speed": "Very Fast", "quality": "Good", "priority": 1},
        "Q4_K_M": {"speed": "Fast", "quality": "Good", "priority": 2},
        "Q5_K_M": {"speed": "Medium", "quality": "Very Good", "priority": 3},
        "Q6_K": {"speed": "Medium-Slow", "quality": "Excellent", "priority": 4},
        "Q8_0": {"speed": "Slow", "quality": "Best", "priority": 5},
    }
    
    # Repositories to check
    repos_to_check = [
        "bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF",
        "unsloth/DeepSeek-V3.1-GGUF",
        "TheBloke/DeepSeek-V3.1-GGUF",
    ]
    
    found_models = []
    
    console.print("[yellow]Checking repositories...[/yellow]\n")
    
    for repo in repos_to_check:
        try:
            # Get repository info
            url = f"https://huggingface.co/api/models/{repo}"
            r = requests.get(url, timeout=15)
            
            if r.status_code == 200:
                # Try to get file listing
                files_url = f"https://huggingface.co/api/models/{repo}/tree/main"
                files_r = requests.get(files_url, timeout=15)
                
                if files_r.status_code == 200:
                    files = files_r.json()
                    gguf_files = [f for f in files if f.get('path', '').endswith('.gguf')]
                    
                    for file_info in gguf_files:
                        path = file_info.get('path', '')
                        size = file_info.get('size', 0)
                        
                        # Check for recommended quantization levels
                        for quant_name, quant_info in recommended_quants.items():
                            if quant_name in path and 'shard' not in path.lower():
                                # Single file (not sharded)
                                size_gb = size / (1024**3) if size else 0
                                found_models.append({
                                    "repo": repo,
                                    "file": path,
                                    "quantization": quant_name,
                                    "size_gb": size_gb,
                                    "speed": quant_info["speed"],
                                    "quality": quant_info["quality"],
                                    "priority": quant_info["priority"],
                                    "url": f"https://huggingface.co/{repo}/resolve/main/{path}",
                                })
                                break
        except Exception as e:
            console.print(f"[dim]Could not check {repo}: {e}[/dim]")
    
    # Sort by priority (lower is better)
    found_models.sort(key=lambda x: x["priority"])
    
    # Display results
    if found_models:
        console.print(Panel(
            "[green]✓ Found better quantized models![/green]\n\n"
            "Your current model uses Q3_K_XL (3-bit) which is slow.\n"
            "These models will provide better speed and quality.",
            title="[green]Recommendations[/green]",
            border_style="green"
        ))
        
        table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
        table.add_column("Quantization", style="cyan", width=12)
        table.add_column("Speed", style="green", width=12)
        table.add_column("Quality", style="yellow", width=12)
        table.add_column("Size", style="magenta", width=10)
        table.add_column("Repository", style="blue", width=35)
        
        for model in found_models[:10]:  # Show top 10
            size_str = f"{model['size_gb']:.1f}GB" if model['size_gb'] > 0 else "N/A"
            repo_short = model['repo'].split('/')[-1][:30]
            
            table.add_row(
                model['quantization'],
                model['speed'],
                model['quality'],
                size_str,
                repo_short
            )
        
        console.print("\n")
        console.print(table)
        
        # Show download instructions for top recommendations
        console.print("\n[bold yellow]Top Recommendations:[/bold yellow]\n")
        
        for i, model in enumerate(found_models[:3], 1):
            console.print(f"[bold]{i}. {model['quantization']}[/bold] - {model['speed']} speed, {model['quality']} quality")
            console.print(f"   Repository: [cyan]{model['repo']}[/cyan]")
            console.print(f"   File: [dim]{model['file']}[/dim]")
            console.print(f"   Download: [blue]{model['url']}[/blue]\n")
        
        # Show usage instructions
        console.print(Panel(
            "[bold]How to use:[/bold]\n\n"
            "1. Download the recommended model file (Q4_K_M or Q4_K_S recommended)\n"
            "2. Place it in your models directory\n"
            "3. Update your llama.cpp server to use the new model\n"
            "4. Expected speed improvement: 2-5x faster than Q3_K_XL\n\n"
            "[bold]Example download command:[/bold]\n"
            f"wget -O models/deepseek-v3.1-q4_k_m.gguf '{found_models[0]['url']}'\n\n"
            "[bold]Or use huggingface-cli:[/bold]\n"
            f"huggingface-cli download {found_models[0]['repo'].split('/')[0]}/{found_models[0]['repo'].split('/')[1]} {found_models[0]['file']} --local-dir models/",
            title="[cyan]Usage Instructions[/cyan]",
            border_style="cyan"
        ))
        
        return found_models
    else:
        console.print(Panel(
            "[yellow]Could not automatically find models, but here are manual recommendations:[/yellow]\n\n"
            "[bold]Best options:[/bold]\n"
            "1. [cyan]bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF[/cyan]\n"
            "   - Look for Q4_K_M or Q4_K_S files\n"
            "   - URL: https://huggingface.co/bartowski/deepseek-ai_DeepSeek-V3.1-Base-GGUF\n\n"
            "2. [cyan]unsloth/DeepSeek-V3.1-GGUF[/cyan]\n"
            "   - Look for Q4_K_M, Q5_K_M, Q6_K, or Q8_0 files\n"
            "   - URL: https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF\n\n"
            "[bold]Quantization guide:[/bold]\n"
            "- Q4_K_S: Fastest, good quality (recommended for speed)\n"
            "- Q4_K_M: Fast, good quality (recommended)\n"
            "- Q5_K_M: Medium speed, very good quality\n"
            "- Q6_K: Slower, excellent quality\n"
            "- Q8_0: Slowest, best quality\n\n"
            "[red]Avoid Q3_K_XL[/red] - it's too aggressive and causes slowdowns",
            title="[yellow]Manual Recommendations[/yellow]",
            border_style="yellow"
        ))
        return []


if __name__ == "__main__":
    find_better_quantized_models()
