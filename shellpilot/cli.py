import typer
from pathlib import Path

app = typer.Typer()

def get_assistant_name():
    path = Path(__file__).parent.parent / "assistant_name.txt"
    if path.exists():
        return path.read_text().strip().capitalize() + "Buddy"
    return "Shellpilot"



@app.command()
def hello(chat: str = typer.Argument(None, help="Say something to your assistant.")) -> None:
    assistant = get_assistant_name()
    if chat:
        typer.echo(f"🧠 {assistant} says: I heard you say '{chat}'!")
    else:
        typer.echo(f"👋 Hello! I’m {assistant}, your terminal assistant.")

@app.command()
def enable():
    Path.home().joinpath(".shellpilot_enabled").touch()
    typer.echo(f"✅ {get_assistant_name()} is now enabled.")
    
@app.command()
def disable():
    flag = Path.home().joinpath(".shellpilot_enabled")
    if flag.exists():
        flag.unlink()
        typer.echo(f"❌ {get_assistant_name()} has been disabled.")
    else:
        typer.echo(f"⚠️ Assistant already disabled.")

if __name__ == "__main__":
    app()