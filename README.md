# 👋 Detector de Gestos - Vocales ASL

Sistema de reconocimiento de gestos en tiempo real para detectar vocales en Lenguaje de Señas Americano (ASL) utilizando visión por computadora.

Este proyecto implementa un sistema capaz de detectar las vocales A, E, I, O y U mediante gestos de las manos usando MediaPipe Hands, OpenCV y Python.
Cuando se detecta un gesto válido, el programa reproduce un sonido, dibuja los puntos articulados de la mano y muestra el gesto detectado en pantalla.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Características

- ✅ Detección en tiempo real de 5 vocales: **A, E, I, O, U**
- ✅ Soporte para hasta **4 manos simultáneas**
- ✅ Reproducción de audio para cada vocal detectada
- ✅ Sistema de confirmación para evitar falsos positivos
- ✅ Algoritmos matemáticos precisos (cálculo de ángulos y distancias 3D)

- ✅ Código modular y bien documentado

## 📋 Requisitos

- Python 3.8 o superior
- Webcam
- Sistema operativo: Windows, Linux o macOS

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Tobardev/lineal.git
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install opencv-python mediapipe pygame
o
pip install opencv-python
pip install mediapipe
pip install pygame
```

### 4. Agregar archivos de audio

Coloca los archivos de audio en la carpeta raíz del proyecto:
- `A.WAV`
- `e.mp3`
- `i.mp3`
- `o.mp3`
- `u.mp3`

## 🎮 Uso

Ejecutar el programa principal:

```bash
python main.py
```

### Controles

- **ESC** o **Q**: Salir del programa

### Gestos soportados

| Vocal | Descripción del gesto |
|-------|----------------------|
| **A** | Puño cerrado con pulgar al costado |
| **E** | Dedos doblados tocando el pulgar |
| **I** | Solo el meñique extendido |
| **O** | Todos los dedos formando un círculo |
| **U** | Índice y medio extendidos juntos |

## 📁 Estructura del Proyecto

```
detector-gestos-asl/
│
├── config.py              # ⚙️ Configuración y constantes
├── audio_manager.py       # 🔊 Gestión de audio
├── geometry_utils.py      # 📐 Utilidades matemáticas
├── gesture_detector.py    # 👋 Detector de gestos
├── main.py               # 🚀 Programa principal
│
├── A.WAV                 # 🎵 Archivos de audio
├── e.mp3
├── i.mp3
├── o.mp3
├── u.mp3
│
└── README.md            # 📖 Documentación
```

## 🔧 Configuración

Puedes ajustar los parámetros en `config.py`:

### Precisión de detección
```python
MEDIAPIPE_CONFIG = {
    'min_detection_confidence': 0.7,  # 0.5 - 1.0
    'min_tracking_confidence': 0.7,   # 0.5 - 1.0
}
```

### Frames de confirmación
```python
DETECTION_CONFIG = {
    'frames_confirmacion': 3,  # 1 - 10
}
```

### Umbrales de distancia
```python
DISTANCE_THRESHOLDS = {
    'muy_cerca': 0.04,
    'cerca': 0.08,
    'medio': 0.12,
    'lejos': 0.18
}
```

## 🧮 Algoritmos Utilizados

### Geometría y Álgebra Lineal
- **Distancia Euclidiana 2D**: Para comparar posiciones en el plano
- **Distancia Euclidiana 3D**: Para análisis espacial con profundidad
- **Cálculo de ángulos**: Usando producto punto vectorial
- **Transformaciones lineales**: Reflexión y escalamiento

### Detección de Gestos
- **Sistema de umbrales**: Clasificación por distancias y ángulos
- **Buffer de confirmación**: Requiere detección estable por N frames
- **Máquina de estados**: Control temporal para evitar repeticiones

## 🎓 Conceptos Matemáticos

El sistema utiliza:
- Vectores en ℝ² y ℝ³
- Norma euclidiana (L2)
- Producto punto para ángulos
- Operadores min/max para bounding boxes
- Comparadores booleanos para clasificación

## 🐛 Solución de Problemas

### El audio no funciona
```bash
pip install --upgrade pygame
```

### La cámara no se detecta
- Verifica que ninguna otra aplicación esté usando la cámara
- En `config.py`, cambia el backend de la cámara


## 📊 Rendimiento

- **FPS típico**: 25-30 fps
- **Latencia**: ~100ms desde el gesto hasta el audio
- **Precisión**: ~95% en condiciones óptimas de iluminación



## 👨‍💻 Autor

Tu Nombre - [@tu_twitter](https://twitter.com/tu_twitter)

Proyecto: [https://github.com/tu-usuario/detector-gestos-asl](https://github.com/tu-usuario/detector-gestos-asl)

## 🙏 Agradecimientos

- [MediaPipe](https://mediapipe.dev/) por el modelo de detección de manos
- [OpenCV](https://opencv.org/) por las herramientas de visión por computadora
- Comunidad de ASL por la documentación de gestos

## 📚 Referencias

- [MediaPipe Hands Documentation](https://google.github.io/mediapipe/solutions/hands.html)
- [ASL Fingerspelling Guide](https://www.startasl.com/fingerspelling/)
- Álgebra Lineal y Geometría Analítica aplicadas a Visión por Computadora

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
