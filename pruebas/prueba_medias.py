import math
from scipy.stats import norm

def prueba_medias(numeros, alpha=0.05):
    """
    Prueba de hipótesis para la media de números pseudoaleatorios
    """
    n = len(numeros)
    if n == 0:
        return None
        
    media_muestral = sum(numeros) / n
    
    # Estadístico Z
    z_calculado = (media_muestral - 0.5) * math.sqrt(12 * n)
    
    # Valores críticos
    z_alpha_2 = norm.ppf(1 - alpha/2)
    
    # Límites de aceptación
    li = 0.5 - z_alpha_2 * (1/math.sqrt(12*n))
    ls = 0.5 + z_alpha_2 * (1/math.sqrt(12*n))
    
    # Decisión
    acepta_H0 = li <= media_muestral <= ls
    
    return {
        'media_muestral': media_muestral,
        'z_calculado': z_calculado,
        'limite_inferior': li,
        'limite_superior': ls,
        'acepta_H0': acepta_H0,
        'alpha': alpha
    }