"""
Author:     Bhuyan, Satyajit
WWID:       11652929
Email:      satyajit.bhuyan@intel.com

File:       flow.py
Project:    Katana - Game Benchmark Automation Framework

Description:
------------
This module defines the `CS2Benchmark` class for automating the launch,
navigation, execution, and monitoring of the CS2 FPS benchmarking workflow.
It uses OpenCV-based template matching and PyAutoGUI for GUI interaction.
The implementation is modular and scalable, designed to integrate with
Katana’s broader multi-game benchmarking architecture.

Key functions include:
- Launching CS2 via Steam (if not already running)
- Navigating through game menus using visual template detection
- Triggering and timing benchmark execution
- Capturing results including screenshot logging
Designed for minimal user intervention and intended to support
future Host-SUT extension and result pipeline integration.
"""
import time
import subprocess
import pyautogui
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
        print("📥 [Run 0] Capturing benchmark duration...")

        if wait_for_template(str(ASSET_DIR / "benchmark_end_screen.png"), timeout=120, check_interval=3):
            self.benchmark_end_time = time.time()
            duration = self.benchmark_end_time - self.benchmark_start_time
            self.benchmark_duration = duration
            print(f"⏱️ [Run 0] Benchmark duration: {duration:.2f} seconds")
            time.sleep(7)

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = Path("logs/screenshots") / f"cs2_benchmark_result_run0_{timestamp}.png"
            pyautogui.screenshot(str(screenshot_path))
            print(f"📸 Screenshot saved to: {screenshot_path}")
        else:
            print("❌ [Run 0] End screen not detected. Cannot measure duration.")

    def collect_results_trace(self, run_id, known_duration):
        if known_duration is None:
            print("❌ [Run] Known duration not provided. Skipping result capture.")
            return

        print(f"📥 [Run {run_id}] Timed collection: sleeping for {known_duration:.2f}s + 7s buffer...")
        time.sleep(known_duration + 7)

        # TODO: Insert PresentMon trigger here in the future

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = Path("logs/screenshots") / f"cs2_benchmark_result_run{run_id}_{timestamp}.png"
        pyautogui.screenshot(str(screenshot_path))
        print(f"📸 Screenshot saved to: {screenshot_path}")


    def teardown(self):
        print("🧹 [Teardown] Initiating cs2 shutdown sequence...")

        # Step 1: Close the console window
        print("🗙 [Teardown] Closing the console...")
        if wait_for_template(str(ASSET_DIR / "console_close_x.png"), timeout=10):
            select_game_mode("console_close_x.png")
            time.sleep(1)
        else:
            print("⚠️ [Teardown] Console close button not found.")

        # Step 2: Click on the power icon
        print("🔋 [Teardown] Clicking the power icon...")
        if wait_for_template(str(ASSET_DIR / "power_button.png"), timeout=10):
            select_game_mode("power_button.png")
            time.sleep(2)
        else:
            print("⚠️ [Teardown] Power button not found.")

        # Step 3: Confirm Quit
        print("🚪 [Teardown] Clicking Quit to exit CS2...")
        if wait_for_template(str(ASSET_DIR / "quit_button.png"), timeout=10):
            select_game_mode("quit_button.png")
            print("✅ [Teardown] CS2 exited.")
        else:
            print("⚠️ [Teardown] Quit button not found. You may need to exit manually.")       
            
