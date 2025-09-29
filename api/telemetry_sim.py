import os
import time
import random
import requests
from datetime import datetime, timezone
import socket
import subprocess
import platform

# Configuration from environment variables
API_URL = os.getenv("API_URL", "http://localhost:8000/api/telemetry")
DEVICE_ID = os.getenv("DEVICE_ID", f"device-{random.randint(1000, 9999)}")
USER_ID = os.getenv("USER_ID", "user-123")
INTERVAL = int(os.getenv("INTERVAL", "10"))  # seconds
BOOT_TIME = datetime.now(timezone.utc).isoformat()

print(f"Starting telemetry simulator for {DEVICE_ID}")
print(f"API URL: {API_URL}")
print(f"Sending data every {INTERVAL} seconds")
print(f"Boot time: {BOOT_TIME}")


def get_cpu_usage():
    """Simulate CPU usage (0-100%)"""
    # Simulate realistic CPU patterns
    base = random.uniform(10, 40)
    spike = random.uniform(0, 60) if random.random() > 0.7 else 0
    return round(min(base + spike, 100), 2)


def get_ram_usage():
    """Simulate RAM usage (0-100%)"""
    # Simulate realistic RAM patterns (usually more stable)
    base = random.uniform(30, 70)
    variation = random.uniform(-10, 10)
    return round(min(max(base + variation, 0), 100), 2)


def get_disk_free():
    """Simulate free disk space (0-100%)"""
    # Disk space decreases slowly over time
    base = random.uniform(40, 80)
    return round(base, 2)


def get_temperature():
    """Simulate temperature in Celsius"""
    # Realistic temperature range for devices
    base = random.uniform(35, 60)
    spike = random.uniform(0, 20) if random.random() > 0.8 else 0
    return round(base + spike, 2)


def get_dns_latency():
    """Measure latency to 8.8.8.8 (Google DNS)"""
    try:
        # Try to ping 8.8.8.8
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", "-W", "2", "8.8.8.8"]

        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3
        )

        if result.returncode == 0:
            # Simulate realistic latency (5-100ms)
            return round(random.uniform(5, 100), 2)
        else:
            return None
    except Exception as e:
        print(f"Error checking DNS latency: {e}")
        return None


def check_connectivity():
    """Check connectivity to 8.8.8.8"""
    try:
        # Try to connect to 8.8.8.8 on port 53 (DNS)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(("8.8.8.8", 53))
        sock.close()

        # Return 1 if connected, 0 if not
        return 1 if result == 0 else 0
    except Exception as e:
        print(f"Error checking connectivity: {e}")
        return 0


def collect_telemetry():
    """Collect all telemetry data"""
    latency = get_dns_latency()
    connectivity = check_connectivity()

    # If latency check failed but connectivity is OK, use simulated latency
    if latency is None and connectivity == 1:
        latency = round(random.uniform(10, 50), 2)
    elif latency is None:
        latency = 0

    telemetry = {
        "device_id": DEVICE_ID,
        "user_id": USER_ID,
        "cpu_usage": get_cpu_usage(),
        "ram_usage": get_ram_usage(),
        "disk_free": get_disk_free(),
        "temperature": get_temperature(),
        "dns_latency": latency,
        "connectivity": connectivity,
        "boot_time": BOOT_TIME,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    return telemetry


def send_telemetry(data):
    """Send telemetry data to API"""
    try:
        response = requests.post(
            API_URL, json=data, timeout=5, headers={"Content-Type": "application/json"}
        )

        if response.status_code in [200, 201]:
            print(
                f"✓ Telemetry sent successfully - CPU: {data['cpu_usage']}%, "
                f"RAM: {data['ram_usage']}%, Temp: {data['temperature']}°C, "
                f"Connectivity: {data['connectivity']}"
            )
            return True
        else:
            print(f"✗ Failed to send telemetry. Status: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Error sending telemetry: {e}")
        return False


def main():
    """Main loop"""
    print("\n" + "=" * 60)
    print("Telemetry Simulator Started")
    print("=" * 60 + "\n")

    while True:
        try:
            telemetry = collect_telemetry()
            send_telemetry(telemetry)
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print("\n\nStopping telemetry simulator...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
