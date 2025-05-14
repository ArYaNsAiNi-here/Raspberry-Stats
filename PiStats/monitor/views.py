# monitor/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
import psutil


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
    """Return Raspberry Pi system statistics as JSON."""
    cpu_temp = get_cpu_temperature()
    vm = psutil.virtual_memory()
    d = psutil.disk_usage('/')

    data = {
        'cpu_temp': f"{cpu_temp:.2f}" if cpu_temp is not None else "N/A",
        'cpu_usage': psutil.cpu_percent(interval=1),
        'ram_usage': vm.percent,  # Percentage of RAM used
        'ram_available': f"{(vm.available / (1024 * 1024)):.2f} MB",
        'ram_used_total': f"{(vm.used / (1024 * 1024)):.2f} MB / {(vm.total / (1024 * 1024)):.2f} MB",
        'disk_usage': d.percent,  # Percentage of disk used
        'disk_used_total': f"{(d.used / (1024 ** 3)):.2f} GB / {(d.total / (1024 ** 3)):.2f} GB",
        'last_updated': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return JsonResponse(data)