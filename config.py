"""
config.py
Configuración general del sistema de detección de gestos
"""

# ========== CONFIGURACIÓN DE MEDIAPIPE ==========
MEDIAPIPE_CONFIG = {
    'static_image_mode': False,
    'max_num_hands': 4,
    'min_detection_confidence': 0.7,
    'min_tracking_confidence': 0.7,
    'model_complexity': 1  # 0=lite, 1=full (más preciso)
}

# ========== CONFIGURACIÓN DE CÁMARA ==========
CAMERA_CONFIG = {
    'width': 1280,
    'height': 720,
    'fps': 30,
    'backend': 'cv2.CAP_DSHOW'  # Windows
}

# ========== CONFIGURACIÓN DE DETECCIÓN ==========
DETECTION_CONFIG = {
    'frames_confirmacion': 3,  # Frames consecutivos para confirmar gesto
}

# ========== UMBRALES DE DISTANCIA ==========
DISTANCE_THRESHOLDS = {
    'muy_cerca': 0.04,
    'cerca': 0.08,
    'medio': 0.12,
    'lejos': 0.18
}

# ========== UMBRALES DE ÁNGULOS ==========
ANGLE_THRESHOLDS = {
    'doblado': 140,      # grados - menos de esto está doblado
    'extendido': 160     # grados - más de esto está extendido
}

# ========== CONFIGURACIÓN DE AUDIO ==========
AUDIO_CONFIG = {
    'archivos': {
        'A': 'A.WAV',
        'E': 'e.mp3',
        'I': 'i.mp3',
        'O': 'o.mp3',
        'U': 'u.mp3'
    }
}

# ========== CONFIGURACIÓN VISUAL ==========
VISUAL_CONFIG = {
    'colores': {
        'landmarks': (0, 255, 0),      # Verde
        'conexiones': (255, 0, 0),     # Rojo
        'bbox': (0, 255, 255),         # Cian
        'texto_confirmado': (0, 255, 0),    # Verde
        'texto_detectando': (255, 165, 0),  # Naranja
        'texto_sin_gesto': (80, 80, 80)     # Gris
    },
    'grosor': {
        'landmarks': 2,
        'conexiones': 2,
        'bbox': 2,
        'texto_normal': 2,
        'texto_gesto': 3
    },
    'tamaños': {
        'circulo_landmark': 3,
        'circulo_centro': 4,
        'fuente_info': 0.6,
        'fuente_gesto': 1.0,
        'fuente_detectando': 0.7,
        'fuente_fps': 0.8
    }
}

# ========== TOLERANCIAS PARA GESTOS ==========
GESTURE_TOLERANCES = {
    'O': {
        'variacion_altura_max': 0.08  # Variación máxima en altura de tips
    },
    'U': {
        'diferencia_altura_max': 0.05  # Diferencia máxima entre índice y medio
    },
    'I': {
        'altura_relativa': True  # Meñique debe estar más alto que medio
    },
    'A': {
        'pulgar_separado': True  # Pulgar debe estar separado del puño
    },
    'E': {
        'pulgar_toca_dedos': True  # Pulgar debe tocar los dedos doblados
    }
}