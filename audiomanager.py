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