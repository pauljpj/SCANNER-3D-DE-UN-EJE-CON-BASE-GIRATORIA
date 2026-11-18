# Escáner 3D de un eje con base giratoria

**Escuela Superior Politécnica del Litoral (ESPOL)** · Sistemas Embebidos · Paralelo 104  
**Integrantes:** Estefano Jara y Justin Coronel

## Descripción

Este proyecto propone un prototipo académico para digitalizar el contorno externo de un objeto utilizando una **Raspberry Pi 4**, un sensor de distancia **ToF VL53L0X** y una **base giratoria accionada mediante un motor paso a paso**. La Raspberry Pi coordina el giro y la adquisición de mediciones a través de comunicación **I²C** y señales **GPIO**.

El sensor permanece fijo mientras la pieza gira; cada distancia medida se asocia a un ángulo para obtener un perfil geométrico. El objetivo es integrar **sensado, control de motores, sincronización, procesamiento y almacenamiento de datos** en un sistema embebido.

> **Alcance:** el diseño académico actual comprende **un eje angular** y una altura de medición en el plano Z. La ampliación a un eje vertical aparece en algunos diagramas del proyecto. El resultado previsto es un perfil a altura variable junto a los dos motores paso a paso permitiendo la amplitud en la proyección de los puntos infrarrojos que posteriormente se convertirán en una nube de puntos. Este proyecto va dirigido a los estudiantes de mecatrónica que quieren hacer sus primeras impresiones 3d y practicar de manera continua la categorización y proyección de objetos menores de 12 cm.

## Documento de diseño y documentación

- 📄 **[Abrir el documento de diseño oficial en PDF](<Documento_Diseno_Escaner_3D_Diagramas_Integrados_104 EPJARA JUSCORONEL.pdf>)** — documento compartido por el equipo, con justificación, alcance, diagramas, software, interfaces y plan de validación.
- 📚 **[Ver la documentación del proyecto](docs/DOCUMENTACION.md)** — índice técnico con enlaces a los diagramas y a los archivos existentes del repositorio.

## Esquemas del proyecto

### Diagrama de conexiones de Raspberry Pi

![Conexiones de Raspberry Pi, sensor y drivers](<Diagrama de conexiones para escáner 3D Raspberry Pi.png>)

[Ver imagen de conexiones en tamaño original](<Diagrama de conexiones para escáner 3D Raspberry Pi.png>)

### Diagramas del documento

| Diagrama | Archivo del repositorio |
|---|---|
| Contexto del sistema | [01_contexto.png](01_contexto.png) |
| Bloques de control, sensado y actuación | [02_bloques.png](02_bloques.png) |
| Secuencia de adquisición | [03_secuencia.png](03_secuencia.png) |
| Máquina de estados | [04_estados.png](04_estados.png) |

**Nota de interpretación:** los diagramas de contexto, bloques y secuencia incluyen una arquitectura de **dos ejes** como ampliación de diseño. Para el prototipo descrito en el PDF, se considera únicamente la base giratoria, con el sensor fijo a una altura.

## Componentes principales

| Componente | Función |
|---|---|
| Raspberry Pi 4 | Control de movimiento, lectura y gestión de archivos |
| Sensor VL53L0X | Medición de distancia por I²C |
| Driver de motor paso a paso | Interfaz entre GPIO y potencia del motor |
| Motor paso a paso | Giro incremental de la base |
| Plataforma giratoria y soporte | Sujeción del objeto y alineación del sensor |
| Alimentación | Energía de la Raspberry Pi y alimentación independiente del motor |

## Funcionamiento planteado

1. Definir la resolución angular y la cantidad de lecturas por posición.
2. Verificar la comunicación con el VL53L0X y establecer el origen angular.
3. Girar la base un incremento `Δθ` y esperar estabilización.
4. Adquirir y validar las lecturas de distancia, asociándolas a su posición angular.
5. Repetir hasta completar una vuelta.
6. Procesar los datos para representar el perfil y exportar resultados a **CSV/PLY**.

El criterio geométrico de referencia, desarrollado en el PDF, es:

$$r(\theta)=R-d(\theta)-o$$

$$x=r(\theta)\cos(\theta),\quad y=r(\theta)\sin(\theta),\quad z=z_0$$

Donde `R` es la distancia calibrada entre sensor y eje, `d(θ)` la medición, `o` el ajuste de cero y `z₀` una altura fija.

## Código fuente

- **[Consultar el programa Python del escáner](<escaner_3d_raspberry_vl53l0x final.py>)**

La configuración exacta de pines, el driver, la corriente del motor y la calibración deben verificarse con el hardware físico. La documentación describe **pruebas propuestas**, sin atribuir resultados experimentales aún no reportados.

## Validación y seguridad

Se han planteado pruebas de comunicación I²C, calibración ToF, retorno angular, sincronización, repetibilidad, exportación y parada segura. El motor no debe alimentarse directamente desde los GPIO de la Raspberry Pi; se debe emplear un driver y una fuente apropiada.

---

**ESPOL · Sistemas Embebidos · Paralelo 104**  
**Estefano Jara · Justin Coronel**
