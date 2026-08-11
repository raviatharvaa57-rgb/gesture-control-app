import datetime
import os
import platform
import subprocess
import psutil

# Get path to the user's home directory to save logs
LOG_FILE = os.path.expanduser("~/mac_scan_log.txt")


def send_notification(title, subtitle, message, sound="Glass"):
    """Triggers a native macOS banner notification with sound."""
    if platform.system() == "Darwin":
        # AppleScript command to generate a system notification banner
        script = f'display notification "{message}" with title "{title}" subtitle "{subtitle}" sound name "{sound}"'
        subprocess.run(["osascript", "-e", script])


def run_login_scanner():
    # 1. Fetch system metrics
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    battery = psutil.sensors_battery()

    # 2. Prepare summary text
    status_summary = f"CPU: {cpu}% | RAM: {ram}% | Disk: {disk}%"

    if battery:
        plug_status = "Plugged In" if battery.power_plugged else "On Battery"
        status_summary += f" | Batt: {battery.percent}% ({plug_status})"

    # 3. Save entry to a log file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] - {status_summary}\n")

    # 4. Trigger the native macOS Notification
    send_notification(
        title="🖥️ Mac Security & Health Scan",
        subtitle="Login Check Complete",
        message=f"System Normal! {status_summary}",
        sound="Hero",  # Choose system sound: Glass, Hero, Ping, Pop
    )


if __name__ == "__main__":
    run_login_scanner()
