"""Main CLI for LLM comparisons."""

import click
import json
from rich.console import Console
from rich.panel import Panel

from .config import (
    MODEL_CONFIGS, DEFAULT_PROMPT, BackendType
)
from .orchestrator import BenchmarkOrchestrator
from .reporter import ReportGenerator

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """LLM Backend Comparison Tool - Benchmark vLLM, llama.cpp, and Ollama."""
    pass


@cli.command()
@click.option("--model", "-m", default="deepseek-v3.1",
              type=click.Choice(list(MODEL_CONFIGS.keys())),
              help="Model to benchmark")
@click.option("--prompt", "-p", default=DEFAULT_PROMPT,
              help="Prompt to use for benchmarking")
@click.option("--backend", "-b", multiple=True,
              type=click.Choice(["vllm", "llama.cpp", "ollama"]),
              help="Backend(s) to test (can specify multiple)")
@click.option("--json", "output_json", is_flag=True,
              help="Output results as JSON")
@click.option("--no-comparison", is_flag=True,
              help="Skip comparison analysis")
def benchmark(model, prompt, backend, output_json, no_comparison):
    """Run benchmark comparison across backends."""
    console.print("[bold green]LLM Backend Comparison Tool[/bold green]")
    console.print("[dim]Benchmarking LLM backends...[/dim]\n")
    
    orchestrator = BenchmarkOrchestrator()
    
    # Check available backends
    available = orchestrator.check_available_backends()
    console.print("[bold cyan]Available Backends:[/bold cyan]")
    for backend_type, is_avail in available.items():
        status = "[green]?[/green]" if is_avail else "[red]?[/red]"
        console.print(f"  {status} {backend_type.value}")
    
    # Convert backend strings to BackendType
    backend_types = None
    if backend:
        backend_types = []
        backend_map = {
            "vllm": BackendType.VLLM,
            "llama.cpp": BackendType.LLAMACPP,
            "ollama": BackendType.OLLAMA
        }
        for b in backend:
            if b in backend_map:
                backend_types.append(backend_map[b])
    
    # Run benchmarks
    results = orchestrator.run_benchmark(
        model_name=model,
        prompt=prompt,
        backends=backend_types
    )
    
    if not results:
        console.print("\n[red]No benchmarks completed successfully[/red]")
        return
    
    # Generate reports
    if output_json:
        json_report = ReportGenerator.generate_json_report(results)
        console.print(json_report)
    else:
        ReportGenerator.generate_table_report(results)
        if not no_comparison:
            ReportGenerator.generate_comparison_report(results)
        
        # Save JSON to file as well
        import os
        output_file = "benchmark_results.json"
        with open(output_file, "w") as f:
            f.write(ReportGenerator.generate_json_report(results))
        console.print(f"\n[green]Results saved to {output_file}[/green]")


@cli.command()
def list_models():
    """List available models."""
    console.print("[bold cyan]Available Models[/bold cyan]")
    console.print("=" * 60)
    
    for model_key, config in MODEL_CONFIGS.items():
        panel_content = f"""
[bold]Model Name:[/bold] {config.name}

[bold]Configuration:[/bold]
  ? vLLM: {config.vllm_model_path or 'Not configured'}
  ? Ollama: {config.ollama_model_name or 'Not configured'}
  ? llama.cpp: {config.llamacpp_model_path or 'Not configured'}

[dim]{config.notes}[/dim]
        """
        console.print(Panel(panel_content.strip(), title=f"[bold]{model_key}[/bold]", border_style="blue"))
        console.print()


@cli.command()
def check_backends():
    """Check which backends are available."""
    orchestrator = BenchmarkOrchestrator()
    available = orchestrator.check_available_backends()
    
    console.print("[bold cyan]Backend Availability Check[/bold cyan]")
    console.print("=" * 60)
    
    for backend_type, is_avail in available.items():
        status = "[green]? Available[/green]" if is_avail else "[red]? Not Available[/red]"
        console.print(f"{backend_type.value}: {status}")
        
        if not is_avail:
            if backend_type == BackendType.VLLM:
                console.print("  [dim]Install with: pip install vllm[/dim]")
            elif backend_type == BackendType.OLLAMA:
                console.print("  [dim]Install from: https://ollama.ai[/dim]")
            elif backend_type == BackendType.LLAMACPP:
                console.print("  [dim]Install from: https://github.com/ggerganov/llama.cpp[/dim]")


if __name__ == "__main__":
    cli()
