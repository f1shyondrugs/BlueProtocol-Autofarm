#!/usr/bin/env python3

DISCORD_WEBHOOK_URL = "YOUR DISCORD WEBHOOK URL"

import pyautogui
import time
import sys
import math
import tkinter as tk
from tkinter import ttk
import threading
import keyboard
import requests
import io
import random
from PIL import Image

ORANGE_X = 960
ORANGE_Y = 470

ORANGE_R = 249
ORANGE_G = 187
ORANGE_B = 23

GRAY_X = 1462
GRAY_Y = 956

GRAY_R = 232
GRAY_G = 232
GRAY_B = 232

CHECK_X = 1695
CHECK_Y = 987

CHECK_R = 210
CHECK_G = 108
CHECK_B = 48

ADDITIONAL_CLICK_X = 1773
ADDITIONAL_CLICK_Y = 593

RED_CHECK_X = 774
RED_CHECK_Y = 900
RED_R = 255
RED_G = 0
RED_B = 0
WHITE_R = 255
WHITE_G = 255
WHITE_B = 255

TOLERANCE = 50
EMERGENCY_TOLERANCE = 20

EMERGENCY_X = 1447
EMERGENCY_Y = 1034
EMERGENCY_R = 234
EMERGENCY_G = 234
EMERGENCY_B = 234

class ColorMonitorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fishing Bot Overlay")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)
        self.click_count = 0
        self.monitoring = False
        self.monitor_thread = None
        self.current_step = 1
        self.orange_detected = False
        self.mouse_held = False
        self.key_held = False
        self.d_key_held = False
        self.orange_check_start_time = None
        self.hotkeys_registered = False
        self.left_mouse_held = False
        self.first_start = True
        self.setup_ui()
        self.setup_hotkeys()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.status_label = ttk.Label(main_frame, text="Status: Paused", font=("Arial", 9))
        self.status_label.grid(row=0, column=0, columnspan=2, pady=(0, 2))
        self.step_label = ttk.Label(main_frame, text="Step 1: Waiting for Bobber", font=("Arial", 8))
        self.step_label.grid(row=1, column=0, columnspan=2, pady=(0, 2))
        self.color_preview = tk.Canvas(main_frame, width=30, height=30, bg="gray")
        self.color_preview.grid(row=2, column=0, padx=(0, 5))
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.rgb_label = ttk.Label(info_frame, text="RGB: ---, ---, ---", font=("Arial", 8))
        self.rgb_label.grid(row=0, column=0, sticky=tk.W)
        self.distance_label = ttk.Label(info_frame, text="Distance: ---", font=("Arial", 8))
        self.distance_label.grid(row=1, column=0, sticky=tk.W)
        self.click_label = ttk.Label(main_frame, text="Fish Caught: 0", font=("Arial", 10, "bold"))
        self.click_label.grid(row=3, column=0, columnspan=2, pady=(5, 2))
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=2)
        self.start_button = ttk.Button(button_frame, text="Start", command=self.toggle_monitoring)
        self.start_button.grid(row=0, column=0, padx=(0, 3))
        self.restart_button = ttk.Button(button_frame, text="Restart", command=self.restart_monitoring)
        self.restart_button.grid(row=0, column=1, padx=(0, 3))
        self.exit_button = ttk.Button(button_frame, text="Exit", command=self.exit_app)
        self.exit_button.grid(row=0, column=2)
        hotkey_label = ttk.Label(main_frame, text="Hotkeys: F1=Pause/Resume, F2=Restart", font=("Arial", 7))
        hotkey_label.grid(row=5, column=0, columnspan=2, pady=(5, 0))
    
    def perform_startup_check(self):
        try:
            startup_pixel = self.get_pixel_color(CHECK_X, CHECK_Y)
            if startup_pixel:
                r, g, b = startup_pixel
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                print(f"Startup check at ({CHECK_X}, {CHECK_Y}): RGB({r}, {g}, {b}) - {hex_color.upper()}")
                self.status_label.config(text=f"Startup: RGB({r}, {g}, {b}) at ({CHECK_X}, {CHECK_Y})", foreground="blue")
                if self.is_check_color(startup_pixel):
                    print(f"Startup check: Target color detected at ({CHECK_X}, {CHECK_Y})")
                    self.status_label.config(text="Status: Paused - No fishing rod, equipping...", foreground="green")
                    try:
                        pyautogui.keyDown('m')
                        print("Startup: Holding 'M' key for 0.5 seconds")
                        self.random_sleep(0.5)
                        pyautogui.keyUp('m')
                        print("Startup: Released 'M' key")
                        self.random_sleep(1.0)
                        pyautogui.click(ADDITIONAL_CLICK_X, ADDITIONAL_CLICK_Y)
                        print(f"Startup: Clicked at ({ADDITIONAL_CLICK_X}, {ADDITIONAL_CLICK_Y})")
                        self.status_label.config(text="Status: Paused - M sequence and click completed", foreground="green")
                    except Exception as e:
                        print(f"Error in startup M key sequence: {e}")
                        self.status_label.config(text="Status: Paused - M sequence error", foreground="red")
                else:
                    print(f"Startup check: Target color not found at ({CHECK_X}, {CHECK_Y})")
                    self.status_label.config(text="Status: Paused - No fishing rod not found at startup", foreground="orange")
            else:
                print(f"Startup check: Could not read pixel at ({CHECK_X}, {CHECK_Y})")
                self.status_label.config(text=f"Startup: Error reading ({CHECK_X}, {CHECK_Y})", foreground="red")
        except Exception as e:
            print(f"Error in startup check: {e}")
            self.status_label.config(text="Startup: Check error", foreground="red")
    
    def setup_hotkeys(self):
        try:
            keyboard.add_hotkey('f1', self.toggle_monitoring)
            keyboard.add_hotkey('f2', self.restart_monitoring)
            self.hotkeys_registered = True
            print("Hotkeys registered: F1=Pause/Resume, F2=Restart")
        except Exception as e:
            print(f"Error setting up hotkeys: {e}")
            self.hotkeys_registered = False
    
    def restart_monitoring(self):
        if self.monitoring:
            self.stop_monitoring()
        self.current_step = 1
        self.orange_detected = False
        self.mouse_held = False
        self.key_held = False
        self.d_key_held = False
        self.orange_check_start_time = None
        self.left_mouse_held = False
        self.first_start = True
        self.step_label.config(text="Step 1: Waiting for Bobber")
        print("Monitoring reset to step 1 - ready to start")
        
    def color_distance(self, r1, g1, b1, r2, g2, b2):
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
    
    def is_orange_color(self, pixel_color):
        r, g, b = pixel_color
        distance = self.color_distance(r, g, b, ORANGE_R, ORANGE_G, ORANGE_B)
        return distance <= TOLERANCE
    
    def is_gray_color(self, pixel_color):
        r, g, b = pixel_color
        distance = self.color_distance(r, g, b, GRAY_R, GRAY_G, GRAY_B)
        return distance <= TOLERANCE
    
    def is_check_color(self, pixel_color):
        r, g, b = pixel_color
        distance = self.color_distance(r, g, b, CHECK_R, CHECK_G, CHECK_B)
        return distance <= TOLERANCE
    
    def is_red_color(self, pixel_color):
        r, g, b = pixel_color
        distance = self.color_distance(r, g, b, RED_R, RED_G, RED_B)
        return distance <= TOLERANCE
    
    def is_white_color(self, pixel_color):
        r, g, b = pixel_color
        distance = self.color_distance(r, g, b, WHITE_R, WHITE_G, WHITE_B)
        return distance <= TOLERANCE
    
    def is_emergency_color(self, pixel_color):
        r, g, b = pixel_color
        distance = self.color_distance(r, g, b, EMERGENCY_R, EMERGENCY_G, EMERGENCY_B)
        return distance <= EMERGENCY_TOLERANCE
    
    def random_sleep(self, base_time, variation_ms=100):
        variation = random.uniform(-variation_ms, variation_ms) / 1000.0
        sleep_time = base_time + variation
        time.sleep(max(0, sleep_time))
    
    def take_screenshot(self):
        try:
            screenshot = pyautogui.screenshot()
            return screenshot
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
    
    def send_screenshot_to_discord(self, screenshot, message="Gray detected - Screenshot"):
        try:
            img_buffer = io.BytesIO()
            screenshot.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            files = {
                'file': ('screenshot.png', img_buffer, 'image/png')
            }
            payload = {
                'content': message
            }
            response = requests.post(DISCORD_WEBHOOK_URL, files=files, data=payload)
            if response.status_code == 204:
                print("Screenshot sent to Discord successfully")
                return True
            else:
                print(f"Failed to send screenshot to Discord. Status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error sending screenshot to Discord: {e}")
            return False
    
    def get_pixel_color(self, x, y):
        try:
            return pyautogui.pixel(x, y)
        except Exception as e:
            print(f"Error getting pixel color: {e}")
            return None
    
    def hold_mouse_at_coordinates(self, x, y):
        try:
            pyautogui.mouseDown(x, y)
            self.mouse_held = True
            print(f"Mouse held down at ({x}, {y})")
            return True
        except Exception as e:
            print(f"Error holding mouse: {e}")
            return False
    
    def release_mouse(self):
        try:
            pyautogui.mouseUp()
            self.mouse_held = False
            print("Mouse released")
            return True
        except Exception as e:
            print(f"Error releasing mouse: {e}")
            return False
    
    def hold_left_mouse(self):
        try:
            pyautogui.mouseDown(button='left')
            self.left_mouse_held = True
            print("Left mouse button held down")
            return True
        except Exception as e:
            print(f"Error holding left mouse: {e}")
            return False
    
    def release_left_mouse(self):
        try:
            pyautogui.mouseUp(button='left')
            self.left_mouse_held = False
            print("Left mouse button released")
            return True
        except Exception as e:
            print(f"Error releasing left mouse: {e}")
            return False
    
    def hold_key(self, key):
        try:
            pyautogui.keyDown(key)
            if key == 'a':
                self.key_held = True
            elif key == 'd':
                self.d_key_held = True
            print(f"Key '{key}' held down")
            return True
        except Exception as e:
            print(f"Error holding key '{key}': {e}")
            return False
    
    def release_key(self, key):
        try:
            pyautogui.keyUp(key)
            if key == 'a':
                self.key_held = False
            elif key == 'd':
                self.d_key_held = False
            print(f"Key '{key}' released")
            return True
        except Exception as e:
            print(f"Error releasing key '{key}': {e}")
            return False
    
    def double_click_at_coordinates(self, x, y):
        try:
            pyautogui.click(x, y)
            print(f"First click at ({x}, {y})")
            self.random_sleep(2.0)
            check_pixel = self.get_pixel_color(CHECK_X, CHECK_Y)
            if check_pixel and self.is_check_color(check_pixel):
                print(f"Check color detected at ({CHECK_X}, {CHECK_Y}) - RGB({check_pixel[0]}, {check_pixel[1]}, {check_pixel[2]})")
                self.root.after(0, lambda: self.status_label.config(text="Status: Check color found! Executing M sequence...", foreground="blue"))
                try:
                    pyautogui.press('m')
                    print("Pressed 'M' key")
                    self.random_sleep(1.0)
                    pyautogui.click(ADDITIONAL_CLICK_X, ADDITIONAL_CLICK_Y)
                    print(f"Clicked at ({ADDITIONAL_CLICK_X}, {ADDITIONAL_CLICK_Y})")
                    self.root.after(0, lambda: self.status_label.config(text="Status: M sequence completed! Waiting...", foreground="green"))
                except Exception as e:
                    print(f"Error in M key sequence: {e}")
                    self.root.after(0, lambda: self.status_label.config(text="Status: M sequence error, continuing...", foreground="red"))
            else:
                print(f"Check color not found at ({CHECK_X}, {CHECK_Y}) - RGB({check_pixel[0] if check_pixel else 'None'}, {check_pixel[1] if check_pixel else 'None'}, {check_pixel[2] if check_pixel else 'None'})")
                self.root.after(0, lambda: self.status_label.config(text="Status: Check color not found, waiting...", foreground="orange"))
            self.random_sleep(2.0)
            pyautogui.mouseDown(940, 504)
            self.random_sleep(0.5)
            pyautogui.mouseUp(940, 504)
            print(f"Second click at (940, 504)")
            return True
        except Exception as e:
            print(f"Error double-clicking: {e}")
            return False
    
    def update_display(self, pixel_color):
        if pixel_color is not None:
            r, g, b = pixel_color
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            self.color_preview.delete("all")
            self.color_preview.create_rectangle(0, 0, 30, 30, fill=hex_color, outline="black", width=1)
            self.rgb_label.config(text=f"RGB: {r:3d}, {g:3d}, {b:3d}")
            emergency_pixel = self.get_pixel_color(EMERGENCY_X, EMERGENCY_Y)
            if emergency_pixel and self.is_emergency_color(emergency_pixel):
                print(f"EMERGENCY: Color detected at ({EMERGENCY_X}, {EMERGENCY_Y}) - Resetting to orange")
                self.status_label.config(text="Status: EMERGENCY! Resetting to waiting for bobber...", foreground="red")
                if self.key_held:
                    self.release_key('a')
                if self.d_key_held:
                    self.release_key('d')
                if self.mouse_held:
                    self.release_mouse()
                if self.left_mouse_held:
                    self.release_left_mouse()
                try:
                    pyautogui.mouseDown(button='left')
                    print("Emergency: Holding left click for 0.5 seconds")
                    self.random_sleep(0.5)
                    pyautogui.mouseUp(button='left')
                    print("Emergency: Released left click")
                except Exception as e:
                    print(f"Error in emergency left click: {e}")
                self.current_step = 1
                self.orange_detected = False
                self.mouse_held = False
                self.key_held = False
                self.d_key_held = False
                self.orange_check_start_time = None
                self.left_mouse_held = False
                self.step_label.config(text="Step 1: Waiting for Bobber")
                self.status_label.config(text="Status: Reset to waiting for bobber - Monitoring...", foreground="green")
                print("Emergency reset completed - back to orange monitoring")
                return
            if self.current_step == 1:
                distance = self.color_distance(r, g, b, ORANGE_R, ORANGE_G, ORANGE_B)
                self.distance_label.config(text=f"Dist: {distance:5.1f}")
                if self.is_orange_color(pixel_color):
                    self.status_label.config(text="Status: Bobber caught, moving to Step 2", foreground="green")
                    self.current_step = 2
                    self.orange_detected = True
                    self.step_label.config(text="Step 2: fish caught")
                    self.hold_mouse_at_coordinates(ORANGE_X, ORANGE_Y)
                    print("Orange detected! Holding mouse and now monitoring for gray color...")
                else:
                    self.status_label.config(text="Status: Looking for Bobber...", foreground="black")
            elif self.current_step == 2:
                distance = self.color_distance(r, g, b, GRAY_R, GRAY_G, GRAY_B)
                self.distance_label.config(text=f"Dist: {distance:5.1f}")
                check_pixel = self.get_pixel_color(RED_CHECK_X, RED_CHECK_Y)
                if check_pixel:
                    if self.is_red_color(check_pixel) or self.is_white_color(check_pixel):
                        if self.left_mouse_held:
                            color_type = "Red" if self.is_red_color(check_pixel) else "White"
                            self.release_left_mouse()
                            print(f"{color_type} detected at ({RED_CHECK_X}, {RED_CHECK_Y}) - Released left mouse")
                    else:
                        if not self.left_mouse_held:
                            self.hold_left_mouse()
                            print(f"Not red/white at ({RED_CHECK_X}, {RED_CHECK_Y}) - Held left mouse")
                current_time = time.time()
                if self.orange_check_start_time is None:
                    self.orange_check_start_time = current_time
                if current_time - self.orange_check_start_time >= 2.0:
                    orange_pixel = self.get_pixel_color(832, 540)
                    if orange_pixel and self.is_orange_color(orange_pixel):
                        if not self.key_held:
                            self.status_label.config(text="Status: Fish guiding left, pressing 'a'...", foreground="orange")
                            self.release_key('d')
                            self.hold_key('a')
                            print("Orange detected while holding mouse! Pressing and holding 'a' key...")
                    orange_pixel = self.get_pixel_color(1088, 540)
                    if orange_pixel and self.is_orange_color(orange_pixel):
                        if not self.d_key_held:
                            self.status_label.config(text="Status: Fish guiding right, pressing 'd'...", foreground="purple")
                            self.release_key('a')
                            self.hold_key('d')
                            print("Second orange detected! Releasing 'a' and pressing 'd' key...")
                    if self.is_gray_color(pixel_color):
                        self.status_label.config(text="Status: fish caught, taking screenshot...", foreground="red")
                        screenshot = self.take_screenshot()
                        if screenshot:
                            def send_screenshot():
                                self.send_screenshot_to_discord(screenshot, f"Fish Caught! Fish #{self.click_count + 1}!")
                            screenshot_thread = threading.Thread(target=send_screenshot, daemon=True)
                            screenshot_thread.start()
                        self.status_label.config(text="Status: fish caught, waiting 1s before clicking...", foreground="red")
                        if self.key_held:
                            self.release_key('a')
                        if self.d_key_held:
                            self.release_key('d')
                        self.release_mouse()
                        self.random_sleep(1.0)
                        self.status_label.config(text="Status: fish caught, double-clicking...", foreground="red")
                        if self.double_click_at_coordinates(GRAY_X, GRAY_Y):
                            self.click_count += 1
                            self.click_label.config(text=f"Fish Caught: {self.click_count}")
                            print(f"Gray detected! Released mouse, waited 1s, and double-clicked at ({GRAY_X}, {GRAY_Y}) - Total double-clicks: {self.click_count}")
                            self.current_step = 1
                            self.orange_detected = False
                            self.mouse_held = False
                            self.key_held = False
                            self.d_key_held = False
                            self.orange_check_start_time = None
                            self.left_mouse_held = False
                            self.step_label.config(text="Step 1: Waiting for Bobber")
                    else:
                        if self.d_key_held:
                            self.status_label.config(text="Status: Holding 'd' - Looking for fish caught...", foreground="purple")
                        elif self.key_held:
                            self.status_label.config(text="Status: Holding 'a' - Looking for fish caught...", foreground="orange")
                        else:
                            self.status_label.config(text="Status: Holding mouse - Looking for fish caught...", foreground="black")
                else:
                    remaining_time = 2.0 - (current_time - self.orange_check_start_time)
                    self.status_label.config(text=f"Status: Waiting {remaining_time:.1f}s...", foreground="blue")
    
    def monitor_loop(self):
        while self.monitoring:
            if self.monitoring:
                if self.current_step == 1:
                    pixel_color = self.get_pixel_color(ORANGE_X, ORANGE_Y)
                else:
                    pixel_color = self.get_pixel_color(GRAY_X, GRAY_Y)
                self.root.after(0, self.update_display, pixel_color)
            self.random_sleep(0.1, variation_ms=25)
    
    def start_monitoring(self):
        if self.first_start:
            self.perform_startup_check()
            self.first_start = False
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.start_button.config(text="Stop")
        self.status_label.config(text="Status: Monitoring...", foreground="black")
    
    def stop_monitoring(self):
        self.monitoring = False
        if self.mouse_held:
            self.release_mouse()
        if self.left_mouse_held:
            self.release_left_mouse()
        if self.key_held:
            self.release_key('a')
        if self.d_key_held:
            self.release_key('d')
        self.start_button.config(text="Start")
        self.status_label.config(text="Status: Stopped", foreground="gray")
    
    def toggle_monitoring(self):
        if self.monitoring:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def exit_app(self):
        self.monitoring = False
        if self.mouse_held:
            self.release_mouse()
        if self.left_mouse_held:
            self.release_left_mouse()
        if self.key_held:
            self.release_key('a')
        if self.d_key_held:
            self.release_key('d')
        if self.hotkeys_registered:
            try:
                keyboard.unhook_all()
                print("Hotkeys unregistered")
            except Exception as e:
                print(f"Error unregistering hotkeys: {e}")
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.root.mainloop()

def main():
    print("Starting Fishing Bot Overlay...")
    app = ColorMonitorGUI()
    app.run()

if __name__ == "__main__":
    main()
