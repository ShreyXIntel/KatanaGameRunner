"""
Author:     Tripathy, Shreyansh
WWID:       12310782
Email:      shreyansh.tripathy@intel.com

File:       flow.py
Project:    Katana - Game Benchmark Automation Framework

Description:
------------
This module defines the `FC6Benchmark` class for automating the launch,
navigation, execution, and monitoring of the FC6 FPS benchmarking workflow.
It uses OpenCV-based template matching and PyAutoGUI for GUI interaction.
The implementation is modular and scalable, designed to integrate with
Katana’s broader multi-game benchmarking architecture.

Key functions include:
- Launching FC6 via Ubisoft (if not already running)
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
from actions import click_on_btn
from detectors import wait_for_template

# Path to local assets folder (within Katana/games/FC6/)
ASSET_DIR = Path(__file__).parent / "assets"

# =======================================================================================
# FC6Benchmark Class: Automates launching and benchmarking FC6 fps benchmark workshop map
# =======================================================================================

class FC6Benchmark:
    def launch(self):
        print("🚀 [Launch] Launching FC6 via Ubisoft...")
        subprocess.Popen(['start', 'uplay://launch/5266/0'], shell=True)
        time.sleep(50)

# Waits for the game to reach to main mennu /lobby after game launch
    def wait_until_ready(self):
        print("⏳ [Wait] Waiting for FC6 main menu to appear...")
        found = wait_for_template(str(ASSET_DIR / "1.1.main_menu.png"), timeout=40)
        if found:
            print("✅ [Wait] Main menu detected.")
        else:
            print("❌ [Wait] Main menu not detected within timeout.")

    def navigate_to_benchmark(self):
        print("🧭 [Navigate] Clicking Options and selecting benchmarks...")
        click_on_btn("2.2.options")
        print("Options button clicked")

        print("Looking for Benchmarks button...")
        if wait_for_template(str(ASSET_DIR / "3.3.btn_benchmark.png"), timeout=20, check_interval=2):
            print("Benchmark button found!")
        else:
            print("❌ [Error] Benchmark button not found.")


    def start_benchmark(self):
        print("Clicking Benchmark button to start benchmark...")
        if wait_for_template(str(ASSET_DIR / "3.3.btn_benchmark.png"), timeout=15, check_interval=2):
            click_on_btn("3.3.btn_benchmark.png")
        else:
            print("❌ [Error] Benchmark button button not found.")
            return

        print("🏁 [Benchmark] Starting benchmark session...")
        print("🧠 Waiting for benchmark to visually begin...")
        # if wait_for_template(str(ASSET_DIR / "benchmark_first_frame.png"), timeout=20, check_interval=1):
        #     self.benchmark_start_time = time.time()
        #     print("✅ [Benchmark] Visual start confirmed.")
        # else:
        #     print("❌ [Benchmark] Failed to detect start frame.")

    def collect_results(self):
        print("📥 [Run 0] Capturing benchmark duration...")

        if wait_for_template(str(ASSET_DIR / "benchmark_end_screen.png"), timeout=120, check_interval=3):
            self.benchmark_end_time = time.time()
            duration = self.benchmark_end_time - self.benchmark_start_time
            self.benchmark_duration = duration
            print(f"⏱️ [Run 0] Benchmark duration: {duration:.2f} seconds")
            time.sleep(7)

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = Path("logs/screenshots") / f"FC6_benchmark_result_run0_{timestamp}.png"
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
        screenshot_path = Path("logs/screenshots") / f"FC6_benchmark_result_run{run_id}_{timestamp}.png"
        pyautogui.screenshot(str(screenshot_path))
        print(f"📸 Screenshot saved to: {screenshot_path}")


    def teardown(self):
        print("🧹 [Teardown] Initiating FC6 shutdown sequence...")

        # Step 1: Close the benchmark results window
        print("🗙 [Teardown] Closing the benchmark results window...")
        if wait_for_template(str(ASSET_DIR / "6.6.backto_options.png"), timeout=10):
            click_on_btn("6.6.backto_options1.png")
            time.sleep(2)
        else:
            print("⚠️ [Teardown] Exit Benchmark button not found.")

        # Step 2: Return to main menu
        print("🔋 [Teardown] Clicking Esc/Back button...")
        if wait_for_template(str(ASSET_DIR / "7.7.backto_main_menu.png"), timeout=10):
            click_on_btn("7.7.backto_main_menu.png")
            time.sleep(2)
        else:
            print("⚠️ [Teardown] Esc/Back button not found.")

        # Step 3: Quiting to desktop
        print("🚪 [Teardown] Clicking Quit To Desktop button...")
        if wait_for_template(str(ASSET_DIR / "8.8.quit_to_desktop.png"), timeout=10):
            click_on_btn("8.8.quit_to_desktop.png")
            print("✅ [Teardown] Quit To Desktop button clicked.")
            time.sleep(2)
        else:
            print("⚠️ [Teardown] Quit To Desktop button not found. You may need to click manually.")  

        # Step 4: Confirming quit
        print("🚪 [Teardown] Confirming quit...")
        if wait_for_template(str(ASSET_DIR / "9.9.quit_to_desktop_final.png"), timeout=10):
            click_on_btn("9.9.quit_to_desktop_final.png")
            print("✅ [Teardown] FC6 exited.")
            time.sleep(2)
        else:
            print("⚠️ [Teardown] Couldn't confirm quit to desktop! You may need to click manually.")       
            
