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
            
    def _cargar_sonidos(self):
        """Carga los archivos de audio para cada vocal"""
        if not self.disponible:
            return
        
        archivos = AUDIO_CONFIG['archivos']
        
        for vocal, archivo in archivos.items():
            try:
                self.sonidos[vocal] = pygame.mixer.Sound(archivo)
                print(f"✓ Sonido '{vocal}' cargado: {archivo}")
            except Exception as e:
                print(f"✗ Error cargando sonido '{vocal}' ({archivo}): {e}")
        
        if not self.sonidos:
            print("✗ No se pudo cargar ningún sonido")
            self.disponible = False