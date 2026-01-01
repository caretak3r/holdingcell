"""Report generator for benchmark results."""

import json
from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text

from .config import BenchmarkResult, BackendType

console = Console()


class ReportGenerator:
    """Generate reports from benchmark results."""
    
    @staticmethod
    def generate_table_report(results: List[BenchmarkResult]) -> None:
        """Generate a rich table report."""
        console.print("\n[bold cyan]Benchmark Results[/bold cyan]")
        console.print("=" * 80)
        
        # Summary table
        table = Table(title="Performance Summary", box=box.ROUNDED, show_header=True)
        table.add_column("Backend", style="cyan", width=15)
        table.add_column("Status", width=12)
        table.add_column("Time (s)", justify="right", style="green", width=12)
        table.add_column("Tokens/s", justify="right", style="magenta", width=15)
        table.add_column("Tokens", justify="right", style="yellow", width=12)
        table.add_column("Output Length", justify="right", width=15)
        
        for result in results:
            status = "[red]Failed[/red]" if result.error else "[green]Success[/green]"
            time_str = f"{result.time_seconds:.2f}" if result.time_seconds > 0 else "N/A"
            tokens_per_sec = f"{result.tokens_per_second:.2f}" if result.tokens_per_second else "N/A"
            tokens_str = str(result.tokens_generated) if result.tokens_generated else "N/A"
            output_len = str(len(result.output))
            
            table.add_row(
                result.backend.value,
                status,
                time_str,
                tokens_per_sec,
                tokens_str,
                output_len
            )
        
        console.print(table)
        
        # Detailed output panel for each result
        console.print("\n[bold cyan]Detailed Outputs[/bold cyan]")
        console.print("=" * 80)
        
        for result in results:
            if result.error:
                panel_content = f"[red]Error: {result.error}[/red]"
                border_style = "red"
            else:
                panel_content = result.output[:2000]  # Limit to 2000 chars
                if len(result.output) > 2000:
                    panel_content += f"\n\n[dim]... (truncated, total length: {len(result.output)} chars)[/dim]"
                border_style = "green"
            
            title = f"{result.backend.value} - {result.model}"
            if not result.error:
                title += f" ({result.time_seconds:.2f}s)"
            
            console.print(Panel(
                panel_content,
                title=title,
                border_style=border_style,
                expand=False
            ))
            console.print()
    
    @staticmethod
    def generate_comparison_report(results: List[BenchmarkResult]) -> None:
        """Generate a comparison report highlighting differences."""
        successful = [r for r in results if not r.error]
        
        if not successful:
            console.print("[red]No successful benchmarks to compare[/red]")
            return
        
        console.print("\n[bold cyan]Comparison Analysis[/bold cyan]")
        console.print("=" * 80)
        
        # Speed comparison
        if len(successful) > 1:
            fastest = min(successful, key=lambda x: x.time_seconds)
            slowest = max(successful, key=lambda x: x.time_seconds)
            
            speedup = slowest.time_seconds / fastest.time_seconds if fastest.time_seconds > 0 else 0
            
            console.print(f"\n[bold]Speed Comparison:[/bold]")
            console.print(f"  Fastest: [green]{fastest.backend.value}[/green] ({fastest.time_seconds:.2f}s)")
            console.print(f"  Slowest: [red]{slowest.backend.value}[/red] ({slowest.time_seconds:.2f}s)")
            console.print(f"  Speedup: [yellow]{speedup:.2f}x[/yellow]")
        
        # Token throughput comparison
        with_tokens = [r for r in successful if r.tokens_per_second]
        if len(with_tokens) > 1:
            fastest_tokens = max(with_tokens, key=lambda x: x.tokens_per_second)
            slowest_tokens = min(with_tokens, key=lambda x: x.tokens_per_second)
            
            throughput_speedup = (
                fastest_tokens.tokens_per_second / slowest_tokens.tokens_per_second
                if slowest_tokens.tokens_per_second > 0 else 0
            )
            
            console.print(f"\n[bold]Token Throughput Comparison:[/bold]")
            console.print(f"  Fastest: [green]{fastest_tokens.backend.value}[/green] ({fastest_tokens.tokens_per_second:.2f} tokens/s)")
            console.print(f"  Slowest: [red]{slowest_tokens.backend.value}[/red] ({slowest_tokens.tokens_per_second:.2f} tokens/s)")
            console.print(f"  Speedup: [yellow]{throughput_speedup:.2f}x[/yellow]")
        
        # Advantages summary
        console.print(f"\n[bold]Backend Advantages:[/bold]")
        
        for result in successful:
            advantages = []
            if result.backend == BackendType.VLLM:
                advantages.append("High throughput")
                advantages.append("Batch processing")
                advantages.append("Continuous batching")
            elif result.backend == BackendType.LLAMACPP:
                advantages.append("Low memory usage")
                advantages.append("Fast inference")
                advantages.append("GGUF format")
            elif result.backend == BackendType.OLLAMA:
                advantages.append("Easy setup")
                advantages.append("Model management")
                advantages.append("API simplicity")
            
            console.print(f"  [cyan]{result.backend.value}:[/cyan] {', '.join(advantages)}")
    
    @staticmethod
    def generate_json_report(results: List[BenchmarkResult]) -> str:
        """Generate JSON report."""
        report_data = {
            "results": []
        }
        
        for result in results:
            report_data["results"].append({
                "backend": result.backend.value,
                "model": result.model,
                "prompt": result.prompt,
                "output": result.output,
                "time_seconds": result.time_seconds,
                "tokens_generated": result.tokens_generated,
                "tokens_per_second": result.tokens_per_second,
                "error": result.error,
                "output_length": len(result.output)
            })
        
        return json.dumps(report_data, indent=2)
