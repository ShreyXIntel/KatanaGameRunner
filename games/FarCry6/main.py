# main.py inside games/cs2/

import sys
import time
from pathlib import Path
from colorama import init, Fore, Style
from .flow import CS2Benchmark

# Initialize colorama
init(autoreset=True)

REQUIRED_ASSETS = [
    "play_tab.png",
    "workshop_tab.png",
    "cs2_fps_benchmark.png",
    "go_button.png",
    "benchmark_first_frame.png",
    "benchmark_end_screen.png"
]

def print_banner():
    print(Fore.WHITE + Style.BRIGHT + """
 ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗███████╗██████╗     ███████╗████████╗██████╗ ██╗██╗  ██╗███████╗    ██████╗ 
██╔════╝██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗    ██╔════╝╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝    ╚════██╗
██║     ██║   ██║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝    ███████╗   ██║   ██████╔╝██║█████╔╝ █████╗       █████╔╝
██║     ██║   ██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗    ╚════██║   ██║   ██╔══██╗██║██╔═██╗ ██╔══╝      ██╔═══╝ 
╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║    ███████║   ██║   ██║  ██║██║██║  ██╗███████╗    ███████╗
 ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝    ╚══════╝
    """)

def check_assets():
    asset_dir = Path(__file__).parent / "assets"
    missing = [f for f in REQUIRED_ASSETS if not (asset_dir / f).is_file()]
    if missing:
        print("\n❌ [Error] Missing asset files:")
        for f in missing:
            print(f" - {f}")
        print(f"\n📂 Please place all assets in: {asset_dir.resolve()}")
        sys.exit(1)

def main():
    print_banner()
    print("📦 ======= Katana CS2 Benchmark Automation ========\n")
    check_assets()

    run_count = 3
    cooldown_between_runs = 120  # seconds

    benchmark = CS2Benchmark()

    # Run 0 – duration measurement
    print("\n⏱️ ===== Starting Run 0 (Duration Measurement) =====")
    benchmark.launch()
    benchmark.wait_until_ready()
    benchmark.navigate_to_benchmark()
    benchmark.start_benchmark()
    benchmark.collect_results()  # For run 0 only
    known_duration = benchmark.benchmark_duration
    benchmark.teardown()
    print(f"🧊 Cooling down for {cooldown_between_runs} seconds...\n")
    time.sleep(cooldown_between_runs)

    # Runs 1 to N – reuse known duration
    for i in range(1, run_count):
        print(f"\n📊 ===== Starting Run {i} =====")
        benchmark.launch()
        benchmark.wait_until_ready()
        benchmark.navigate_to_benchmark()
        benchmark.start_benchmark()
        benchmark.collect_results_trace(run_id=i, known_duration=known_duration)
        benchmark.teardown()
        if i < run_count - 1:
            print(f"🧊 Cooling down for {cooldown_between_runs} seconds...\n")
            time.sleep(cooldown_between_runs)        

    print("✅ All runs complete.\n")

if __name__ == "__main__":
    main()
