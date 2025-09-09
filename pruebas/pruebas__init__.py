# pruebas/__init__.py
from .prueba_medias import prueba_medias as prueba_medias_func
from .prueba_varianza import prueba_varianza as prueba_varianza_func
from .prueba_chi_cuadrado import prueba_chi_cuadrado as prueba_chi_cuadrado_func

# Crear alias con nombres diferentes
prueba_medias = prueba_medias_func
prueba_varianza = prueba_varianza_func  
prueba_chi_cuadrado = prueba_chi_cuadrado_func

__all__ = ['prueba_medias', 'prueba_varianza', 'prueba_chi_cuadrado']