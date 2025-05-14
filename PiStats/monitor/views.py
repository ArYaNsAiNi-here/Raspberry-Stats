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
            # Temperature is provided in millidegrees Celsius. Convert to degrees.
            temp_str = f.read().strip()
            return float(temp_str) / 1000.0
    except Exception:
        return None

def index(request):
    """Render the monitoring dashboard."""
    return render(request, 'monitor/index.html')

def system_stats(request):
    """Return Raspberry Pi system statistics as JSON."""
    cpu_temp = get_cpu_temperature()
    data = {
        'cpu_temp': f"{cpu_temp:.2f}" if cpu_temp is not None else "N/A",
        'cpu_usage': psutil.cpu_percent(interval=1),
        'ram_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'last_updated': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return JsonResponse(data)