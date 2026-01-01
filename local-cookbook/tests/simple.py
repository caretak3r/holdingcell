from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
import sys

console = Console()

def test_llm_server():
    """Test if LLM model hosted via llama.cpp is working."""
    base_url = "http://127.0.0.1:8000/v1"
    test_prompt = "What is 2+2? Please provide a brief answer."
    
    console.print(f"[bold blue]Testing LLM server at {base_url}[/bold blue]")
    console.print(f"[dim]Test prompt: {test_prompt}[/dim]\n")
    
    try:
        openai_client = OpenAI(
            base_url=base_url,
            api_key="sk-no-key-required",
        )
        
        console.print("[yellow]Sending request to LLM server...[/yellow]")
        completion = openai_client.chat.completions.create(
            model="ModelCloud/DeepSeek-R1-Distill-Qwen-7B-gptqmodel-4bit-vortex-v2",
            messages=[{"role": "user", "content": test_prompt}],
        )
        
        response = completion.choices[0].message.content
        
        console.print(Panel(
            f"[green]✓ LLM server is working![/green]\n\n"
            f"[bold]Response:[/bold]\n{response}",
            title="[green]Success[/green]",
            border_style="green"
        ))
        
        return True
        
    except Exception as e:
        console.print(Panel(
            f"[red]✗ LLM server test failed![/red]\n\n"
            f"[bold]Error:[/bold] {str(e)}",
            title="[red]Error[/red]",
            border_style="red"
        ))
        return False

if __name__ == "__main__":
    success = test_llm_server()
    sys.exit(0 if success else 1)
