"""Main CLI module for local-cookbook."""

import json
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text

from local_cookbook.gpu_checker import get_gpu_info, format_gpu_info
from local_cookbook.cpu_checker import (
    get_cpu_info,
    get_memory_info,
    format_cpu_info,
    format_memory_info
)
from local_cookbook.llm_checker import (
    generate_compatibility_report,
    LLM_REQUIREMENTS
)
from local_cookbook.quantized_recommender import print_quantized_recommendations

console = Console()


def print_system_info(gpu_info, cpu_info, memory_info, detailed=False):
    """Print system information."""
    console.print("\n[bold cyan]System Information[/bold cyan]")
    console.print("=" * 60)
    
    # GPU Info
    console.print("\n[bold yellow]GPU Information[/bold yellow]")
    if gpu_info.count > 0:
        table = Table(box=box.ROUNDED)
        table.add_column("GPU", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("VRAM", style="magenta")
        
        for gpu in gpu_info.gpus:
            gpu_label = f"GPU {gpu['index']}"
            vram_str = f"{gpu['vram_gb']:.2f} GB"
            if detailed and 'driver_version' in gpu:
                gpu_label += f"\n[dim](Driver: {gpu['driver_version']})[/dim]"
            table.add_row(gpu_label, gpu['name'], vram_str)
        
        table.add_row("Total", "", f"{gpu_info.total_vram_gb:.2f} GB")
        console.print(table)
    else:
        console.print("[yellow]No GPUs detected[/yellow]")
    
    # CPU Info
    console.print("\n[bold yellow]CPU Information[/bold yellow]")
    table = Table(box=box.ROUNDED)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Model", cpu_info.model_name)
    table.add_row("Physical Cores", str(cpu_info.physical_cores))
    table.add_row("Logical Cores", str(cpu_info.logical_cores))
    table.add_row("Architecture", cpu_info.architecture)
    if cpu_info.frequency_mhz > 0:
        table.add_row("Frequency", f"{cpu_info.frequency_mhz:.2f} MHz")
    console.print(table)
    
    # Memory Info
    console.print("\n[bold yellow]Memory Information[/bold yellow]")
    table = Table(box=box.ROUNDED)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total RAM", f"{memory_info.total_gb:.2f} GB")
    table.add_row("Available RAM", f"{memory_info.available_gb:.2f} GB")
    table.add_row("Used RAM", f"{memory_info.used_gb:.2f} GB ({memory_info.percent:.1f}%)")
    console.print(table)


def print_llm_compatibility(report, detailed=False):
    """Print LLM compatibility report."""
    console.print("\n[bold cyan]LLM Compatibility Report[/bold cyan]")
    console.print("=" * 60)
    
    for llm_name, compat_info in report["llm_compatibility"].items():
        req = compat_info["requirements"]
        
        # Status indicator
        if compat_info["compatible"] and compat_info["recommended"]:
            status_icon = "[green]?[/green]"
            status_text = "[green]Compatible (Recommended)[/green]"
        elif compat_info["compatible"]:
            status_icon = "[yellow]?[/yellow]"
            status_text = "[yellow]Compatible (Below Recommended)[/yellow]"
        else:
            status_icon = "[red]?[/red]"
            status_text = "[red]Not Compatible[/red]"
        
        panel_title = f"{status_icon} {req.name} - {status_text}"
        
        # Build content
        content_lines = []
        
        # Requirements table
        table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
        table.add_column("Resource", style="cyan", width=20)
        table.add_column("Minimum", style="yellow", width=15)
        table.add_column("Recommended", style="green", width=15)
        table.add_column("Available", style="magenta", width=15)
        table.add_column("Status", width=12)
        
        # VRAM row
        vram_status = compat_info["checks"]["vram"]["status"]
        if vram_status == "pass":
            status_col = "[green]? Pass[/green]"
        elif vram_status == "warning":
            status_col = "[yellow]? Warning[/yellow]"
        elif vram_status == "fail":
            status_col = "[red]? Fail[/red]"
        else:
            status_col = "[dim]No GPU[/dim]"
        
        table.add_row(
            "VRAM",
            f"{compat_info['checks']['vram']['minimum']:.1f} GB",
            f"{compat_info['checks']['vram']['recommended']:.1f} GB",
            f"{compat_info['checks']['vram']['available']:.1f} GB",
            status_col
        )
        
        # RAM row
        ram_status = compat_info["checks"]["ram"]["status"]
        if ram_status == "pass":
            status_col = "[green]? Pass[/green]"
        elif ram_status == "warning":
            status_col = "[yellow]? Warning[/yellow]"
        else:
            status_col = "[red]? Fail[/red]"
        
        table.add_row(
            "RAM",
            f"{compat_info['checks']['ram']['minimum']:.1f} GB",
            f"{compat_info['checks']['ram']['recommended']:.1f} GB",
            f"{compat_info['checks']['ram']['available']:.1f} GB",
            status_col
        )
        
        # CPU row
        cpu_status = compat_info["checks"]["cpu"]["status"]
        if cpu_status == "pass":
            status_col = "[green]? Pass[/green]"
        else:
            status_col = "[yellow]? Warning[/yellow]"
        
        table.add_row(
            "CPU Cores",
            str(compat_info['checks']['cpu']['minimum']),
            str(compat_info['checks']['cpu']['recommended']),
            str(compat_info['checks']['cpu']['available']),
            status_col
        )
        
        # Print table separately, then add text content
        console.print(Panel(table, title=panel_title, border_style="blue"))
        
        # Warnings
        if compat_info["warnings"]:
            console.print("\n[bold yellow]Warnings:[/bold yellow]")
            for warning in compat_info["warnings"]:
                console.print(f"  ? {warning}")
        
        # Notes
        if req.notes:
            console.print(f"\n[bold dim]Notes:[/bold dim] {req.notes}")
        
        console.print()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Local Cookbook - System Resource Checker and LLM Compatibility Analyzer."""
    pass


@cli.command()
@click.option("--detailed", "-d", is_flag=True, help="Show detailed information")
@click.option("--json", "output_json", is_flag=True, help="Output in JSON format")
@click.option("--llm", multiple=True, type=click.Choice(["gpt-oss", "qwen", "deepseek", "glm-4.6", "glm-4.5v"]), 
              help="Check specific LLM(s) only")
def check(detailed, output_json, llm):
    """Check system resources and LLM compatibility."""
    console.print("[bold green]Local Cookbook - System Check[/bold green]")
    console.print("[dim]Gathering system information...[/dim]\n")
    
    # Gather system info
    gpu_info = get_gpu_info()
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    
    # Generate compatibility report
    llm_names = list(llm) if llm else None
    report = generate_compatibility_report(gpu_info, cpu_info, memory_info, llm_names)
    
    if output_json:
        # JSON output
        console.print(json.dumps(report, indent=2, default=str))
    else:
        # Rich formatted output
        print_system_info(gpu_info, cpu_info, memory_info, detailed)
        print_llm_compatibility(report, detailed)
        
        # Quantized model recommendations
        print_quantized_recommendations(gpu_info, memory_info)
        
        # Summary
        console.print("\n[bold cyan]Summary[/bold cyan]")
        console.print("=" * 60)
        
        compatible_count = sum(1 for c in report["llm_compatibility"].values() if c["compatible"])
        total_count = len(report["llm_compatibility"])
        
        console.print(f"[green]Compatible LLMs: {compatible_count}/{total_count}[/green]")
        
        if compatible_count > 0:
            console.print("\n[bold]Recommended LLMs for your system:[/bold]")
            for llm_name, compat_info in report["llm_compatibility"].items():
                if compat_info["compatible"] and compat_info["recommended"]:
                    console.print(f"  ? [green]{compat_info['llm_name']}[/green]")


@cli.command()
def list_llms():
    """List all supported LLMs and their requirements."""
    console.print("[bold cyan]Supported LLMs and Requirements[/bold cyan]")
    console.print("=" * 60)
    
    for llm_name, req in LLM_REQUIREMENTS.items():
        panel_content = f"""
[bold]Minimum Requirements:[/bold]
  ? VRAM: {req.min_vram_gb} GB (recommended: {req.recommended_vram_gb} GB)
  ? RAM: {req.min_ram_gb} GB (recommended: {req.recommended_ram_gb} GB)
  ? CPU Cores: {req.min_cpu_cores} (recommended: {req.recommended_cpu_cores})
  ? Quantization Support: {'Yes' if req.quantization_support else 'No'}

[dim]{req.notes}[/dim]
        """
        console.print(Panel(panel_content.strip(), title=f"[bold]{req.name}[/bold]", border_style="blue"))
        console.print()


if __name__ == "__main__":
    cli()
