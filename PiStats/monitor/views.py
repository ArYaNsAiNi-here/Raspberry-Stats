from django.shortcuts import render
from django.http import JsonResponse
import psutil
from gpiozero import CPUTemperature

def index(request):
    """Render the monitoring dashboard."""
    return render(request, 'monitor/index.html')

def system_stats(request):
    """Return Raspberry Pi system statistics."""
    try:
        cpu_temp = CPUTemperature().temperature
    except Exception as e:
        # Fallback if gpiozero cannot read the temperature
        cpu_temp = None

    data = {
        'cpu_temp': f"{cpu_temp:.2f}" if cpu_temp is not None else "N/A",
        'cpu_usage': psutil.cpu_percent(interval=1),
        'ram_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
    }
    return JsonResponse(data)