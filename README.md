# Entrega 5 - Laboratorio de Robotica

## UR5 con gripper - ROS 2 Humble y MoveIt 2

Implementacion de una simulacion de un robot UR5
con pinza utilizando ROS 2 Humble, Gazebo y MoveIt 2.

## Repositorio base

https://github.com/DanielPalominoS/ur5_gripper_packages

El archivo adaptaciones_repositorio_base.patch
contiene los cambios realizados sobre los archivos
versionados del repositorio original para adaptar
la simulacion.

## Paquetes desarrollados

### 1. pick_place_ur5

Nodo que ejecuta una rutina Pick and Place simulada
en tres configuraciones articulares, incluyendo
movimientos del brazo y comandos de apertura y
cierre de la pinza.

Ejecutar:

ros2 run pick_place_ur5 pick_place_node

### 2. ur5_moveit_config

Paquete generado mediante MoveIt Setup Assistant.

Grupos configurados:
- ur5_arm
- gripper

Incluye poses de referencia, configuracion
cinematica, controladores y archivos de lanzamiento.

### 3. moveit_ur5_ejecucion

Nodo que utiliza MoveIt para planificar y ejecutar
una trayectoria del brazo UR5.

Ejecutar:

ros2 run moveit_ur5_ejecucion ejecutar_trayectoria

## Entorno utilizado

- Ubuntu 22.04.5 LTS
- ROS 2 Humble
- Gazebo Sim
- MoveIt 2
- Python

## Resultados

Se verificaron los movimientos articulares del UR5,
las operaciones de apertura y cierre del gripper,
la planificacion de trayectorias en RViz y la ejecucion
de una trayectoria mediante un nodo de MoveIt.

## Evidencias audiovisuales

Los videos de funcionamiento se entregan mediante
enlaces de Google Drive en el informe PDF.
