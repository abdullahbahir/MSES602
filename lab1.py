"""
MSES602 - Lab #1: Introduction to DevOps - Traditional Ops with Python
System environment check script (extends envChk.py with an SSH reachability check).
"""

import psutil
import platform
import socket
from datetime import datetime


def print_section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


# ---------------------------------------------------------
# System Information
# ---------------------------------------------------------

print_section("SYSTEM INFORMATION")

print("Operating System:", platform.system())
print("OS Version:", platform.version())
print("Machine:", platform.machine())
print("Hostname:", socket.gethostname())


# ---------------------------------------------------------
# CPU Information
# ---------------------------------------------------------

print_section("CPU INFORMATION")

print("CPU Cores:", psutil.cpu_count(logical=False))
print("Logical CPUs:", psutil.cpu_count(logical=True))

cpu_usage = psutil.cpu_percent(interval=1)

print("Current CPU Usage:", cpu_usage, "%")


# ---------------------------------------------------------
# Memory Information
# ---------------------------------------------------------

print_section("MEMORY INFORMATION")

memory = psutil.virtual_memory()

print("Total Memory:",
      round(memory.total / (1024 ** 3), 2), "GB")

print("Available Memory:",
      round(memory.available / (1024 ** 3), 2), "GB")

print("Used Memory:",
      round(memory.used / (1024 ** 3), 2), "GB")

print("Memory Usage:",
      memory.percent, "%")


# ---------------------------------------------------------
# Disk Information
# ---------------------------------------------------------

print_section("DISK INFORMATION")

disk = psutil.disk_usage("/")

print("Total Disk Space:",
      round(disk.total / (1024 ** 3), 2), "GB")

print("Used Disk Space:",
      round(disk.used / (1024 ** 3), 2), "GB")

print("Free Disk Space:",
      round(disk.free / (1024 ** 3), 2), "GB")

print("Disk Usage:",
      disk.percent, "%")


# ---------------------------------------------------------
# Network Information
# ---------------------------------------------------------

print_section("NETWORK INFORMATION")

network = psutil.net_io_counters()

print("Bytes Sent:",
      round(network.bytes_sent / (1024 ** 2), 2), "MB")

print("Bytes Received:",
      round(network.bytes_recv / (1024 ** 2), 2), "MB")


# ---------------------------------------------------------
# SSH Connectivity
# ---------------------------------------------------------

print_section("SSH CONNECTIVITY")

ssh_host = "127.0.0.1"
ssh_port = 22

try:
    with socket.create_connection((ssh_host, ssh_port), timeout=3):
        print(f"SSH port {ssh_port} on {ssh_host} is OPEN (reachable).")
except (socket.timeout, ConnectionRefusedError, OSError):
    print(f"SSH port {ssh_port} on {ssh_host} is NOT reachable.")


# ---------------------------------------------------------
# Boot Time
# ---------------------------------------------------------

print_section("SYSTEM UPTIME")

boot_time = datetime.fromtimestamp(psutil.boot_time())

print("System Boot Time:", boot_time)

uptime_seconds = datetime.now().timestamp() - psutil.boot_time()

uptime_hours = uptime_seconds / 3600

print("System Uptime:",
      round(uptime_hours, 2), "hours")


# ---------------------------------------------------------
# Logged In Users
# ---------------------------------------------------------

print_section("LOGGED IN USERS")

users = psutil.users()

if users:
    for user in users:
        print("Username:", user.name)
        print("Terminal:", user.terminal)
        print("Login Time:",
              datetime.fromtimestamp(user.started))
else:
    print("No logged-in users found.")


# ---------------------------------------------------------
# Running Processes
# ---------------------------------------------------------

print_section("RUNNING PROCESSES")

process_count = len(psutil.pids())

print("Number of Running Processes:",
      process_count)


# ---------------------------------------------------------
# Final Status
# ---------------------------------------------------------

print_section("SYSTEM STATUS")

if cpu_usage > 80:
    print("WARNING: CPU usage is high.")
else:
    print("CPU usage is normal.")

if memory.percent > 80:
    print("WARNING: Memory usage is high.")
else:
    print("Memory usage is normal.")

if disk.percent > 80:
    print("WARNING: Disk usage is high.")
else:
    print("Disk usage is normal.")

print()
print("System environment check completed.")