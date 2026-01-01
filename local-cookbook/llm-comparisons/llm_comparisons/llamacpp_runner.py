"""llama.cpp backend runner."""

import subprocess
import time
import os
from typing import Optional
from rich.console import Console

from .base import BackendRunner
from .config import (
    BenchmarkResult, ModelConfig, BackendType
)

console = Console()


class LlamaCppRunner(BackendRunner):
    """Runner for llama.cpp backend."""
    
    def __init__(self):
        super().__init__(BackendType.LLAMACPP)
        self.llamacpp_binary: Optional[str] = None
    
    def _find_llamacpp_binary(self) -> Optional[str]:
        """Find llama.cpp binary."""
        possible_paths = [
            "llama-cli",
            "llama",
            "llama.cpp/llama-cli",
            "llama.cpp/build/bin/llama-cli",
            os.path.expanduser("~/llama.cpp/llama-cli"),
            os.path.expanduser("~/llama.cpp/build/bin/llama-cli"),
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run(
                    [path, "--help"],
                    capture_output=True,
                    timeout=2
                )
                if result.returncode == 0:
                    return path
            except Exception:
                continue
        
        return None
    
    def is_available(self) -> bool:
        """Check if llama.cpp is available."""
        self.llamacpp_binary = self._find_llamacpp_binary()
        return self.llamacpp_binary is not None
    
    def initialize(self, model_config: ModelConfig) -> bool:
        """Initialize llama.cpp."""
        if not self.is_available():
            console.print("[yellow]llama.cpp binary not found. Please install llama.cpp first.[/yellow]")
            console.print("[dim]Install from: https://github.com/ggerganov/llama.cpp[/dim]")
            return False
        
        if not model_config.llamacpp_model_path:
            console.print(f"[yellow]No llama.cpp model path configured. Using default search locations.[/yellow]")
            # Try to find model automatically
            possible_paths = [
                f"models/{model_config.name.lower().replace('-', '_')}.gguf",
                f"~/models/{model_config.name.lower().replace('-', '_')}.gguf",
                f"~/.local/share/llama.cpp/models/{model_config.name.lower().replace('-', '_')}.gguf",
            ]
            for path in possible_paths:
                expanded = os.path.expanduser(path)
                if os.path.exists(expanded):
                    model_config.llamacpp_model_path = expanded
                    break
        
        if not model_config.llamacpp_model_path or not os.path.exists(model_config.llamacpp_model_path):
            console.print(f"[red]Model file not found: {model_config.llamacpp_model_path}[/red]")
            console.print("[dim]Please download a GGUF model file and configure the path.[/dim]")
            return False
        
        self.initialized = True
        return True
    
    def generate(self, prompt: str, model_config: ModelConfig) -> BenchmarkResult:
        """Generate response using llama.cpp."""
        if not self.initialized or not self.llamacpp_binary:
            return BenchmarkResult(
                backend=self.backend_type,
                model=model_config.name,
                prompt=prompt,
                output="",
                time_seconds=0,
                error="llama.cpp not initialized"
            )
        
        if not model_config.llamacpp_model_path:
            return BenchmarkResult(
                backend=self.backend_type,
                model=model_config.name,
                prompt=prompt,
                output="",
                time_seconds=0,
                error="No model path configured"
            )
        
        try:
            start_time = time.time()
            
            # Run llama.cpp
            cmd = [
                self.llamacpp_binary,
                "-m", model_config.llamacpp_model_path,
                "-p", prompt,
                "-n", "2048",  # max tokens
                "-t", "4",  # threads
                "--temp", "0.7",
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            elapsed = time.time() - start_time
            
            if result.returncode != 0:
                return BenchmarkResult(
                    backend=self.backend_type,
                    model=model_config.name,
                    prompt=prompt,
                    output="",
                    time_seconds=elapsed,
                    error=f"llama.cpp error: {result.stderr}"
                )
            
            output_text = result.stdout.strip()
            # Try to extract token count from output if available
            tokens = None
            if "tokens" in result.stderr.lower():
                # Parse token count from stderr if available
                import re
                match = re.search(r'(\d+)\s*tokens', result.stderr)
                if match:
                    tokens = int(match.group(1))
            
            return BenchmarkResult(
                backend=self.backend_type,
                model=model_config.name,
                prompt=prompt,
                output=output_text,
                time_seconds=elapsed,
                tokens_generated=tokens
            )
            
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            return BenchmarkResult(
                backend=self.backend_type,
                model=model_config.name,
                prompt=prompt,
                output="",
                time_seconds=elapsed,
                error="Timeout after 300 seconds"
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
        """Cleanup llama.cpp."""
        self.initialized = False
