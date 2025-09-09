from scipy.stats import chi2

def prueba_varianza(numeros, alpha=0.05):
    """
    Prueba de hipótesis para la varianza
    """
    n = len(numeros)
    if n < 2:
        return None
        
    media = sum(numeros) / n
    varianza_muestral = sum((x - media)**2 for x in numeros) / (n - 1)
    
    # Estadístico Chi-cuadrado
    chi2_calculado = (n - 1) * varianza_muestral * 12
    
    # Valores críticos
    chi2_li = chi2.ppf(alpha/2, n-1)
    chi2_ls = chi2.ppf(1 - alpha/2, n-1)
    
    # Límites para la varianza
    li_var = chi2_li / (12 * (n - 1))
    ls_var = chi2_ls / (12 * (n - 1))
    
    # Decisión
    acepta_H0 = li_var <= varianza_muestral <= ls_var
    
    return {
        'varianza_muestral': varianza_muestral,
        'varianza_teorica': 1/12,
        'chi2_calculado': chi2_calculado,
        'limite_inferior_var': li_var,
        'limite_superior_var': ls_var,
        'acepta_H0': acepta_H0,
        'alpha': alpha
    }