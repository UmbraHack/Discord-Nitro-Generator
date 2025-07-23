import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, scrolledtext
import random
import string
import requests
import threading
import json
import time

# CODED BY @UmbraHack


# ---------------------------------------------------------------
# 🛡️ COPYRIGHT WARNING - Discord Nitro Generator Tool by @UmbraHack 
# ---------------------------------------------------------------
# This software is protected under intellectual property laws.
# You may NOT modify, distribute, or reuse any part of this code
# unless authorized by the developer.
# Any unauthorized tampering may cause issues or break functionality.
# ---------------------------------------------------------------

messagebox.showwarning(
            "⚠️ WARNING",
            "This tool is protected.\n\nDo not modify the code unless you fully understand what you're doing.\n\nUnauthorized modification may break the tool or violate terms."
        )

class NitroGenerator:
    def __init__(self, root):
        self.root = root

        self.root.title("Discord Nitro Generator - CODED BY @UmbraHack")
        self.root.geometry("600x400")
        self.root.configure(bg="#1C2526")
        self.running = False
        self.threads = []
        self.valid_codes = 0
        self.invalid_codes = 0

        # GUI Elements
        self.setup_gui()

    def setup_gui(self):
        # Webhook Frame
        webhook_frame = tk.Frame(self.root, bg="#1C2526")
        webhook_frame.pack(pady=10)

        tk.Label(webhook_frame, text="Webhook URL (optional):", bg="#1C2526", fg="#00FF00", font=("Arial", 12)).pack(side=tk.LEFT)
        self.webhook_entry = tk.Entry(webhook_frame, width=40, bg="#0A0F0F", fg="#00FF00", insertbackground="#00FF00")
        self.webhook_entry.pack(side=tk.LEFT, padx=5)

        # Threads Frame
        threads_frame = tk.Frame(self.root, bg="#1C2526")
        threads_frame.pack(pady=10)

        tk.Label(threads_frame, text="Threads:", bg="#1C2526", fg="#00FF00", font=("Arial", 12)).pack(side=tk.LEFT)
        self.threads_entry = tk.Entry(threads_frame, width=10, bg="#0A0F0F", fg="#00FF00", insertbackground="#00FF00")
        self.threads_entry.pack(side=tk.LEFT, padx=5)
        self.threads_entry.insert(0, "10")

        # Buttons
        button_frame = tk.Frame(self.root, bg="#1C2526")
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_generation, bg="#00FF00", fg="#000000", font=("Arial", 12))
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_generation, bg="#00FF00", fg="#000000", font=("Arial", 12))
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Output Area
        self.output_area = scrolledtext.ScrolledText(self.root, width=60, height=10, bg="#0A0F0F", fg="#00FF00", font=("Arial", 10))
        self.output_area.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="Valid: 0 | Invalid: 0", bg="#1C2526", fg="#00FF00", font=("Arial", 12))
        self.status_label.pack(pady=5)

    def log(self, message):
        self.output_area.insert(tk.END, message + "\n")
        self.output_area.see(tk.END)

    def send_webhook(self, url_nitro, webhook_url):
        try:
            payload = {
                'embeds': [{
                    'title': 'Nitro Valid!',
                    'description': f"**Nitro:**\n```{url_nitro}```",
                    'color': 0x00FF00,
                    'footer': {'text': 'CODED BY @UmbraHack'}
                }],
                'username': 'Nitro Generator',
                'avatar_url': 'https://imgur.com/a/w5xfN39'
            }
            headers = {'Content-Type': 'application/json'}
            requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        except:
            self.log("Webhook failed. Your URL is probably garbage.")

    def nitro_check(self):
        try:
            code_nitro = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            url_nitro = f'https://discord.gift/{code_nitro}'
            response = requests.get(
                f'https://discordapp.com/api/v6/entitlements/gift-codes/{code_nitro}?with_application=false&with_subscription_plan=true',
                timeout=2
            )
            if response.status_code == 200:
                self.valid_codes += 1
                webhook_url = self.webhook_entry.get()
                if webhook_url:
                    self.send_webhook(url_nitro, webhook_url)
                self.log(f"[VALID] {url_nitro}")
            else:
                self.invalid_codes += 1
                self.log(f"[INVALID] {url_nitro}")
            self.status_label.config(text=f"Valid: {self.valid_codes} | Invalid: {self.invalid_codes}")
        except:
            self.invalid_codes += 1
            self.log(f"[ERROR] Failed to check {url_nitro}")

    def generate_codes(self):
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        try:
            threads_number = int(self.threads_entry.get())
            if threads_number <= 0:
                raise ValueError
        except:
            self.log("Invalid thread count. Try again ?")
            self.running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            return

        self.threads = []
        for _ in range(threads_number):
            if not self.running:
                break
            t = threading.Thread(target=self.nitro_check)
            t.start()
            self.threads.append(t)

    def start_generation(self):
        if not self.running:
            threading.Thread(target=self.generate_codes).start()

    def stop_generation(self):
        self.running = False
        for thread in self.threads:
            thread.join()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log("Generation stopped.")

def main():
    root = tk.Tk()
    app = NitroGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
