import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkinter import PhotoImage
import subprocess
import pickle
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
import threading
import socket
import netifaces
import logging


class DDosDetectionFirewall(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window Configuration
        self.title("DDoS Detection and Firewall")
        self.geometry("900x750")
        self.configure(bg="#2c3e50")

        # Custom Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', foreground='white', background='#2c3e50', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 10), background='#3498db')
        self.style.configure('Danger.TButton', background='#e74c3c')

        # Main Frame
        main_frame = tk.Frame(self, bg="#2c3e50")
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Header
        header_label = ttk.Label(
            main_frame, 
            text="DDoS Detection and Firewall", 
            font=('Arial', 18, 'bold')
        )
        header_label.pack(pady=(0, 20))

        # DDoS Detection Image (Placeholder)
        try:
            image_path = "./icon.png"  # Replace with your image file path
            ddos_image = PhotoImage(file=image_path)

            # Create a Label to display the image
            self.image_label = ttk.Label(
                main_frame,
                image=ddos_image,
                background="#f9f9f9"  # Match the app background to blend seamlessly
            )
            self.image_label.image = ddos_image  # Keep a reference to avoid garbage collection

            # Center the image
            self.image_label.pack(pady=10, anchor="center")  # Use anchor="center" to ensure centering
        except Exception as e:
            # Fallback to text if the image can't be loaded
            self.image_label = ttk.Label(
                main_frame,
                text="[DDoS Detection Visualization]",
                background="#f9f9f9",
                foreground="#333333",
                font=('Ubuntu', 16, 'italic'),
                anchor="center"
            )
            self.image_label.pack(pady=10, fill=tk.X)

        # Status Label
        self.status_var = tk.StringVar(value="Idle: No Active Detection")
        status_label = ttk.Label(
            main_frame, 
            textvariable=self.status_var, 
            style='TLabel'
        )
        status_label.pack(pady=10)

        # Network Adapter Dropdown
        ttk.Label(main_frame, text="Select Network Adapter:", style='TLabel').pack()
        self.adapter_var = tk.StringVar()
        adapters = self.get_network_adapters()
        adapter_dropdown = ttk.Combobox(
            main_frame, 
            textvariable=self.adapter_var, 
            values=adapters, 
            state="readonly"
        )
        adapter_dropdown.pack(pady=10)
        if adapters:
            adapter_dropdown.set(adapters[0])

        # Buttons Frame
        buttons_frame = tk.Frame(main_frame, bg="#2c3e50")
        buttons_frame.pack(pady=10)

        # Detect and Mitigate Button
        ttk.Button(
            buttons_frame, 
            text="Start DDoS Detection", 
            command=self.start_ddos_detection
        ).grid(row=0, column=0, padx=5, pady=5)

        # Blacklist Buttons
        ttk.Label(buttons_frame, text="Blacklist:", style='TLabel').grid(row=1, column=0, pady=5)
        ttk.Button(
            buttons_frame, 
            text="Start Blacklist", 
            command=self.start_blacklist_firewall
        ).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(
            buttons_frame, 
            text="Open blacklist_ip.txt", 
            command=self.open_blacklist_file
        ).grid(row=2, column=1, padx=5, pady=5)

        # Whitelist Buttons
        ttk.Label(buttons_frame, text="Whitelist:", style='TLabel').grid(row=3, column=0, pady=5)
        ttk.Button(
            buttons_frame, 
            text="Start Whitelist", 
            command=self.start_whitelist_firewall
        ).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(
            buttons_frame, 
            text="Open whitelist_ip.txt", 
            command=self.open_whitelist_file
        ).grid(row=4, column=1, padx=5, pady=5)

        # SSL/TLS Blocking Buttons
        ttk.Label(buttons_frame, text="SSL/TLS Blocking:", style='TLabel').grid(row=5, column=0, pady=5)
        ttk.Button(
            buttons_frame, 
            text="Start SSL/TLS Blocking", 
            command=self.start_ssl_tls_blocking
        ).grid(row=6, column=0, padx=5, pady=5)
        ttk.Button(
            buttons_frame, 
            text="Open blocklist_website.txt", 
            command=self.open_blocklist_websites_file
        ).grid(row=6, column=1, padx=5, pady=5)

        # Stop Button
        self.stop_button = ttk.Button(
            main_frame, 
            text="STOP ALL PROCESSES", 
            style='Danger.TButton', 
            command=self.stop_process
        )
        # self.stop_button.pack(pady=20)


    def on_close(self):
        """Handle the close event."""
        self.quit()

    def stop_process(self):
        """Stop any running process and flush iptables."""
        if hasattr(self, 'running_thread') and self.running_thread.is_alive():
            self.stop_event.set()  # Signal the thread to stop
            self.running_thread.join()  # Wait for the thread to finish
            self.flush_iptables()

    def flush_iptables(self):
        """Flush iptables to reset firewall rules."""
        try:
            subprocess.run(['iptables', '-F'])  # Flush all iptables rules
        except Exception as e:
            pass

    def get_network_adapters(self):
        """Retrieve network interfaces available on the system."""
        try:
            interfaces = netifaces.interfaces()
            return interfaces
        except Exception as e:
            return []

    def start_ddos_detection(self):
        """Start DDoS detection and mitigation."""
        def callproc():
	        subprocess.call("sudo ryu-manager mitigation_module.py", shell=True)
        t1 = threading.Thread(target=callproc)
        t1.start()
	 
        

    def start_blacklist_firewall(self):
        """Start Blacklist firewall."""
        self.apply_firewall_rules("blacklistedip.txt")

    def open_blacklist_file(self):
        """Open the blacklisted IP file."""
        file_path = "./blacklistedip.txt"
        if file_path:
            os.system(f"xdg-open {file_path}")

    def start_whitelist_firewall(self):
        """Start Whitelist firewall."""
        self.apply_firewall_rules("whitelistedip.txt", whitelist=True)

    def open_whitelist_file(self):
        """Open the whitelisted IP file."""
        file_path = "./whitelistedip.txt"
        if file_path:
            os.system(f"xdg-open {file_path}")

    def start_ssl_tls_blocking(self):
        """Start blocking SSL/TLS websites."""
        adapter = self.adapter_dropdown.get()
        self.block_ssl_tls_websites(adapter)

    def open_blocklist_websites_file(self):
        """Open the blocklist websites file."""
        file_path = "./website_block.txt"
        if file_path:
            os.system(f"xdg-open {file_path}")

    def apply_firewall_rules(self, file_name, whitelist=False):
        """Apply firewall rules based on the IP list."""
        try:
            with open(file_name, 'r') as file:
                ip_list = file.readlines()
                for ip in ip_list:
                    ip = ip.strip()
                    if whitelist:
                        subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-j', 'ACCEPT'])
                    else:
                        subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])
        except Exception as e:
            pass
    def block_ssl_tls_websites(self, adapter):
        """Block SSL/TLS websites by manipulating system settings for a specific adapter."""
        try:
            blocklist = []
            with open("blocklist_websites.txt", 'r') as file:
                blocklist = file.readlines()

            # Dummy blocking logic for SSL/TLS websites. Extend it for your use case.
            for website in blocklist:
                website = website.strip()
                subprocess.run(['iptables', '-A', 'OUTPUT', '-d', website, '-j', 'DROP'])

        except Exception as e:
            pass
# Main entry point for the application
def run_gui():
    try:
        app = DDosDetectionFirewall()
        app.mainloop()
    except Exception as e:
        print(f"Error initializing GUI: {e}")

# Call the function to run the GUI
if __name__ == "__main__":
    run_gui()

