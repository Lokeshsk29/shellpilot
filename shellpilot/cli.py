import typer
from pathlib import Path

app = typer.Typer()

def get_assistant_name():
    path = Path(__file__).parent.parent / "assistant_name.txt"
    if path.exists():
        return path.read_text().strip().capitalize() + "Buddy"
    return "Shellpilot"



@app.command()
def hello():
    typer.echo(f"👋 Hello! I’m {get_assistant_name()}, your terminal assistant.")
    
    
if __name__ == "__main__":
    app()