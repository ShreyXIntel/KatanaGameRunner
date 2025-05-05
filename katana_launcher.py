import os
import importlib
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def discover_games(games_dir="games"):
    """Discover all game folders that contain a main.py"""
    game_dirs = []
    for game in Path(games_dir).iterdir():
        if game.is_dir() and (game / "main.py").exists():
            game_dirs.append(game.name)
    return game_dirs

def select_game(games):
    print("\n🎮 Available Games:\n")
    for idx, game in enumerate(games, 1):
        print(f"{idx}. {game}")
    choice = input("\nSelect a game to run (1/2/3...): ")
    try:
        return games[int(choice) - 1]
    except (IndexError, ValueError):
        print("❌ Invalid selection.")
        return None

def run_game(game_key):
    try:
        module_path = f"games.{game_key}.main"
        game_main = importlib.import_module(module_path)
        game_main.main()
    except Exception as e:
        print(f"⚠️  Failed to launch '{game_key}': {e}")

if __name__ == "__main__":
    print(Fore.RED + Style.BRIGHT + """
    ===================================================
    """)
    print(Fore.GREEN + Style.BRIGHT + """
    ██╗  ██╗ █████╗ ████████╗ █████╗ ███╗   ██╗ █████╗     
    ██║ ██╔╝██╔══██╗╚══██╔══╝██╔══██╗████╗  ██║██╔══██╗    
    █████╔╝ ███████║   ██║   ███████║██╔██╗ ██║███████║    
    ██╔═██╗ ██╔══██║   ██║   ██╔══██║██║╚██╗██║██╔══██║    
    ██║  ██╗██║  ██║   ██║   ██║  ██║██║ ╚████║██║  ██║    
    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝    
    """)
    print(Fore.RED + Style.BRIGHT + """
    ===================================================
    """)

    games = discover_games()
    if not games:
        print("❌ No benchmarkable games found in ./games")
    else:
        selected = select_game(games)
        if selected:
            run_game(selected)
