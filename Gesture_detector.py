"""
gesture_detector.py
Modulo para deteccion de gestos de vocales en lenguaje de señas
"""

import mediapipe as mp
from config import DISTANCE_THRESHOLDS, ANGLE_THRESHOLDS, GESTURE_TOLERANCES, DETECTION_CONFIG
from geometryutils import (
    distancia3, angulo_entre_puntos, esta_doblado_mejorado, variacion_valores
)


class GestureDetector:
    """Clase para detectar gestos de vocales ASL"""

    def __init__(self):
        self.mp_manos = mp.solutions.hands
        self.gesto_buffer = {}
        self.frames_confirmacion = DETECTION_CONFIG['frames_confirmacion']

        #Cargar Umbrales
        self.th = DISTANCE_THRESHOLDS
        self.ang = ANGLE_THRESHOLDS
        self.tol = GESTURE_TOLERANCES

        def detectar_vocal(self, lm, mano_label =None):
            """
            Detecta qué vocal está siendo señalada
        
            Args:
            lm: Landmarks de la mano (lista de 21 puntos)
                mano_label: Etiqueta de la mano ('Left' o 'Right')
        
            Returns:
                str: Letra de la vocal ('A', 'E', 'I', 'O', 'U') o None
            """
            #Extraer todos los landmarks necesarios
            landmarks = self._extraer_landmarks(lm)

            #Calcular estado de los dedos
            estado_dedos = self._calcular_estado_dedos(landmarks)

            #Calcular distancias importantes
            distancias = self._calcular_distancias(landmarks)

            #Detectar cada vocal en orden de especificidad
            if self._es_vocal_a(estado_dedos, distancias):
                return 'A'
            
            if self._es_vocal_e(estado_dedos, distancias):
                return 'E'
        
            if self._es_vocal_i(estado_dedos, landmarks):
                return 'I'
        
            if self._es_vocal_o(estado_dedos, distancias, landmarks):
                return 'O'
        
            if self._es_vocal_u(estado_dedos, distancias, landmarks):
                return 'U'
            
            return None
        
        def _extraer_landmarks(self,lm):
             """Extrae y organiza todos los landmarks necesarios"""
        return {
            # Muñeca
            'muñeca': lm[self.mp_manos.HandLandmark.WRIST],
            
            # Pulgar
            'pulgar_mcp': lm[self.mp_manos.HandLandmark.THUMB_MCP],
            'pulgar_ip': lm[self.mp_manos.HandLandmark.THUMB_IP],
            'pulgar_tip': lm[self.mp_manos.HandLandmark.THUMB_TIP],
            
            # Índice
            'indice_mcp': lm[self.mp_manos.HandLandmark.INDEX_FINGER_MCP],
            'indice_pip': lm[self.mp_manos.HandLandmark.INDEX_FINGER_PIP],
            'indice_tip': lm[self.mp_manos.HandLandmark.INDEX_FINGER_TIP],
            
            # Medio
            'medio_mcp': lm[self.mp_manos.HandLandmark.MIDDLE_FINGER_MCP],
            'medio_pip': lm[self.mp_manos.HandLandmark.MIDDLE_FINGER_PIP],
            'medio_tip': lm[self.mp_manos.HandLandmark.MIDDLE_FINGER_TIP],
            
            # Anular
            'anular_mcp': lm[self.mp_manos.HandLandmark.RING_FINGER_MCP],
            'anular_pip': lm[self.mp_manos.HandLandmark.RING_FINGER_PIP],
            'anular_tip': lm[self.mp_manos.HandLandmark.RING_FINGER_TIP],
            
            # Meñique
            'meñique_mcp': lm[self.mp_manos.HandLandmark.PINKY_MCP],
            'meñique_pip': lm[self.mp_manos.HandLandmark.PINKY_PIP],
            'meñique_tip': lm[self.mp_manos.HandLandmark.PINKY_TIP],
        }