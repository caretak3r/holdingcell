"""Base backend runner interface."""

from abc import ABC, abstractmethod
from typing import Optional
from .config import BenchmarkResult, ModelConfig, BackendType


class BackendRunner(ABC):
    """Base class for backend runners."""
    
    def __init__(self, backend_type: BackendType):
        self.backend_type = backend_type
        self.initialized = False
    
    @abstractmethod
    def initialize(self, model_config: ModelConfig) -> bool:
        """Initialize the backend with the given model."""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, model_config: ModelConfig) -> BenchmarkResult:
        """Generate a response for the given prompt."""
        pass
    
    @abstractmethod
    def cleanup(self):
        """Clean up resources."""
        pass
    
    def is_available(self) -> bool:
        """Check if this backend is available on the system."""
        return False
