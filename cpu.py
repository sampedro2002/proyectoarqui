import psutil

def obtener_porcentaje_cpu():
    porcentaje = psutil.cpu_percent(interval=1)
    return porcentaje

porcentaje_cpu = obtener_porcentaje_cpu()

if porcentaje_cpu >= 10:
    alerta = (f"Alerta el uso del CPU esta en: {porcentaje_cpu}%")



