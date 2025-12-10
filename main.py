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


        # Calcular bounding box
        x_min, y_min, x_max, y_max, cx, cy = calcular_bounding_box(lm_mano.landmark, w, h)
        
        # Dibujar bounding box y centro
        cv2.rectangle(frame, (x_min-10, y_min-10), (x_max+10, y_max+10),
                     self.colores['bbox'], self.grosor['bbox'])
        cv2.circle(frame, (cx, cy), self.tamaños['circulo_centro'],
                  self.colores['bbox'], -1)
        
        # Obtener etiqueta de mano
        etiqueta_mano = "Desconocida"
        if resultados.multi_handedness and len(resultados.multi_handedness) > i_mano:
            etiqueta_mano = resultados.multi_handedness[i_mano].classification[0].label
        
        # Detectar gesto
        gesto_detectado = self.gesture_detector.detectar_vocal(lm_mano.landmark, etiqueta_mano)
        
        # Confirmar gesto
        gesto_confirmado = self.gesture_detector.confirmar_gesto(i_mano, gesto_detectado)
        
        # Manejar reproducción de audio
        self._manejar_audio(i_mano, gesto_detectado, gesto_confirmado)
        
        # Dibujar información
        self._dibujar_info(frame, i_mano, etiqueta_mano, x_min, y_min, y_max,
                          gesto_detectado, gesto_confirmado)
    
    def _manejar_audio(self, i_mano, gesto_detectado, gesto_confirmado):
        """Maneja la lógica de reproducción de audio"""
        ahora = time.time()
        
        if i_mano in self.ultimo_tiempo_gesto:
            ultima_letra, ultimo_ts = self.ultimo_tiempo_gesto[i_mano]
        else:
            ultima_letra, ultimo_ts = None, 0
        
        # Solo reproducir si el gesto está confirmado
        if gesto_confirmado is not None:
            if ultima_letra != gesto_confirmado:
                self.audio_manager.reproducir(gesto_confirmado)
                self.ultimo_tiempo_gesto[i_mano] = (gesto_confirmado, ahora)
                print(f"Mano {i_mano}: Reproduciendo '{gesto_confirmado}'")
        else:
            if ultima_letra is not None and gesto_detectado is None:
                self.ultimo_tiempo_gesto[i_mano] = (None, ahora)
                self.gesture_detector.limpiar_buffer(i_mano)
    
    def _dibujar_info(self, frame, i_mano, etiqueta, x_min, y_min, y_max,
                     gesto_detectado, gesto_confirmado):
        """Dibuja información en pantalla"""
        
        # Etiqueta de mano
        cv2.putText(frame, f'#{i_mano+1} {etiqueta}', (x_min, y_min - 15),
                   cv2.FONT_HERSHEY_SIMPLEX, self.tamaños['fuente_info'],
                   self.colores['bbox'], self.grosor['texto_normal'])
        
        # Gesto detectado/confirmado
        if gesto_confirmado:
            cv2.putText(frame, f'Gesto: {gesto_confirmado}', (x_min, y_max + 25),
                       cv2.FONT_HERSHEY_SIMPLEX, self.tamaños['fuente_gesto'],
                       self.colores['texto_confirmado'], self.grosor['texto_gesto'])
        elif gesto_detectado:
            cv2.putText(frame, f'Detectando: {gesto_detectado}...', (x_min, y_max + 25),
                       cv2.FONT_HERSHEY_SIMPLEX, self.tamaños['fuente_detectando'],
                       self.colores['texto_detectando'], self.grosor['texto_normal'])
        else:
            cv2.putText(frame, 'Gesto: -', (x_min, y_max + 25),
                       cv2.FONT_HERSHEY_SIMPLEX, self.tamaños['fuente_detectando'],
                       self.colores['texto_sin_gesto'], self.grosor['texto_normal'])
 
    def _dibujar_fps(self, frame):
        """Calcula y dibuja FPS"""
        tiempo_actual = time.time()
        fps = 1 / (tiempo_actual - self.tiempo_prev) if self.tiempo_prev != 0 else 0
        self.tiempo_prev = tiempo_actual
        
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, self.tamaños['fuente_fps'],
                   self.colores['texto_confirmado'], self.grosor['texto_normal'])
       
        

        