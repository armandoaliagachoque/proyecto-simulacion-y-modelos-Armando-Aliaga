def cuadrados_medios(semilla, n):
    """
    Genera números pseudoaleatorios usando el método de cuadrados medios
    """
    numeros = []
    X_actual = semilla
    d = len(str(semilla))
    
    for i in range(n):
        # Elevar al cuadrado
        Y = X_actual ** 2
        
        # Convertir a string y extraer dígitos centrales
        str_Y = str(Y)
        
        # Padding para asegurar longitud suficiente
        if len(str_Y) < 2 * d:
            str_Y = str_Y.zfill(2 * d)
        
        # Extraer D dígitos del centro
        start = (len(str_Y) - d) // 2
        X_siguiente = int(str_Y[start:start + d])
        
        # Calcular ri
        ri = X_siguiente / (10 ** d)
        
        numeros.append(ri)
        X_actual = X_siguiente
    
    return numeros