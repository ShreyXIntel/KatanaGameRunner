
import sys
import time
from pathlib import Path
from games.cs2.flow import CS2Benchmark

REQUIRED_ASSETS = [
    "assets/play_tab.png",
    "assets/workshop_tab.png"
]

def check_assets_exist():
    missing = [f for f in REQUIRED_ASSETS if not Path(f).is_file()]
    if missing:
        print("\n[Error] Missing required asset files:")
        for f in missing:
            print(f" - {f}")
        print("\nPlease ensure all required images are in the correct 'assets/' folder.")
        sys.exit(1)

def main():
    print("=== Katana CS2 Benchmark Automation ===\n")
    check_assets_exist()
    cs2 = CS2Benchmark()
    cs2.launch()
    cs2.wait_until_ready()
    cs2.navigate_to_benchmark()
    cs2.start_benchmark()
    cs2.collect_results()
    cs2.teardown()
    print("\n✅ Benchmark run complete.")

if __name__ == "__main__":
    main()
