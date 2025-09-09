# Sistema de Simulación - Generadores Pseudoaleatorios
###ESTUDIANTE: ARMANDO ALIAGA CHOQUE
###MATERIA SIMULACION Y MODELOS
###DOCENTE: NEDDY CHOQUE
###GESTION: 2025-II

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![GUI](https://img.shields.io/badge/GUI-Tkinter-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

Sistema de simulación para generación y análisis de números pseudoaleatorios con interfaz gráfica moderna.

## CARACTERISTICAS

####  Generadores Implementados
- **Multiplicador Constante** - Algoritmo con semilla y constante
- **Productos Medios** - Generación basada en dos semillas  
- **Cuadrados Medios** - Método clásico de elevación al cuadrado

####  Pruebas Estadísticas
- **Prueba de Medias** - Verificación de media teórica (0.5)
- **Prueba de Varianza** - Validación de varianza teórica (1/12)
- **Prueba Chi-Cuadrado** - Test de uniformidad de distribución
## INSTALACION

#### Requisitos Previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

###Pasos de instalación
1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tuusuario/proyecto-simulacion.git
   cd proyecto-simulacion```

2. **Instalar dependencias **
```pip install -r requirements.txt```
3. **Ejecutar aplicacion **
```python main.py
o
python gui.py```
###Dependencias principales
numpy>=1.21.0
matplotlib>=3.5.0
scipy>=1.7.0
##CAPTURAS DE LA GUI
[![INTERFAZ PRINCIPAL](https://snipboard.io/MRNSzP.jpg "INTERFAZ PRINCIPAL")](https://snipboard.io/MRNSzP.jpg "INTERFAZ PRINCIPAL")
[![PRUEBAS](https://snipboard.io/to3BhU.jpg "PRUEBAS")](https://snipboard.io/to3BhU.jpg "PRUEBAS")
[![HISTOGRAMA](https://snipboard.io/fPesRI.jpg "HISTOGRAMA")](https://snipboard.io/fPesRI.jpg "HISTOGRAMA")
[![EXPORTACION](https://snipboard.io/ITokWD.jpg "EXPORTACION")](https://snipboard.io/ITokWD.jpg "EXPORTACION")
##Bitácora de Clases

###Clase 1 – 13 de agosto
- Configuración del entorno Python.

- Revisión de las librerías necesarias para el proyecto.

- Explicación de la estructura básica del proyecto.

- Implementación inicial de la GUI (Interfaz Gráfica de Usuario).

### Clase 2 – 20 de agosto
- Estudio del algoritmo de Multiplicador Constante.

- Implementación del algoritmo de Productos Medios.

- Implementación del algoritmo de Cuadrados Medios.

- Integración de los generadores dentro de la interfaz gráfica.

###Clase 3 – 27 de agosto
- Explicación e implementación de la Prueba de Medias.

- Explicación e implementación de la Prueba de Varianza.

- Explicación e implementación de la Prueba Chi-Cuadrado.

- Visualización de resultados mediante gráficas.

###Clase 4 – 3 de septiembre
- Creación de un sistema de exportación múltiple de resultados.

- Mejoras en la interfaz gráfica para mayor usabilidad.

- Elaboración de la documentación completa del proyecto.
