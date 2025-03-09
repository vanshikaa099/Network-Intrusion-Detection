import subprocess
import signal
import sys
import time

whitelist = []

def run_command(command):
    """Executes a shell command."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\n{e}")

def apply_iptables_rules():
    """Allows only traffic from whitelisted IPs and blocks all other traffic."""
    # Clear existing iptables rules
    run_command("sudo iptables -F")

    # Block all incoming traffic by default
    run_command("sudo iptables -P INPUT DROP")
    
    # Allow traffic from whitelisted IPs
    for ip in whitelist:
        command = f"sudo iptables -A INPUT -s {ip} -j ACCEPT"
        print(f"Allowing: {ip}")
        run_command(command)

def restore_default_iptables():
    """Restores default iptables rules (allow all traffic)."""
    print("\nRestoring default iptables rules (allow all traffic)...")
    run_command("sudo iptables -F")
    run_command("sudo iptables -P INPUT ACCEPT")

def load_whitelist_from_file(filename):
    """Loads whitelisted IPs from a file."""
    global whitelist
    try:
        with open(filename, 'r') as file:
            whitelist = [line.strip() for line in file if line.strip()]
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
    """Main function to set up the whitelist firewall."""
    # Set up signal handler for Ctrl+C (SIGINT)
    signal.signal(signal.SIGINT, signal_handler)

    # Load whitelisted IPs from file
    whitelist_file = "whitelistedip.txt"
    load_whitelist_from_file(whitelist_file)

    if not whitelist:
        print("No IPs found in the whitelist. Exiting...")
        sys.exit(1)

    # Apply iptables rules to allow only whitelisted IPs
    apply_iptables_rules()
    print("Whitelist firewall is active. Press Ctrl+C to stop and restore default settings...")

    # Keep the program running
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()
