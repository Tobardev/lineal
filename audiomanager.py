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
        
       def reproducir(self, vocal):
        """
        Reproduce el sonido de la vocal especificada
        
        Args:
            vocal (str): Letra de la vocal ('A', 'E', 'I', 'O', 'U')
        """
        if not self.disponible:
            return
        
        sonido = self.sonidos.get(vocal)
        if sonido:
            sonido.stop()  # Detener si ya está reproduciéndose
            sonido.play()
        else:
            print(f"⚠ Sonido para '{vocal}' no disponible")
    
    def detener_todos(self):
        """Detiene todos los sonidos que se estén reproduciendo"""
        if not self.disponible:
            return
        
        pygame.mixer.stop()
    
    def esta_disponible(self):
        """Retorna si el sistema de audio está disponible"""
        return self.disponible
    
    def obtener_vocales_disponibles(self):
        """Retorna lista de vocales con sonido disponible"""
        return list(self.sonidos.keys())