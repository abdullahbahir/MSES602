# Section 7: Modifying a Script and Explaining the Change

For the final part of the lab, I modified the system environment script to add a check for SSH connectivity. The original script collected basic system metrics such as CPU, memory, and disk usage, but it did not verify whether SSH was reachable. I extended the script to test port 22 on localhost and print a clear status message indicating whether the service was open or not.

## Modified Script

```python
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


print_section("SYSTEM INFORMATION")
print("Operating System:", platform.system())
print("OS Version:", platform.version())
print("Machine:", platform.machine())
print("Hostname:", socket.gethostname())

print_section("CPU INFORMATION")
print("CPU Cores:", psutil.cpu_count(logical=False))
print("Logical CPUs:", psutil.cpu_count(logical=True))

cpu_usage = psutil.cpu_percent(interval=1)
print("Current CPU Usage:", cpu_usage, "%")

print_section("MEMORY INFORMATION")
memory = psutil.virtual_memory()
print("Total Memory:", round(memory.total / (1024 ** 3), 2), "GB")
print("Available Memory:", round(memory.available / (1024 ** 3), 2), "GB")
print("Used Memory:", round(memory.used / (1024 ** 3), 2), "GB")
print("Memory Usage:", memory.percent, "%")

print_section("DISK INFORMATION")
disk = psutil.disk_usage("/")
print("Total Disk Space:", round(disk.total / (1024 ** 3), 2), "GB")
print("Used Disk Space:", round(disk.used / (1024 ** 3), 2), "GB")
print("Free Disk Space:", round(disk.free / (1024 ** 3), 2), "GB")
print("Disk Usage:", disk.percent, "%")

print_section("NETWORK INFORMATION")
network = psutil.net_io_counters()
print("Bytes Sent:", round(network.bytes_sent / (1024 ** 2), 2), "MB")
print("Bytes Received:", round(network.bytes_recv / (1024 ** 2), 2), "MB")

print_section("SSH CONNECTIVITY")
ssh_host = "127.0.0.1"
ssh_port = 22

try:
    with socket.create_connection((ssh_host, ssh_port), timeout=3):
        print(f"SSH port {ssh_port} on {ssh_host} is OPEN (reachable).")
except (socket.timeout, ConnectionRefusedError, OSError):
    print(f"SSH port {ssh_port} on {ssh_host} is NOT reachable.")

print_section("SYSTEM UPTIME")
boot_time = datetime.fromtimestamp(psutil.boot_time())
print("System Boot Time:", boot_time)

uptime_seconds = datetime.now().timestamp() - psutil.boot_time()
uptime_hours = uptime_seconds / 3600
print("System Uptime:", round(uptime_hours, 2), "hours")

print_section("LOGGED IN USERS")
users = psutil.users()
if users:
    for user in users:
        print("Username:", user.name)
        print("Terminal:", user.terminal)
        print("Login Time:", datetime.fromtimestamp(user.started))
else:
    print("No logged-in users found.")

print_section("RUNNING PROCESSES")
process_count = len(psutil.pids())
print("Number of Running Processes:", process_count)

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
```

## Explanation

The modification adds a new section called SSH CONNECTIVITY. It uses Python’s socket library to attempt a connection to 127.0.0.1 on port 22. If the port is open, it prints that SSH is reachable. If the connection times out or is refused, it prints that SSH is not reachable. This is useful because a system administrator may want to confirm that SSH is available before trying to log in remotely.

This change improves the script because it checks both system performance and service availability. Instead of only reporting hardware status, the script now helps determine if a critical service is working. This makes it more useful for real-world monitoring and troubleshooting.

## Results from the Script

The output showed:

- SSH port 22 on 127.0.0.1 is OPEN (reachable)
- System Uptime: 1.02 hours
- Logged-in users: abdullah on both seat0 and tty2
- Number of Running Processes: 204
- CPU usage is normal
- Memory usage is normal
- Disk usage is normal

This confirms that the VM was functioning properly and that SSH was active and accepting connections.

## Peer Response

Great job! I like how you added the SSH connectivity check because it makes the script more useful than just reporting CPU and memory. This is a practical improvement because it tells you whether the service is actually reachable before troubleshooting other issues.
