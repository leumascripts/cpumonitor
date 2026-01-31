import psutil           
import time
import datetime
import random
import subprocess
import platform

# Constants
CPU_THRESHOLD = 80.0  # CPU usage percentage above which an alert is sent
INTERVAL = 2
LOG_FILE = "system_alert.log"
MAX_CONSECUTIVE = 3
PROCESS_WHITELIST = ["explorer.exe", "cpumonitor.py", "kernel_task.exe", "System Idle Process", "System", "python.exe", "taskhostw.exe", "services.exe", "wininit.exe"]

def analyze_system():
    """Analyzes current CPU usage."""
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage > CPU_THRESHOLD, cpu_usage

def log_alert(value):
    """Logs the alert details to a file and sends a notification."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{timestamp}] ALERT: CPU Usage at {value}%\n"
    message += "Top CPU-consuming processes:\n"
    
    heavy_processes = get_heavy_processes()
    for p in heavy_processes:
        message += f"  PID: {p['pid']}, Name: {p['name']}, CPU%: {p['cpu_percent']}\n"
    
    with open(LOG_FILE, "a") as log_file: 
        log_file.write(message + "-"*20 + "\n")
    
    print(message.strip())
    send_notification("High CPU Alert", f"CPU usage is at {value}%\nCheck logs for details.")
    
    # Active defense trigger if needed
    active_defense(heavy_processes)

def get_heavy_processes():
    """Returns a list of the top 3 processes consuming the most CPU."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            info = proc.info
            # Filter out whitelisted processes
            if info['name'].lower() not in [n.lower() for n in PROCESS_WHITELIST]:
                processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue    

    # Sort processes by CPU usage in descending order
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:3]

def send_notification(title, message):
    """Sends a system notification based on the OS."""
    os_type = platform.system()
    try:
        if os_type == "Windows":    
            powershell_cmd = (
                f'[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null; '
                f'$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02); '
                f'$textNodes = $template.GetElementsByTagName("text"); '
                f'$textNodes.Item(0).AppendChild($template.CreateTextNode("{title}")) > $null; '
                f'$textNodes.Item(1).AppendChild($template.CreateTextNode("{message}")) > $null; '
                f'$toast = [Windows.UI.Notifications.ToastNotification]::new($template); '
                f'$notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Python App"); '
                f'$notifier.Show($toast);'
            )
            subprocess.run(['powershell', '-Command', powershell_cmd])
        elif os_type == "Darwin":  # macOS
            subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'])
        elif os_type == "Linux":
            subprocess.run(['notify-send', title, message])
    except Exception as e:
        print(f"Error sending notification: {e}")

def active_defense(critical_processes):
    """Terminates processes exceeding 90% CPU usage during an alert."""
    for p in critical_processes:
        if p['cpu_percent'] > 90.0:
            try:
                if p['name'].lower() in [n.lower() for n in PROCESS_WHITELIST]:
                    print(f"[!] Process {p['name']} (PID: {p['pid']}) is whitelisted. No action taken.\n")
                    continue

                proc_to_kill = psutil.Process(p['pid'])
                name = p['name']
                print(f"[!] ACTIVE DEFENSE: Forcibly terminating {name} (PID: {p['pid']}) due to excessive CPU usage ({p['cpu_percent']}%).\n")
                
                proc_to_kill.terminate()
                time.sleep(0.5)
                if proc_to_kill.is_running():
                    proc_to_kill.kill()
                    print(f"Process {name} (PID: {p['pid']}) killed forcefully.\n")
                else:
                    print(f"Process {name} (PID: {p['pid']}) terminated successfully.\n")
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(f"Unable to terminate process: Access Denied or Process Ended. {e}")

def main():
    print("Welcome to the CPU Monitoring System.\nMonitoring in progress...\n")
    alert_counter = 0
    
    try:
        while True:
            is_alert, cpu_usage = analyze_system()
            
            if is_alert:
                alert_counter += 1
                log_alert(cpu_usage)
            else:
                alert_counter = 0
                print(f"CPU usage is at {cpu_usage}%. System stable.\n")

            if alert_counter >= MAX_CONSECUTIVE:
                print("Warning: High CPU usage detected for more than 3 consecutive checks.\nSystem will hibernate for safety reasons.\n")
                # Note: This is a simulation of hibernation logic.
                time.sleep(random.randint(1, 5)) 
                break

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nMonitoring stopped manually by the user.\n")
        time.sleep(1)

if __name__ == "__main__":
    main()

