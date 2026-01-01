"""Ollama backend runner."""

import subprocess
import time
import json
from typing import Optional
from rich.console import Console

from .base import BackendRunner
from .config import (
    BenchmarkResult, ModelConfig, BackendType
)

console = Console()


class OllamaRunner(BackendRunner):
    """Runner for Ollama backend."""
    
    def __init__(self):
        super().__init__(BackendType.OLLAMA)
        self.api_base = "http://localhost:11434"
    
    def is_available(self) -> bool:
        """Check if Ollama is installed and running."""
        try:
            result = subprocess.run(
                ["ollama", "--version"],
                capture_output=True,
                timeout=2
            )
            if result.returncode != 0:
                return False
            
            # Check if server is running
            import requests
            try:
                response = requests.get(f"{self.api_base}/api/tags", timeout=2)
                return response.status_code == 200
            except Exception:
                return False
        except Exception:
            return False
    
    def initialize(self, model_config: ModelConfig) -> bool:
        """Initialize Ollama - ensure model is available."""
        if not self.is_available():
            console.print("[red]Ollama is not installed or not running.[/red]")
            console.print("[dim]Install from: https://ollama.ai[/dim]")
            return False
        
        if not model_config.ollama_model_name:
            console.print(f"[red]No Ollama model name configured for {model_config.name}[/red]")
            return False
        
        try:
            import requests
            
            # Check if model exists
            response = requests.get(f"{self.api_base}/api/tags", timeout=10)
            if response.status_code != 200:
                console.print("[red]Failed to connect to Ollama API[/red]")
                return False
            
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            
            if model_config.ollama_model_name not in model_names:
                console.print(f"[yellow]Model {model_config.ollama_model_name} not found. Pulling...[/yellow]")
                # Pull the model
                pull_response = requests.post(
                    f"{self.api_base}/api/pull",
                    json={"name": model_config.ollama_model_name},
                    timeout=600,  # 10 minutes for model pull
                    stream=True
                )
                
                if pull_response.status_code != 200:
                    console.print(f"[red]Failed to pull model: {model_config.ollama_model_name}[/red]")
                    return False
                
                # Stream pull progress
                for line in pull_response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if "status" in data:
                                console.print(f"[dim]{data['status']}[/dim]")
                        except Exception:
                            pass
            
            self.initialized = True
            console.print(f"[green]Ollama ready with model: {model_config.ollama_model_name}[/green]")
            return True
            
        except ImportError:
            console.print("[red]requests library required for Ollama. Install with: pip install requests[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Failed to initialize Ollama: {e}[/red]")
            return False
    
    def generate(self, prompt: str, model_config: ModelConfig) -> BenchmarkResult:
        """Generate response using Ollama."""
        if not self.initialized:
            return BenchmarkResult(
                backend=self.backend_type,
                model=model_config.name,
                prompt=prompt,
                output="",
                time_seconds=0,
                error="Ollama not initialized"
            )
        
        try:
            import requests
            
            start_time = time.time()
            
            # Call Ollama API
            response = requests.post(
                f"{self.api_base}/api/generate",
                json={
                    "model": model_config.ollama_model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 2048,
                        "temperature": 0.7
                    }
                },
                timeout=300
            )
            
            elapsed = time.time() - start_time
            
            if response.status_code != 200:
                return BenchmarkResult(
                    backend=self.backend_type,
                    model=model_config.name,
                    prompt=prompt,
                    output="",
                    time_seconds=elapsed,
                    error=f"API error: {response.status_code} - {response.text}"
                )
            
            data = response.json()
            output_text = data.get("response", "")
            
            # Extract token info if available
            eval_count = data.get("eval_count", None)
            prompt_eval_count = data.get("prompt_eval_count", None)
            tokens = None
            if eval_count is not None:
                tokens = eval_count
            
            return BenchmarkResult(
                backend=self.backend_type,
                model=model_config.name,
                prompt=prompt,
                output=output_text,
                time_seconds=elapsed,
                tokens_generated=tokens
            )
            
        except Exception as e:
            elapsed = time.time() - start_time if 'start_time' in locals() else 0
            return BenchmarkResult(
                backend=self.backend_type,
                model=model_config.name,
                prompt=prompt,
                output="",
                time_seconds=elapsed,
                error=str(e)
            )
    
    def cleanup(self):
        """Cleanup Ollama."""
        self.initialized = False
