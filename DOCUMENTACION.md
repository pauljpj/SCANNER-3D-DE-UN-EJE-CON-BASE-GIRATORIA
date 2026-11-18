# Documentación del proyecto

**Escáner por barrido angular de un eje con base giratoria**  
ESPOL · Sistemas Embebidos · Paralelo 104  
Estefano Jara · Justin Coronel

## Documento técnico oficial

El documento de diseño presentado por el equipo se encuentra **ya publicado en la raíz del repositorio**:

### 📄 [Abrir el Documento de Diseño en PDF](<../Documento_Diseno_Escaner_3D_Diagramas_Integrados_104 EPJARA JUSCORONEL.pdf>)

Este PDF de **cinco páginas** contiene el desarrollo académico del proyecto. Se conserva como fuente principal, sin sustituir su redacción por una versión resumida.

**Contenido del documento:**

1. Introducción y resumen técnico justificativo.
2. Alcance y limitaciones.
3. Diagrama de contexto.
4. Diagrama de bloques del diseño y geometría de adquisición.
5. Diagrama de software: máquina de estados y secuencia.
6. Diseño de interfaces.
7. Alternativas de diseño.
8. Plan de test y validación.
9. Consideraciones éticas.

## Diagramas ya publicados en GitHub

Los siguientes recursos están en la **raíz** del repositorio. Se enlazan directamente y **no se vuelven a subir ni duplicar**.

### 1. Contexto del sistema

![Diagrama de contexto](../01_contexto.png)

[Ver imagen original](../01_contexto.png)

El diagrama sitúa al operador, al objeto, a la alimentación y al entorno alrededor del sistema de adquisición.

### 2. Bloques del diseño

![Diagrama de bloques](../02_bloques.png)

[Ver imagen original](../02_bloques.png)

Representa control, sensado, actuación, energía y procesamiento. Incluye también un motor vertical previsto en una arquitectura ampliada.

### 3. Secuencia de adquisición

![Secuencia del escaneo](../03_secuencia.png)

[Ver imagen original](../03_secuencia.png)

Presenta el recorrido lógico desde la configuración y la lectura hasta el almacenamiento y la reconstrucción.

### 4. Máquina de estados

![Máquina de estados](../04_estados.png)

[Ver imagen original](../04_estados.png)

Contempla configuración, referencia, barrido, pausa, procesamiento, exportación y atención de fallos.

### 5. Diagrama de conexiones de Raspberry Pi

![Diagrama de conexiones entre Raspberry Pi y periféricos](<../Diagrama de conexiones para escáner 3D Raspberry Pi.png>)

[Ver diagrama de conexiones completo](<../Diagrama de conexiones para escáner 3D Raspberry Pi.png>)

Este recurso representa el esquema visual de cableado para la Raspberry Pi y sus periféricos. Antes de construirlo, es indispensable verificar que el pinout y los componentes indicados coincidan con los disponibles físicamente.

## Aclaración del diseño implementable

**El alcance académico definido en el documento oficial es un barrido angular de un solo eje.** El sensor VL53L0X permanece a altura fija y la plataforma hace girar el objeto. Algunos diagramas del material original contienen referencias a un eje vertical, movimientos `Δz` y dos drivers; esas partes se consideran **ampliaciones futuras**, no requisitos del prototipo de un eje.

Al estar fija la altura `z₀`, la transformación descrita en el documento obtiene puntos de un perfil en el plano XY. Una exportación STL cerrada e imprimible **no es un resultado garantizado**.

## Programa del proyecto

El archivo de código existente en el repositorio es:

- [escaner_3d_raspberry_vl53l0x final.py](<../escaner_3d_raspberry_vl53l0x final.py>)

## Plan de validación

El PDF define comprobaciones de comunicación I²C, calibración del sensor, retorno a una referencia angular, sincronización de muestras, perfil cilíndrico, repetibilidad, exportación de archivos, comportamiento ante fallos y seguridad eléctrica. Sus criterios son **objetivos propuestos**, no mediciones declaradas como ya obtenidas.

## Repositorio principal

[Volver al README del proyecto](../README.md)
