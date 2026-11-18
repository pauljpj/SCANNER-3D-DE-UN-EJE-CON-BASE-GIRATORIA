"""Prototipo de escáner 3D: Raspberry Pi 4 + VL53L0X + 2 A4988.




import csv
import math
import statistics
import time
from pathlib import Path

import board
import busio
import adafruit_vl53l0x
from gpiozero import OutputDevice, Button

# ----- AJUSTAR SEGÚN EL PROTOTIPO -----
STEPS_PER_REV = 200       # Pasos completos del motor; cambiar por microsteps si aplica
TURNTABLE_GEAR_RATIO = 1.0  # Vueltas motor / vuelta plataforma
LEAD_SCREW_REV_PER_CM = 8.0  # VALOR PROVISIONAL: medir el husillo real
LAYER_HEIGHT_MM = 0.5
MAX_HEIGHT_MM = 120.0
SENSOR_TO_CENTER_MM = 80.0   # Medir físicamente desde el plano de referencia
READINGS_PER_POINT = 5
STEP_HALF_PERIOD_S = 0.003
SETTLE_S = 0.04
MAX_VALID_MM = 1800  # Filtrado preliminar, depende del montaje y superficie
HOMING_MAX_STEPS = 25000    # Límite duro de movimiento durante homing
HOMING_DIRECTION_HIGH = True  # Confirmar con prueba mecánica
Z_UP_DIRECTION_HIGH = False   # Debe ser opuesta a HOMING_DIRECTION_HIGH
BASE_DIRECTION_HIGH = False
OUTPUT = Path('escaneo_3d.csv')

# BCM numbering (no numeración física)
base_step = OutputDevice(17, initial_value=False)
base_dir = OutputDevice(27, initial_value=False)
base_enable = OutputDevice(22, initial_value=True)  # A4988 EN activo en LOW
z_step = OutputDevice(23, initial_value=False)
z_dir = OutputDevice(24, initial_value=False)
z_enable = OutputDevice(25, initial_value=True)
z_limit = Button(5, pull_up=True, bounce_time=0.02)  # NO -> GND

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)


def pulse(pin):
    pin.on()
    time.sleep(STEP_HALF_PERIOD_S)
    pin.off()
    time.sleep(STEP_HALF_PERIOD_S)


def home_z():
    """Bajar hasta fin de carrera, con límite de pasos para evitar daños."""
    if z_limit.is_pressed:
        print('Fin de carrera activo. Comprueba posición antes de continuar.')
        return
    z_dir.value = HOMING_DIRECTION_HIGH
    z_enable.off()
    for _ in range(HOMING_MAX_STEPS):
        if z_limit.is_pressed:
            return
        pulse(z_step)
    raise RuntimeError('Homing abortado: no se detectó fin de carrera dentro del límite.')


def read_distance_mm():
    samples = []
    for _ in range(READINGS_PER_POINT):
        try:
            reading = int(sensor.range)
            if 0 < reading <= MAX_VALID_MM:
                samples.append(reading)
        except (OSError, RuntimeError):
            pass
    return statistics.median(samples) if samples else None


def scan():
    # Número entero de pasos por vuelta REAL de la plataforma.
    steps_per_turn = round(STEPS_PER_REV * TURNTABLE_GEAR_RATIO)
    if steps_per_turn < 1:
        raise ValueError('Configuración inválida de pasos de plataforma')
    steps_per_mm_z = STEPS_PER_REV * LEAD_SCREW_REV_PER_CM / 10.0
    if steps_per_mm_z <= 0 or LAYER_HEIGHT_MM <= 0:
        raise ValueError('Parámetros del eje Z inválidos')

    print('Iniciando homing Z...')
    home_z()
    print('Homing terminado; iniciando escaneo.')
    base_dir.value = BASE_DIRECTION_HIGH
    z_dir.value = Z_UP_DIRECTION_HIGH
    base_enable.off()
    z_enable.off()

    step_position_z = 0
    target_layer = 0
    with OUTPUT.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x_mm', 'y_mm', 'z_mm', 'angulo_grados', 'distancia_mm'])
        while target_layer * LAYER_HEIGHT_MM <= MAX_HEIGHT_MM + 1e-9:
            height_mm = step_position_z / steps_per_mm_z
            print(f'Capa {target_layer}: altura real estimada {height_mm:.3f} mm')
            for index in range(steps_per_turn):
                angle_rad = 2 * math.pi * index / steps_per_turn
                time.sleep(SETTLE_S)
                measured = read_distance_mm()
                if measured is not None:
                    radius = SENSOR_TO_CENTER_MM - measured
                    # No se acepta un punto situado más allá del centro de la pieza.
                    if radius >= 0:
                        writer.writerow([round(radius * math.cos(angle_rad), 3),
                                         round(radius * math.sin(angle_rad), 3),
                                         round(height_mm, 3),
                                         round(math.degrees(angle_rad), 3), measured])
                pulse(base_step)
            file.flush()
            target_layer += 1
            if target_layer * LAYER_HEIGHT_MM > MAX_HEIGHT_MM + 1e-9:
                break
            target_steps_z = round(target_layer * LAYER_HEIGHT_MM * steps_per_mm_z)
            for _ in range(max(0, target_steps_z - step_position_z)):
                pulse(z_step)
                step_position_z += 1
    print(f'CSV guardado: {OUTPUT.resolve()}')


def main():
    print('PRUEBA PREVIA: comprobar manualmente sentido del eje Z, final de carrera,')
    print('alimentación, corriente de drivers y geometría antes de iniciar.')
    if input('Escribe ESCANEAR para comenzar: ').strip() != 'ESCANEAR':
        print('Cancelado')
        return
    try:
        scan()
    finally:
        base_enable.on()  # A4988 deshabilitado
        z_enable.on()     # ATENCIÓN: si Z cae sin torque, usar soporte/freno
        for device in (base_step, base_dir, base_enable, z_step, z_dir, z_enable, z_limit):
            device.close()


if __name__ == '__main__':
    main()

import numpy as np
import pandas as pd
import open3d as o3d

# Leer archivo generado por Raspberry Pi
datos = pd.read_csv("scan_001.csv")

# Extraer las coordenadas tridimensionales
puntos = datos[["x_mm", "y_mm", "z_mm"]].to_numpy()

# Eliminar valores no válidos
puntos = puntos[np.isfinite(puntos).all(axis=1)]

# Crear nube de puntos
nube = o3d.geometry.PointCloud()
nube.points = o3d.utility.Vector3dVector(puntos)

# Guardar nube de puntos
o3d.io.write_point_cloud("nube_3d.ply", nube)

# Visualizar
o3d.visualization.draw_geometries([nube])
