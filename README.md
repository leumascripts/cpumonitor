# CPU-Shield 🛡️

**CPU-Shield** is a powerful, lightweight Python utility designed to monitor system resources, alert the user about CPU spikes, and provide an automated defense mechanism against runaway processes.

## 🚀 Key Features
- **Real-time Monitoring**: Analyzes CPU usage at randomized intervals to detect anomalies.
- **Active Defense**: Automatically terminates non-whitelisted processes that exceed 90% CPU usage.
- **Detailed Logging**: Records all alerts, including timestamps and the top 3 offending processes (PID, Name, CPU%).
- **Cross-Platform Notifications**: Native desktop alerts for **Windows, macOS, and Linux**.
- **Safety Whitelist**: Built-in protection for critical system processes.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/leumascripts/cpu-shield-py.git](https://github.com/leumascripts/cpu-shield-py.git)
   cd cpu-shield-py

   Install dependencies: pip install -r requirements.txt

## 💻 Usage

2. **Since the script needs to manage system processes, it must be run with administrative privileges**:

    Windows: Run PowerShell or Command Prompt as Administrator.

    Linux/macOS: sudo python cpu_shield.py

## ⚙️ Configuration

3. **You can customize the behavior directly in the script**:

    CPU_THRESHOLD: Percentage to trigger logs (default: 80%).

    PROCESS_WHITELIST: List of processes that the script will never terminate.

    MAX_CONSECUTIVE: Number of high-CPU checks before the safety shutdown/hibernation sequence.

## ⚠️ Disclaimer

This tool is powerful. The Active Defense feature will terminate processes. Ensure you have added your critical work applications to the PROCESS_WHITELIST to avoid data loss. The author is not responsible for any system instability or data loss.

## 📄 License

Distributed under the MIT License. See LICENSE for more information.
