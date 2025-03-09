import subprocess
import signal
import sys
import time

blacklist = []

def run_command(command):
    """Executes a shell command."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\n{e}")

def apply_iptables_rules():
    """Blocks traffic from blacklisted IPs."""
    # Clear existing blacklist iptables rules (optional)
    run_command("sudo iptables -F")
    
    for ip in blacklist:
        command = f"sudo iptables -A INPUT -s {ip} -j DROP"
        print(f"Blocking: {ip}")
        run_command(command)

def restore_default_iptables():
    """Restores default iptables rules (allow all traffic)."""
    print("\nRestoring default iptables rules (allow all traffic)...")
    run_command("sudo iptables -F")
    run_command("sudo iptables -P INPUT ACCEPT")

def load_blacklist_from_file(filename):
    """Loads blacklisted IPs from a file."""
    global blacklist
    try:
        with open(filename, 'r') as file:
            blacklist = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    except Exception as e:
        print(f"Error reading file {filename}: {e}")

def signal_handler(signum, frame):
    """Handles termination signals."""
    print(f"\nInterrupt signal ({signum}) received.")
    restore_default_iptables()
    sys.exit(0)

def main():
    """Main function to set up the firewall."""
    # Set up signal handler for Ctrl+C (SIGINT)
    signal.signal(signal.SIGINT, signal_handler)

    # Load blacklisted IPs from file
    blacklist_file = "blacklistedip.txt"
    load_blacklist_from_file(blacklist_file)

    if not blacklist:
        print("No IPs found in the blacklist. Exiting...")
        sys.exit(1)

    # Apply iptables rules to block blacklisted IPs
    apply_iptables_rules()
    print("Blacklist firewall is active. Press Ctrl+C to stop and restore default settings...")

    # Keep the program running
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()
