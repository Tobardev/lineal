"""
audio_manager.py
Módulo para gestión de audio y reproducción de sonidos
"""

import pygame
from config import AUDIO_CONFIG


class AudioManager:
    """Clase para manejar la carga y reproducción de sonidos"""
    
    def __init__(self):
        self.disponible = False
        self.sonidos = {}
        self._inicializar()

         def _inicializar(self):
        """Inicializa pygame mixer y carga los sonidos"""
        try:
            pygame.mixer.init()
            self.disponible = True
            print("✓ pygame inicializado correctamente")
            self._cargar_sonidos()
        except Exception as e:
            print(f"✗ pygame no está disponible: {e}")
            print("  Para habilitar sonido: pip install pygame")
            self.disponible = False