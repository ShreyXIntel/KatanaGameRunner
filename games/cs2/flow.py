import time
import subprocess
from pathlib import Path
from .actions import click_play_tab, select_game_mode
from .detectors import wait_for_template

# Path to local assets folder (within Katana/games/cs2/)
ASSET_DIR = Path(__file__).parent / "assets"

# =======================================================================================
# CS2Benchmark Class: Automates launching and benchmarking CS2 fps benchmark workshop map
# =======================================================================================

class CS2Benchmark:

    def launch(self):
        print("🚀 [Launch] Launching CS2 via Steam...")
        subprocess.Popen(['start', 'steam://rungameid/730'], shell=True)
        time.sleep(40)

    def wait_until_ready(self):
        print("⏳ [Wait] Waiting for CS2 main screen to appear...")
        found = wait_for_template(str(ASSET_DIR / "play_tab.png"), timeout=40)
        if found:
            print("✅ [Wait] Main screen detected.")
        else:
            print("❌ [Wait] Main screen not detected within timeout.")

    def navigate_to_benchmark(self):
        print("🧭 [Navigate] Clicking PLAY and selecting game mode...")
        click_play_tab()

        print("🧱 [Step 1] Looking for 'Workshop Maps' tab...")
        if wait_for_template(str(ASSET_DIR / "workshop_tab.png"), timeout=20, check_interval=2):
            select_game_mode("workshop_tab.png")
        else:
            print("❌ [Error] 'Workshop' tab not found.")

        print("🗺️ [Step 2] Selecting CS2 FPS Benchmark map...")
        if wait_for_template(str(ASSET_DIR / "cs2_fps_benchmark.png"), timeout=20, check_interval=2):
            select_game_mode("cs2_fps_benchmark.png")
        else:
            print("❌ [Error] 'CS2 FPS Benchmark' map not found.")

    def start_benchmark(self):
        print("🎯 [Step 3] Clicking GO to start benchmark...")
        if wait_for_template(str(ASSET_DIR / "go_button.png"), timeout=15, check_interval=2):
            select_game_mode("go_button.png")
        else:
            print("❌ [Error] 'GO' button not found.")
            return

        print("🏁 [Benchmark] Starting benchmark session...")
        print("🧠 Waiting for benchmark to visually begin...")
        if wait_for_template(str(ASSET_DIR / "benchmark_first_frame.png"), timeout=20, check_interval=1):
            self.benchmark_start_time = time.time()
            print("✅ [Benchmark] Visual start confirmed.")
        else:
            print("❌ [Benchmark] Failed to detect start frame.")

    def collect_results(self):
        print("📊 [Collect] Waiting for benchmark to finish...")
        if wait_for_template(str(ASSET_DIR / "benchmark_end_screen.png"), timeout=120, check_interval=2):
            self.benchmark_end_time = time.time()
            duration = self.benchmark_end_time - self.benchmark_start_time
            print(f"⏱️ [Done] Benchmark duration: {duration:.2f} seconds")
        else:
            print("❌ [Error] Benchmark end screen not detected within timeout.")

    def teardown(self):
        print("🧹 [Teardown] Ending benchmark and exiting game (not implemented yet)...")
