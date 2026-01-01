"""vLLM backend runner."""

import subprocess
import time
import json
import os
from typing import Optional
from rich.console import Console

from .base import BackendRunner
from .config import (
    BenchmarkResult, ModelConfig, BackendType
)

console = Console()


class VLLMRunner(BackendRunner):
    """Runner for vLLM backend."""
    
    def __init__(self):
        super().__init__(BackendType.VLLM)
        self.process: Optional[subprocess.Popen] = None
        self.api_port = 8000
        self.api_base = f"http://localhost:{self.api_port}"
    
    def is_available(self) -> bool:
        """Check if vLLM is installed."""
        try:
            result = subprocess.run(
                ["python", "-c", "import vllm"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def initialize(self, model_config: ModelConfig) -> bool:
        """Initialize vLLM server."""
        if not self.is_available():
            console.print("[red]vLLM is not installed. Install with: pip install vllm[/red]")
            return False
        
        if not model_config.vllm_model_path:
            console.print(f"[red]No vLLM model path configured for {model_config.name}[/red]")
            return False
        
        try:
            console.print(f"[yellow]Starting vLLM server for {model_config.name}...[/yellow]")
            
            # Start vLLM server in background
            cmd = [
                "python", "-m", "vllm.entrypoints.openai.api_server",
                "--model", model_config.vllm_model_path,
                "--port", str(self.api_port),
                "--host", "127.0.0.1"
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to be ready
            import requests
            max_wait = 120  # 2 minutes
            elapsed = 0
            while elapsed < max_wait:
                try:
                    response = requests.get(f"{self.api_base}/health", timeout=2)
                    if response.status_code == 200:
                        self.initialized = True
                        console.print("[green]vLLM server started successfully[/green]")
                        return True
                except Exception:
                    time.sleep(2)
                    elapsed += 2
            
            console.print("[red]vLLM server failed to start[/red]")
            return False
            
        except ImportError:
            console.print("[red]requests library required for vLLM. Install with: pip install requests[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Failed to initialize vLLM: {e}[/red]")
            return False
    
    def generate(self, prompt: str, model_config: ModelConfig) -> BenchmarkResult:
        """Generate response using vLLM."""
        if not self.initialized:
            return BenchmarkResult(
                backend=self.backend_type,
                model=model_config.name,
                prompt=prompt,
                output="",
                time_seconds=0,
                error="vLLM not initialized"
            )
        
        try:
            import requests
            
            start_time = time.time()
            
            # Call vLLM API
            response = requests.post(
                f"{self.api_base}/v1/completions",
                json={
                    "model": model_config.vllm_model_path,
                    "prompt": prompt,
                    "max_tokens": 2048,
                    "temperature": 0.7
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
            output_text = data.get("choices", [{}])[0].get("text", "")
            tokens = data.get("usage", {}).get("total_tokens", None)
            
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
        """Stop vLLM server."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=10)
            except Exception:
                self.process.kill()
            self.process = None
            self.initialized = False
            console.print("[yellow]vLLM server stopped[/yellow]")
