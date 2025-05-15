# monitor/views.py
import speedtest
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import localtime
import psutil

def get_network_speed():
    """
    Run a speed test and return download speed, upload speed, and ping.
    """
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / (1024 * 1024)  # Convert to Mbps
        upload_speed = st.upload() / (1024 * 1024)      # Convert to Mbps
        ping = st.results.ping
        return {
            "download_speed": f"{download_speed:.2f} Mbps",
            "upload_speed": f"{upload_speed:.2f} Mbps",
            "ping": f"{ping:.2f} ms"
        }
    except Exception:
        return {
            "download_speed": "N/A",
            "upload_speed": "N/A",
            "ping": "N/A"
        }


def get_cpu_temperature():
    """
    Read the CPU temperature directly from the system file.
    Returns the temperature in degrees Celsius, or None on error.
    """
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_str = f.read().strip()
            return float(temp_str) / 1000.0  # Convert from millidegrees to degrees
    except Exception:
        return None


def index(request):
    """Render the monitoring dashboard."""
    return render(request, 'monitor/index.html')


def system_stats(request):
    """Return Raspberry Pi system statistics, including network speed."""
    cpu_temp = get_cpu_temperature()
    vm = psutil.virtual_memory()
    d = psutil.disk_usage('/')
    # network_speed = get_network_speed()

    data = {
        'cpu_temp': f"{cpu_temp:.2f}" if cpu_temp is not None else "N/A",
        'cpu_usage': psutil.cpu_percent(interval=1),
        'ram_usage': vm.percent,
        'ram_available': f"{(vm.available / (1024*1024)):.2f} MB",
        'ram_used_total': f"{(vm.used / (1024*1024)):.2f} MB / {(vm.total / (1024*1024)):.2f} MB",
        'disk_usage': d.percent,
        'disk_used_total': f"{(d.used / (1024**3)):.2f} GB / {(d.total / (1024**3)):.2f} GB",
        # 'download_speed': network_speed["download_speed"],
        # 'upload_speed': network_speed["upload_speed"],
        # 'ping': network_speed["ping"],
        'last_updated': localtime().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return JsonResponse(data)