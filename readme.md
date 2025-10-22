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
## Bitácora de Desarrollo

A continuación, se detalla el registro de las actividades clave realizadas en las últimas sesiones del proyecto:

### Clase 5 – 10 de septiembre
* **Generadores Pseudoaleatorios:** Revisión y optimización de los métodos de generación previamente implementados.
* **Nuevos Métodos:** Incorporación de los generadores **congruencial mixto** y **congruencial lineal**.
* **Interfaz de Parámetros:** Ajuste de la GUI para permitir el ingreso de parámetros específicos (semilla, módulo, constante, etc.) para cada generador.
* **Validación:** Implementación de validación de datos en los campos de entrada del formulario para asegurar la integridad de los parámetros.

### Clase 6 – 17 de septiembre
* **Formulario Principal:** Desarrollo del módulo principal dedicado a la configuración de las **pruebas estadísticas**.
* **Parámetros Dinámicos:** Creación de campos dinámicos para ingresar valores como *n* (cantidad de datos), *k* (intervalos) y **nivel de significancia** ($\alpha$).
* **Controles:** Adición de botones funcionales claves: **Generar**, **Probar** y **Exportar**.
* **Visualización:** Implementación de la presentación de resultados numéricos de las pruebas en la interfaz.

### Clase 7 – 24 de septiembre
* **Mejora de la GUI:** Optimización del diseño mediante la segmentación de la interfaz en pestañas (**Generadores**, **Pruebas** y **Variables**).
* **Gráficos:** Implementación de la visualización gráfica automática, incluyendo **histogramas** y **tablas de frecuencias**.
* **Exportación:** Integración del sistema para exportar los resultados generados en formatos **CSV** y **Excel**.
* **Pruebas:** Verificación de la funcionalidad completa y estabilidad del formulario principal.

### Clase 8 – 8 de octubre
* **Simulación Visual:** Introducción al **"Juego de la Vida"** de Conway como módulo de simulación complementario.
* **Estructura del Tablero:** Creación de la matriz base para representar el estado de las celdas (vivas/muertas).
* **Lógica de Evolución:** Programación de la lógica de evolución de las generaciones conforme a las reglas del juego.
* **Renderizado:** Uso de librerías como `tkinter.Canvas` o `matplotlib` para la representación gráfica del tablero.

### Clase 9 – 15 de octubre
* **Integración:** Inclusión del módulo del **Juego de la Vida** dentro de la interfaz principal del proyecto.
* **Controles Interactivos:** Adición de funcionalidades de control (iniciar, pausar, reiniciar y ajuste de tamaño del tablero).
* **Optimización:** Refinamiento del algoritmo para mejorar el rendimiento de la simulación en tiempo real.
* **Cierre de Módulos:** Revisión general del código fuente y pruebas finales de funcionamiento en entorno *offline*.

### Clase 10 – 22 de octubre
* **Sincronización:** Configuración y ejecución de la sincronización del proyecto con el repositorio remoto de **GitHub**.
* **Documentación:** Actualización exhaustiva del archivo **README.md** para reflejar los últimos cambios y funcionalidades implementadas en el proyecto.
