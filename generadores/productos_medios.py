def productos_medios(semilla1, semilla2, n):
    """
    Genera números pseudoaleatorios usando el método de productos medios
    """
    numeros = []
    X_previo = semilla1
    X_actual = semilla2
    d = len(str(semilla1))
    
    for i in range(n):
        # Multiplicar los dos valores anteriores
        Y = X_previo * X_actual
        
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
        
        # Actualizar valores para siguiente iteración
        X_previo = X_actual
        X_actual = X_siguiente
    
    return numeros