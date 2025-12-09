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
def distancia3(a, b):
    """
    Calcula la distancia Euclidiana 3D entre dos landmarks
    Args:
        a, b: Landmarks con atributos .x, .y, .z
    Returns:
        Float: Distancia 3D entre los puntos
    """
dx = a.x - b.x
dy = a.y - b.y
dz = a.z - b.z

return math.sqrt(dx*dx + dy*dy + dz*dz)

def angulo_entre_puntos(a, b, c):
    """
    Calcula el angulo en el punto b formado por los puntos a-b-c
    Args: 
        a, b, c: Puntos con atributos .x y .y
    Returns:
        float: Angulo en grados (0-180)
    Ejemplo:
        Para un dedo, a=mcp, b=pip, c=tip
        Retorna el angulo de flexion del dedo
    """
    # Vectores ba y bc
    ba = (a.x - b.x, a.y - b.y)
    bc = (c.x - b.x, c.y - b.y)

    # Producto punto
    dot_product = ba[0]*bc[0] + ba[1]*bc[1]

    #Magnitudes
    mag_ba = math.sqrt(ba[0]**2 + ba[1]**2)
    mag_bc = math.sqrt(bc[0]**2 + bc[1]**2)

    # Evitar division por cero
    if mag_ba * mag_bc == 0:
        return 0
    
    #Calcular coseno del angulo
    cos_angle = dot_product / (mag_ba * mag_bc)
    
    # Clamp para evitar errores de punto flotante
    cos_angle = max(-1, min(1, cos_angle))

    # Convertir a grados
    angle = math.acos(cos_angle)
    return math.degress(angle)


