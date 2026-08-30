# Lab 1 – Introduction to DevOps: Traditional Ops with Python

College of Computer & Information Sciences  
Regis University  

---

## Abstract

This paper describes the steps taken to complete Lab #1 of MSES602, which focused on traditional systems operations using an Ubuntu 20.04 LTS Virtual Machine. The lab covered installing and verifying SSH, Python 3, pip, and Git, cloning a DevOps utilities repository, and running several Python scripts for password security auditing, network monitoring, and system environment checks. The lab was extended by modifying `envChk.py` to include SSH connectivity testing, system uptime, logged-in users, running process counts, and automated status warnings.

**Keywords:** DevOps, Ubuntu, SSH, Python, psutil, scripting, automation

---

## Introduction

The purpose of this lab was to practice traditional systems administration tasks manually and through Python scripting on an Ubuntu 20.04 LTS Virtual Machine. As described in the DevOps Handbook, manual system setup is error-prone, time-consuming, and expensive. John Willis's CAMS model (Culture, Automation, Measurement, Sharing) emphasizes automation as a core DevOps principle. This lab provided hands-on experience with the foundational tools and scripts that form the basis of that automation, reinforcing the idea of treating systems as reproducible "cattle" rather than carefully maintained "pets."

---

## Procedure & Observations

### SSH Installation and Verification

After starting the Ubuntu VM, SSH was installed using the `apt` package manager and the service status was verified.

```bash
sudo apt install ssh
service ssh status
```

![SSH Service Status](images/sc1.png)

The SSH service was confirmed to be active and running. A loopback connection was then tested to verify that SSH was accepting connections on `127.0.0.1`.

```bash
ssh osboxes@127.0.0.1
exit
```

![Successful SSH Connection](images/sc2.png)

The connection was successful. The loopback address `127.0.0.1` confirmed SSH was listening locally before testing with external connections.

---

### Python 3 and pip Installation

The Python 3 version was verified and `pip3` was installed to enable Python package management for later steps.

```bash
python3 --version
sudo apt install python3-pip
pip3 --version
pip --help
```

![Python3 and Pip](images/sc3.png)

Python 3 was already present on the Ubuntu image. pip3 was successfully installed and confirmed working.

---

### Git Installation

Git was installed to support version-controlled scripts and repository cloning — a foundational DevOps practice.

```bash
sudo apt install git
git --version
```

![Git Version](images/sc4.png)

Git was installed and confirmed at an acceptable version. Storing scripts in Git repositories is a key DevOps practice that ensures repeatability and collaboration.

---

### Cloning the DevOps Utilities Repository

A `Projects` directory was created and the MSES602 DevOps utilities repository was cloned from GitHub. The Python scripts used in subsequent steps were located inside the cloned directory.

```bash
cd
mkdir Projects
cd Projects
git clone https://github.com/RegisUniversity/MSES602_DevOpsUtils.git
cd ./MSES_DevOpsUtils/src/python3
ls
```

![Cloned Repository and Python Files](images/sc5.png)

The repository cloned successfully and the Python scripts were visible and accessible.

---

### Running passChk.py – Password Security Audit

The `passChk.py` script reads the system user and password files and flags any accounts with short usernames or passwords that could be easily guessed by brute-force tools.

```bash
python3 passChk.py
```

![passChk.py Output](images/sc6.png)

The output flagged several accounts. Most were system-level accounts rather than active user accounts. The script source was then reviewed in `nano` to understand its logic.

```bash
nano passChk.py
```

![passChk.py Source Code](images/sc7.png)

Reviewing the code showed how it opens `/etc/passwd` and `/etc/shadow`, iterates over accounts, and applies length thresholds. Running this check manually every day would be tedious — automating it with a script makes the process consistent and fast.

---

### Running netmon.py – Network Monitor

The `netmon.py` script polls network connectivity at intervals and reports whether the network is reachable. It can be extended to trigger alerts or corrective actions on failure.

```bash
python3 netmon.py
```

![netmon.py Running](images/sc8.png)

The script reported the network as up and continued sleeping between checks. This type of lightweight monitor is useful when diagnosing intermittent connectivity issues from the application side.

---

### Extending envChk.py – System Environment Check

For the final task, `psutil` was installed and the `envChk.py` script was extended into `lab1.py` with the following additional capabilities beyond the original:

- SSH connectivity check (port 22 on localhost)
- System uptime since last boot
- Logged-in users
- Running process count
- Threshold-based status warnings for CPU, memory, and disk

```bash
pip3 install psutil
python3 lab1.py
```

The extended script `lab1.py`:

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
print("System Uptime:", round(uptime_seconds / 3600, 2), "hours")

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
print("Number of Running Processes:", len(psutil.pids()))

print_section("SYSTEM STATUS")
print("WARNING: CPU usage is high." if cpu_usage > 80 else "CPU usage is normal.")
print("WARNING: Memory usage is high." if memory.percent > 80 else "Memory usage is normal.")
print("WARNING: Disk usage is high." if disk.percent > 80 else "Disk usage is normal.")

print()
print("System environment check completed.")
```

![Script Output – System and CPU Info](images/sc9.png)

![Script Output – Memory, Disk, and Network](images/sc10.png)

![Script Output – SSH Check, Uptime, Users, and Status](images/sc11.png)

The script ran successfully. The SSH connectivity check confirmed port 22 was open, and all system status indicators were within normal thresholds. Adding SSH connectivity to the environment check is a useful real-world addition — an operator running this script can immediately know whether the SSH service is reachable without running a separate command.

---

## Conclusions

This lab demonstrated the process of manually setting up an Ubuntu VM and running Python-based operational scripts. The steps covered SSH setup, Python and pip verification, Git installation, repository cloning, password auditing, network monitoring, and system environment checking. Each task illustrated why automating these operations with scripts stored in version-controlled repositories is preferable to manual execution. The extended `lab1.py` script added practical monitoring features — SSH connectivity, uptime, user sessions, and process counts — that give an operator a comprehensive system snapshot in a single command. As emphasized in the DevOps Handbook, this type of automation is central to the CAMS model and is the foundation for moving from treating systems as "pets" to treating them as reproducible "cattle."

---

## References

Willis, J., Debois, P., Humble, J., & Kim, G. (2021). *The DevOps Handbook: How to Create World-Class Agility, Reliability, & Security in Technology Organizations, 2nd ed.* IT Revolution Press.

Linuxize (2018). How to install Pip on Ubuntu 18.04.

Menchaca, J. (2018). DevOps Concepts: Pets vs Cattle.

Parkash, A. (2018). Using apt-get Commands in Linux [Complete Beginners Guide].

Rendek, L. (2018). Enable SSH on Ubuntu 18.04 Bionic Beaver Linux.

Willis, J. (2011a). DevOps Culture (Part 1). IT Revolution Press.

psutil documentation. https://psutil.readthedocs.io/en/latest/
