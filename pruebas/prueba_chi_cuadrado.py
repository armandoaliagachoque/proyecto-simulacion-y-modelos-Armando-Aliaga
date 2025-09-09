import math
from scipy.stats import chi2 as chi2_dist

def prueba_chi_cuadrado(numeros, alpha=0.05):
    """
    Prueba de Chi-cuadrado para uniformidad
    """
    n = len(numeros)
    if n == 0:
        return None
        
    m = max(5, int(math.sqrt(n)))  # Mínimo 5 intervalos
    
    # Crear intervalos
    intervalos = [(i/m, (i+1)/m) for i in range(m)]
    
    # Calcular frecuencias observadas
    frec_observadas = [0] * m
    for num in numeros:
        for i, (inicio, fin) in enumerate(intervalos):
            if inicio <= num < fin or (i == m-1 and num == 1.0):
                frec_observadas[i] += 1
                break
    
    # Frecuencias esperadas
    frec_esperadas = [n / m] * m
    
    # Estadístico Chi-cuadrado
    chi2_calculado = 0
    for i in range(m):
        if frec_esperadas[i] > 0:  # Evitar división por cero
            chi2_calculado += ((frec_observadas[i] - frec_esperadas[i])**2) / frec_esperadas[i]
    
    # Valor crítico
    chi2_critico = chi2_dist.ppf(1 - alpha, m - 1)
    
    # Decisión
    acepta_H0 = chi2_calculado <= chi2_critico
    
    return {
        'chi2_calculado': chi2_calculado,
        'chi2_critico': chi2_critico,
        'frecuencias_observadas': frec_observadas,
        'frecuencias_esperadas': frec_esperadas,
        'intervalos': intervalos,
        'acepta_H0': acepta_H0,
        'alpha': alpha,
        'num_intervalos': m
    }