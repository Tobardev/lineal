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
            Detecta que vocal esta siendo señalada
        
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
            
            # indice
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
    
    def _calcular_estado_dedos(self, lm):
        """calcular si cada dedo esta doblado o ecxtendido"""
        return {
            'indice': {
                'doblado': esta_doblado_mejorado(lm['indice_tip'], lm['indice_pip'], lm['indice_mcp']),
                'angulo': angulo_entre_puntos(lm['indice_mcp'], lm['indice_pip'], lm['indice_tip'])
            },
            'medio': {
                'doblado': esta_doblado_mejorado(lm['medio_tip'], lm['medio_pip'], lm['medio_mcp']),
                'angulo': angulo_entre_puntos(lm['medio_mcp'], lm['medio_pip'], lm['medio_tip'])
            },
            'anular': {
                'doblado': esta_doblado_mejorado(lm['anular_tip'], lm['anular_pip'], lm['anular_mcp']),
                'angulo': angulo_entre_puntos(lm['anular_mcp'], lm['anular_pip'], lm['anular_tip'])
            },
            'meñique': {
                'doblado': esta_doblado_mejorado(lm['meñique_tip'], lm['meñique_pip'], lm['meñique_mcp']),
                'angulo': angulo_entre_puntos(lm['meñique_mcp'], lm['meñique_pip'], lm['meñique_tip'])
            }


        }
    
    def _calcular_distancias(self, lm):
        """Calcula distancias importantes entre puntos"""
        return {
            'pulgar_indice': distancia3(lm['pulgar_tip'], lm['indice_tip']),
            'indice_medio': distancia3(lm['indice_tip'], lm['medio_tip']),
            'medio_anular': distancia3(lm['medio_tip'], lm['anular_tip']),
            'anular_meñique': distancia3(lm['anular_tip'], lm['meñique_tip']),
            'pulgar_mcp': distancia3(lm['pulgar_tip'], lm['indice_mcp']),
        }
    
    def _es_vocal_a(self, estado, dist):
        """Detecta vocal A: puño cerrado con pulgar al costado"""
        todos_doblados = all(estado[d]['doblado'] for d in ['indice', 'medio', 'anular', 'meñique'])
        angulos_doblados = all(estado[d]['angulo'] < self.ang['doblado'] 
                              for d in ['indice', 'medio'])
        pulgar_separado = (dist['pulgar_mcp'] > self.th['medio'] and 
                          dist['pulgar_indice'] > self.th['cerca'])
        
        return todos_doblados and angulos_doblados and pulgar_separado
    
    def _es_vocal_e(self, estado, dist):
        """Detecta vocal E: dedos doblados tocando el pulgar"""
        todos_doblados = all(estado[d]['doblado'] for d in ['indice', 'medio', 'anular', 'meñique'])
        angulo_doblado = estado['indice']['angulo'] < self.ang['doblado']
        pulgar_cerca = dist['pulgar_indice'] < self.th['cerca']
        
        return todos_doblados and angulo_doblado and pulgar_cerca
    
    def _es_vocal_i(self, estado, lm):
        """Detecta vocal I: solo meñique extendido"""
        dedos_doblados = all(estado[d]['doblado'] for d in ['indice', 'medio', 'anular'])
        meñique_extendido = (not estado['meñique']['doblado'] and 
                            estado['meñique']['angulo'] > self.ang['extendido'])
        
        # Verificación adicional: meñique más alto que medio
        meñique_alto = lm['meñique_tip'].y < lm['medio_tip'].y
        
        return dedos_doblados and meñique_extendido and meñique_alto

    def _es_vocal_o(self, estado, dist, lm):
        """Detecta vocal O: dedos formando circulo"""
        # Promedio de distancias entre dedos adyacentes
        distancias_lista = [dist['pulgar_indice'], dist['indice_medio'], 
                           dist['medio_anular'], dist['anular_meñique']]
        promedio = sum(distancias_lista) / len(distancias_lista)
        
        todos_cercanos = promedio < self.th['medio']
        no_todos_doblados = not all(estado[d]['doblado'] 
                                    for d in ['indice', 'medio', 'anular', 'meñique'])
        
        # Verificar altura similar de las puntas
        alturas = [lm['indice_tip'].y, lm['medio_tip'].y, 
                  lm['anular_tip'].y, lm['meñique_tip'].y]
        variacion = variacion_valores(alturas)
        
        return todos_cercanos and no_todos_doblados and variacion < self.tol['O']['variacion_altura_max']
    
    def _es_vocal_u(self, estado, dist, lm):
        """Detecta vocal U: indice y medio extendidos juntos"""
        ind_med_extendidos = (not estado['indice']['doblado'] and 
                             not estado['medio']['doblado'] and
                             estado['indice']['angulo'] > self.ang['extendido'] and
                             estado['medio']['angulo'] > self.ang['extendido'])
        
        anu_meñ_doblados = estado['anular']['doblado'] and estado['meñique']['doblado']
        ind_med_juntos = dist['indice_medio'] < self.th['cerca']
        
        # Verificar altura similar
        diferencia_altura = abs(lm['indice_tip'].y - lm['medio_tip'].y)
        altura_similar = diferencia_altura < self.tol['U']['diferencia_altura_max']
        
        return ind_med_extendidos and anu_meñ_doblados and ind_med_juntos and altura_similar
    
    def confirmar_gesto(self, i_mano, gesto_actual):
        """
        Confirma un gesto solo si se detecta de forma estable
        
        Args:
            i_mano: indice de la mano
            gesto_actual: Gesto detectado actualmente
        
        Returns:
            str: Gesto confirmado o None
        """
        if i_mano not in self.gesto_buffer:
            self.gesto_buffer[i_mano] = []
        
        # Agregar al buffer
        self.gesto_buffer[i_mano].append(gesto_actual)
        
        # Mantener solo los ultimos N frames
        if len(self.gesto_buffer[i_mano]) > self.frames_confirmacion:
            self.gesto_buffer[i_mano].pop(0)
        
        # Confirmar si todos coinciden
        if len(self.gesto_buffer[i_mano]) == self.frames_confirmacion:
            if all(g == gesto_actual for g in self.gesto_buffer[i_mano]):
                return gesto_actual
        
        return None
    
    def limpiar_buffer(self, i_mano):
        """Limpia el buffer de confirmación de una mano"""
        if i_mano in self.gesto_buffer:
            self.gesto_buffer[i_mano] = []    