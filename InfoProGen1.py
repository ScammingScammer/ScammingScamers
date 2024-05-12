import logging
import socket
import platform
import subprocess
import uuid
import psutil  # Added psutil module for retrieving RAM information
import wmi

# Configure logging
logging.basicConfig(filename='system_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to get local IP address
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

# Function to get public IP address
def get_public_ip():
    return subprocess.check_output(['curl', 'ifconfig.me'], stderr=subprocess.DEVNULL).decode().strip()

# Function to get CPU information
def get_cpu():
    return platform.processor()

# Function to get username
def get_username():
    return subprocess.check_output(['whoami']).decode().strip()

# Function to get hostname
def get_hostname():
    return socket.gethostname()

# Function to get HWID (Hardware ID)
def get_hwid():
    return uuid.getnode()

# Function to get MAC address
def get_mac():
    return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])

# Function to get GPU information
def get_gpu():
    c = wmi.WMI()
    for gpu in c.Win32_VideoController():
        return gpu.Name

# Function to get monitor information
def get_monitor_info():
    c = wmi.WMI()
    monitors = c.Win32_DesktopMonitor()
    monitor_count = len(monitors)
    monitor_info = []
    for monitor in monitors:
        if hasattr(monitor, 'ScreenWidth') and hasattr(monitor, 'ScreenHeight'):
            resolution = f"{monitor.ScreenWidth}x{monitor.ScreenHeight}"
            monitor_info.append(f"{monitor.Description}: {resolution}")
        else:
            monitor_info.append("Unknown")
    return monitor_count, monitor_info

# Function to get refresh rate information
def get_refresh_rate_info():
    c = wmi.WMI()
    refresh_rate_info = []
    for display in c.Win32_VideoController():
        refresh_rate_info.append(f"{display.CurrentRefreshRate}Hz")
    return refresh_rate_info

# Function to get RAM information
def get_ram():
    return str(round(psutil.virtual_memory().total / (1024 ** 3), 2)) + " GB"

# Function to get operating system information
def get_os_info():
    return platform.platform()

# Main function
def main():
    logging.info('Local IP: ' + get_local_ip())
    logging.info('Public IP: ' + get_public_ip())
    logging.info('Operating System: ' + get_os_info())
    logging.info('CPU: ' + get_cpu())
    logging.info('RAM: ' + get_ram())  # Added RAM information to logging
    logging.info('Username: ' + get_username())
    logging.info('Hostname: ' + get_hostname())
    logging.info('HWID: ' + str(get_hwid()))
    logging.info('MAC Address: ' + get_mac())
    logging.info('GPU: ' + str(get_gpu()))
    monitor_count, monitor_info = get_monitor_info()
    logging.info('Monitor Count: ' + str(monitor_count))
    for info in monitor_info:
        logging.info('Monitor: ' + info)
    refresh_rate_info = get_refresh_rate_info()
    for rate in refresh_rate_info:
        logging.info('Refresh Rate: ' + rate)

if __name__ == "__main__":
    main()
