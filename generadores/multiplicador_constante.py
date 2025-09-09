def multiplicador_constante(semilla, constante, n):
    """
    Genera números pseudoaleatorios usando el método de multiplicador constante
    """
    numeros = []
    X_actual = semilla
    d = len(str(semilla))
    
    for i in range(n):
        # Multiplicar constante por valor actual
        Y = constante * X_actual
        
        # Convertir a string para extraer dígitos centrales
        str_Y = str(Y)
        
        # Asegurar longitud suficiente
        if len(str_Y) < 2 * d:
            str_Y = str_Y.zfill(2 * d)
        
        # Extraer D dígitos del centro
        start = (len(str_Y) - d) // 2
        X_siguiente = int(str_Y[start:start + d])
        
        # Calcular ri = 0.X_siguiente
        ri = X_siguiente / (10 ** d)
        
        numeros.append(ri)
        X_actual = X_siguiente
    
    return numeros