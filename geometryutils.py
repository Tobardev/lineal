"""
geometryutils.py
Funciones de geometría y cálculos matemáticos para detección de gestos
Autor: Juan Camilo Quiceno - 2363251-2724
"""

import math


# ========================================
# FUNCIONES DE DISTANCIA
# ========================================

def distancia2(a, b):
    """
    Calcula la distancia Euclidiana 2D entre dos puntos normalizados
    
    Args:
        a, b: Puntos con atributos .x y .y
    
    Returns:
        float: Distancia 2D entre los puntos
    """
    return math.hypot(a.x - b.x, a.y - b.y)