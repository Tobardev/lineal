"""
main.py
Programa principal para detección de gestos de vocales en lenguaje de señas
"""

import cv2 
import mediapipe as mp
import time 

from audiomanager.py import AudioManager


class GestureRecognitionApp:
    """Aplicacion principal de reconocimientos de gestos"""
    
    def __init__(self):
        # Inicializar componentes
        self.audio_manager = AudioManager()
        self.gesture_detector = GestureDetector()
        
        # Configurar MediaPipe
        self.mp_manos = mp.solutions.hands
        self.mp_dibujo = mp.solutions.drawing_utils
        self.manos = self.mp_manos.Hands(**MEDIAPIPE_CONFIG)
        
        # Configurar cámara
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CONFIG['width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CONFIG['height'])
        self.cap.set(cv2.CAP_PROP_FPS, CAMERA_CONFIG['fps'])
        
        # Estado
        self.ultimo_tiempo_gesto = {}
        self.tiempo_prev = 0
        self.corriendo = True
        
        # Configuración visual
        self.colores = VISUAL_CONFIG['colores']
        self.grosor = VISUAL_CONFIG['grosor']
        self.tamaños = VISUAL_CONFIG['tamaños']
    
    def procesar_mano(self, i_mano, lm_mano, frame, h, w, resultados):
        """Procesa una mano detectada"""
        
        # Dibujar landmarks
        self.mp_dibujo.draw_landmarks(
            frame,
            lm_mano,
            self.mp_manos.HAND_CONNECTIONS,
            self.mp_dibujo.DrawingSpec(
                color=self.colores['landmarks'],
                thickness=self.grosor['landmarks'],
                circle_radius=self.tamaños['circulo_landmark']
            ),
            self.mp_dibujo.DrawingSpec(
                color=self.colores['conexiones'],
                thickness=self.grosor['conexiones']
            )
        )
        

        