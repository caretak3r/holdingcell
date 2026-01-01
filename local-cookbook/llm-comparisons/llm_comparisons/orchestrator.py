"""Benchmark orchestrator to run all backends."""

import time
from typing import List, Dict, Optional, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import (
    BenchmarkResult, ModelConfig, MODEL_CONFIGS, DEFAULT_PROMPT, BackendType
)
from .vllm_runner import VLLMRunner
from .llamacpp_runner import LlamaCppRunner
from .ollama_runner import OllamaRunner

console = Console()


class BenchmarkOrchestrator:
    """Orchestrates benchmarking across multiple backends."""
    
    def __init__(self):
        self.runners = {
            BackendType.VLLM: VLLMRunner(),
            BackendType.LLAMACPP: LlamaCppRunner(),
            BackendType.OLLAMA: OllamaRunner(),
        }
        self.results: List[BenchmarkResult] = []
    
    def check_available_backends(self) -> Dict[BackendType, bool]:
        """Check which backends are available."""
        available = {}
        for backend_type, runner in self.runners.items():
            available[backend_type] = runner.is_available()
        return available
    
    def run_benchmark(
        self,
        model_name: str = "deepseek-v3.1",
        prompt: str = DEFAULT_PROMPT,
        backends: Optional[List[BackendType]] = None
    ) -> List[BenchmarkResult]:
        """Run benchmark for specified model and backends."""
        if model_name not in MODEL_CONFIGS:
            console.print(f"[red]Unknown model: {model_name}[/red]")
            console.print(f"[yellow]Available models: {', '.join(MODEL_CONFIGS.keys())}[/yellow]")
            return []
        
        model_config = MODEL_CONFIGS[model_name]
        
        # Filter to available backends
        available = self.check_available_backends()
        if backends is None:
            backends = [bt for bt in BackendType if available.get(bt, False)]
        
        # Filter to only available backends
        backends = [bt for bt in backends if available.get(bt, False)]
        
        if not backends:
            console.print("[red]No available backends found![/red]")
            console.print("[yellow]Please install at least one of: vLLM, llama.cpp, or Ollama[/yellow]")
            return []
        
        console.print(f"\n[bold cyan]Running benchmarks for {model_config.name}[/bold cyan]")
        console.print(f"[dim]Prompt: {prompt[:80]}...[/dim]\n")
        
        results = []
        
        for backend_type in backends:
            runner = self.runners[backend_type]
            
            with console.status(f"[bold yellow]Initializing {backend_type.value}...[/bold yellow]"):
                if not runner.initialize(model_config):
                    console.print(f"[red]Failed to initialize {backend_type.value}[/red]")
                    continue
            
            try:
                console.print(f"[bold green]Running {backend_type.value}...[/bold green]")
                start_time = time.time()
                
                result = runner.generate(prompt, model_config)
                result.setup_time_seconds = time.time() - start_time - result.time_seconds
                
                results.append(result)
                
                if result.error:
                    console.print(f"[red]  Error: {result.error}[/red]")
                else:
                    console.print(f"[green]  Completed in {result.time_seconds:.2f}s[/green]")
                    if result.tokens_per_second:
                        console.print(f"[green]  Speed: {result.tokens_per_second:.2f} tokens/s[/green]")
                
            except Exception as e:
                console.print(f"[red]Error running {backend_type.value}: {e}[/red]")
            finally:
                runner.cleanup()
        
        self.results = results
        return results
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of benchmark results."""
        if not self.results:
            return {"error": "No results available"}
        
        successful = [r for r in self.results if not r.error]
        
        summary = {
            "total_backends": len(self.results),
            "successful_backends": len(successful),
            "failed_backends": len(self.results) - len(successful),
            "fastest": None,
            "slowest": None,
            "fastest_tokens_per_second": None,
            "results": {}
        }
        
        if successful:
            # Find fastest and slowest
            fastest = min(successful, key=lambda x: x.time_seconds)
            slowest = max(successful, key=lambda x: x.time_seconds)
            summary["fastest"] = fastest.backend.value
            summary["slowest"] = slowest.backend.value
            
            # Find fastest tokens per second
            with_tokens = [r for r in successful if r.tokens_per_second]
            if with_tokens:
                fastest_tokens = max(with_tokens, key=lambda x: x.tokens_per_second)
                summary["fastest_tokens_per_second"] = fastest_tokens.backend.value
            
            # Per-backend results
            for result in successful:
                summary["results"][result.backend.value] = {
                    "time_seconds": result.time_seconds,
                    "tokens_per_second": result.tokens_per_second,
                    "tokens_generated": result.tokens_generated,
                    "output_length": len(result.output)
                }
        
        return summary
