import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Importar módulos
from generadores import multiplicador_constante, productos_medios, cuadrados_medios
from pruebas.prueba_medias import prueba_medias
from pruebas.prueba_varianza import prueba_varianza
from pruebas.prueba_chi_cuadrado import prueba_chi_cuadrado
from utils import distribuciones 
from utils import exportador
from utils.distribuciones import parametros_por_dist

class SimulacionApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Simulación - Generadores Pseudoaleatorios")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2C3E50')  # Azul oscuro
        
        # Variables de estado
        self.numeros_generados = []
        self.resultados_pruebas = {}
        
        # Configurar estilo
        self.configurar_estilos()
        
        # Crear interfaz
        self.crear_interfaz()
        
        self.crear_pestana_juego_vida()

        
    def configurar_estilos(self):
        """Configurar estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores principales
        self.color_amarillo = '#F39C12'
        self.color_azul_oscuro = '#2C3E50'
        self.color_azul_medio = '#3498DB'
        self.color_azul_claro = '#ECF0F1'
        self.color_blanco = '#FFFFFF'
        
        # Configurar estilos
        style.configure('TFrame', background=self.color_azul_claro)
        style.configure('TLabel', background=self.color_azul_claro, foreground=self.color_azul_oscuro)
        style.configure('TButton', background=self.color_amarillo, foreground=self.color_azul_oscuro)
        style.configure('TNotebook', background=self.color_azul_oscuro)
        style.configure('TNotebook.Tab', background=self.color_azul_medio, foreground=self.color_blanco)
        
    def crear_interfaz(self):
        """Crear la interfaz gráfica principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        title_label = tk.Label(main_frame, 
                              text="SISTEMA DE SIMULACIÓN - GENERADORES PSEUDOALEATORIOS",
                              font=('Arial', 16, 'bold'),
                              bg=self.color_azul_oscuro,
                              fg=self.color_amarillo,
                              pady=10)
        title_label.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky='nsew')
        
        # Crear pestañas
        self.crear_pestana_generadores()
        self.crear_pestana_pruebas()
        self.crear_pestana_distribuciones()
        self.crear_pestana_visualizacion()
        self.crear_pestana_exportacion()
        
        # Barra de estado
        self.status_bar = tk.Label(self.root, text="Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=2, column=0, sticky='ew')
        
    def crear_pestana_generadores(self):
        """Crear pestaña de generadores"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Generadores")
        
        # Configurar grid
        for i in range(4):
            frame.columnconfigure(i, weight=1)
        for i in range(10):
            frame.rowconfigure(i, weight=1)
        
        # Título
        title = tk.Label(frame, text="GENERADORES DE NÚMEROS PSEUDOALEATORIOS", 
                        font=('Arial', 12, 'bold'),
                        bg=self.color_azul_claro,
                        fg=self.color_azul_oscuro)
        title.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Selección de método
        tk.Label(frame, text="Método:", bg=self.color_azul_claro).grid(row=1, column=0, sticky='w', padx=5)
        self.metodo_var = tk.StringVar(value="multiplicador_constante")
        metodos = [
            ("Multiplicador Constante", "multiplicador_constante"),
            ("Productos Medios", "productos_medios"),
            ("Cuadrados Medios", "cuadrados_medios")
        ]
        
        for i, (text, value) in enumerate(metodos):
            rb = tk.Radiobutton(frame, text=text, variable=self.metodo_var, 
                               value=value, bg=self.color_azul_claro,
                               command=self.actualizar_campos)
            rb.grid(row=2+i, column=0, sticky='w', padx=20, pady=2)
        
        # Campos de entrada comunes
        tk.Label(frame, text="Cantidad (n):", bg=self.color_azul_claro).grid(row=1, column=1, sticky='w', padx=5)
        self.n_entry = tk.Entry(frame, width=15)
        self.n_entry.grid(row=1, column=2, sticky='w', padx=5)
        self.n_entry.insert(0, "100")
        
        # Campos específicos por método
        self.crear_campos_especificos(frame)
        
        # Botón de generación
        gen_btn = tk.Button(frame, text="Generar Números", 
                           bg=self.color_amarillo, fg=self.color_azul_oscuro,
                           font=('Arial', 10, 'bold'),
                           command=self.generar_numeros)
        gen_btn.grid(row=6, column=0, columnspan=4, pady=20)
              # Área para mostrar números generados
        tk.Label(frame, text="Números Generados:", bg=self.color_azul_claro,
                 font=('Arial', 10, 'bold')).grid(row=7, column=0, columnspan=4, sticky='w')

        self.numeros_text = tk.Text(frame, height=10, width=80, bg=self.color_blanco)
        self.numeros_text.grid(row=8, column=0, columnspan=4, sticky='nsew')

        # Scrollbar
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.numeros_text.yview)
        scrollbar.grid(row=8, column=4, sticky='ns')
        self.numeros_text.configure(yscrollcommand=scrollbar.set)
        
      
        
    def crear_campos_especificos(self, frame):
        """Crear campos específicos para cada método"""
        # Frame para campos específicos
        self.campos_especificos = ttk.Frame(frame)
        self.campos_especificos.grid(row=5, column=0, columnspan=4, sticky='ew', pady=10)
        self.campos_especificos.columnconfigure(1, weight=1)
        
        # Inicializar variables
        self.semilla_entry = None
        self.constante_entry = None
        self.semilla1_entry = None
        self.semilla2_entry = None
        
        self.actualizar_campos()
        
    def actualizar_campos(self):
        """Actualizar campos según el método seleccionado"""
        # Limpiar frame
        for widget in self.campos_especificos.winfo_children():
            widget.destroy()
        
        metodo = self.metodo_var.get()
        
        if metodo == "multiplicador_constante":
            tk.Label(self.campos_especificos, text="Semilla (X0):", bg=self.color_azul_claro).grid(row=0, column=0, sticky='w', padx=5)
            self.semilla_entry = tk.Entry(self.campos_especificos, width=15)
            self.semilla_entry.grid(row=0, column=1, sticky='w', padx=5)
            self.semilla_entry.insert(0, "9803")
            
            tk.Label(self.campos_especificos, text="Constante (α):", bg=self.color_azul_claro).grid(row=1, column=0, sticky='w', padx=5)
            self.constante_entry = tk.Entry(self.campos_especificos, width=15)
            self.constante_entry.grid(row=1, column=1, sticky='w', padx=5)
            self.constante_entry.insert(0, "6965")
            
        elif metodo == "productos_medios":
            tk.Label(self.campos_especificos, text="Semilla 1 (X0):", bg=self.color_azul_claro).grid(row=0, column=0, sticky='w', padx=5)
            self.semilla1_entry = tk.Entry(self.campos_especificos, width=15)
            self.semilla1_entry.grid(row=0, column=1, sticky='w', padx=5)
            self.semilla1_entry.insert(0, "5015")
            
            tk.Label(self.campos_especificos, text="Semilla 2 (X1):", bg=self.color_azul_claro).grid(row=1, column=0, sticky='w', padx=5)
            self.semilla2_entry = tk.Entry(self.campos_especificos, width=15)
            self.semilla2_entry.grid(row=1, column=1, sticky='w', padx=5)
            self.semilla2_entry.insert(0, "5734")
            
        elif metodo == "cuadrados_medios":
            tk.Label(self.campos_especificos, text="Semilla (X0):", bg=self.color_azul_claro).grid(row=0, column=0, sticky='w', padx=5)
            self.semilla_entry = tk.Entry(self.campos_especificos, width=15)
            self.semilla_entry.grid(row=0, column=1, sticky='w', padx=5)
            self.semilla_entry.insert(0, "1234")
    
    def crear_pestana_pruebas(self):
        """Crear pestaña de pruebas estadísticas"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Pruebas Estadísticas")
        
        # Configurar grid
        for i in range(3):
            frame.columnconfigure(i, weight=1)
        
        # Título
        title = tk.Label(frame, text="PRUEBAS ESTADÍSTICAS", 
                        font=('Arial', 12, 'bold'),
                        bg=self.color_azul_claro,
                        fg=self.color_azul_oscuro)
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Nivel de significancia
        tk.Label(frame, text="Nivel de significancia (α):", bg=self.color_azul_claro).grid(row=1, column=0, sticky='w')
        self.alpha_entry = tk.Entry(frame, width=10)
        self.alpha_entry.grid(row=1, column=1, sticky='w')
        self.alpha_entry.insert(0, "0.05")
        
        # Botones de pruebas
        pruebas = [
            ("Prueba de Medias", self.ejecutar_prueba_medias),
            ("Prueba de Varianza", self.ejecutar_prueba_varianza),
            ("Prueba Chi-Cuadrado", self.ejecutar_prueba_chi)
        ]
        
        for i, (text, command) in enumerate(pruebas):
            btn = tk.Button(frame, text=text, bg=self.color_azul_medio, fg=self.color_blanco,
                           command=command, width=20)
            btn.grid(row=2+i, column=0, columnspan=3, pady=5)
        
        # Área de resultados
        tk.Label(frame, text="Resultados:", bg=self.color_azul_claro, 
                font=('Arial', 10, 'bold')).grid(row=5, column=0, sticky='w', pady=(20, 5))
        
        self.resultados_text = tk.Text(frame, height=15, width=70, bg=self.color_blanco)
        self.resultados_text.grid(row=6, column=0, columnspan=3, sticky='nsew')
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.resultados_text.yview)
        scrollbar.grid(row=6, column=3, sticky='ns')
        self.resultados_text.configure(yscrollcommand=scrollbar.set)
    
    def crear_pestana_visualizacion(self):
        """Crear pestaña de visualización"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Visualización")
        
        # Configurar grid
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        
        # Título
        title = tk.Label(frame, text="VISUALIZACIÓN DE RESULTADOS", 
                        font=('Arial', 12, 'bold'),
                        bg=self.color_azul_claro,
                        fg=self.color_azul_oscuro)
        title.grid(row=0, column=0, pady=(0, 20))
        
        # Frame para gráficos
        graph_frame = ttk.Frame(frame)
        graph_frame.grid(row=1, column=0, sticky='nsew')
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(0, weight=1)
        
        # Figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        # Botones de visualización
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, pady=10)
        
        tk.Button(btn_frame, text="Mostrar Histograma", bg=self.color_amarillo,
                 command=self.mostrar_histograma).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Mostrar Tabla de Frecuencias",
                  bg=self.color_amarillo, fg=self.color_azul_oscuro,
                  command=self.mostrar_tabla_frecuencias).grid(row=8, column=0, columnspan=4, pady=10)

        tk.Button(btn_frame, text="Mostrar Secuencia", bg=self.color_azul_medio, fg=self.color_blanco,
                 command=self.mostrar_secuencia).pack(side=tk.LEFT, padx=5)
    
    def crear_pestana_exportacion(self):
        """Crear pestaña de exportación"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Exportación")
        
        # Título
        title = tk.Label(frame, text="EXPORTACIÓN DE DATOS", 
                        font=('Arial', 12, 'bold'),
                        bg=self.color_azul_claro,
                        fg=self.color_azul_oscuro)
        title.grid(row=0, column=0, pady=(0, 20))
        
        # Botones de exportación
        export_buttons = [
            ("Exportar Números (TXT)", self.exportar_numeros_txt),
            ("Exportar Números (CSV)", self.exportar_numeros_csv),
            ("Exportar Resultados (JSON)", self.exportar_resultados_json)
        ]
        
        for i, (text, command) in enumerate(export_buttons):
            btn = tk.Button(frame, text=text, bg=self.color_azul_medio, fg=self.color_blanco,
                           command=command, width=25)
            btn.grid(row=1+i, column=0, pady=10)
    
    def generar_numeros(self):
        """Generar números pseudoaleatorios"""
        try:
            n = int(self.n_entry.get())
            metodo = self.metodo_var.get()
            
            if metodo == "multiplicador_constante":
                semilla = int(self.semilla_entry.get())
                constante = int(self.constante_entry.get())
                self.numeros_generados = multiplicador_constante(semilla, constante, n)
                
            elif metodo == "productos_medios":
                semilla1 = int(self.semilla1_entry.get())
                semilla2 = int(self.semilla2_entry.get())
                self.numeros_generados = productos_medios(semilla1, semilla2, n)
                
            elif metodo == "cuadrados_medios":
                semilla = int(self.semilla_entry.get())
                self.numeros_generados = cuadrados_medios(semilla, n)
            
            self.status_bar.config(text=f"Generados {n} números usando {metodo}")
                        # Mostrar los números en el área de texto
            self.numeros_text.delete(1.0, tk.END)  # limpiar antes
            for i, num in enumerate(self.numeros_generados, 1):
                self.numeros_text.insert(tk.END, f"{i}: {num}\n")

            messagebox.showinfo("Éxito", f"Se generaron {n} números pseudoaleatorios")
            
            
        except ValueError as e:
            messagebox.showerror("Error", "Por favor ingrese valores válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar números: {str(e)}")
    
    def ejecutar_prueba_medias(self):
        """Ejecutar prueba de medias"""
        if not self.numeros_generados:
            messagebox.showwarning("Advertencia", "Primero genere números aleatorios")
            return
        
        try:
            alpha = float(self.alpha_entry.get())
            resultados = prueba_medias(self.numeros_generados, alpha)
            self.resultados_pruebas["Prueba de Medias"] = resultados
            self.mostrar_resultados("PRUEBA DE MEDIAS", resultados)
        except Exception as e:
            messagebox.showerror("Error", f"Error en prueba de medias: {str(e)}")
    
    def ejecutar_prueba_varianza(self):
        """Ejecutar prueba de varianza"""
        if not self.numeros_generados:
            messagebox.showwarning("Advertencia", "Primero genere números aleatorios")
            return
        
        try:
            alpha = float(self.alpha_entry.get())
            resultados = prueba_varianza(self.numeros_generados, alpha)
            self.resultados_pruebas["Prueba de Varianza"] = resultados
            self.mostrar_resultados("PRUEBA DE VARIANZA", resultados)
        except Exception as e:
            messagebox.showerror("Error", f"Error en prueba de varianza: {str(e)}")
    
    def ejecutar_prueba_chi(self):
        """Ejecutar prueba chi-cuadrado"""
        if not self.numeros_generados:
            messagebox.showwarning("Advertencia", "Primero genere números aleatorios")
            return
        
        try:
            alpha = float(self.alpha_entry.get())
            resultados = prueba_chi_cuadrado(self.numeros_generados, alpha)
            self.resultados_pruebas["Prueba Chi-Cuadrado"] = resultados
            self.mostrar_resultados("PRUEBA CHI-CUADRADO", resultados)
        except Exception as e:
            messagebox.showerror("Error", f"Error en prueba chi-cuadrado: {str(e)}")
    
    def mostrar_resultados(self, titulo, resultados):
        """Mostrar resultados en el área de texto"""
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.insert(tk.END, f"=== {titulo} ===\n\n")
        
        for key, value in resultados.items():
            if isinstance(value, float):
                self.resultados_text.insert(tk.END, f"{key}: {value:.6f}\n")
            else:
                self.resultados_text.insert(tk.END, f"{key}: {value}\n")
        
        # Resaltar decisión
        self.resultados_text.insert(tk.END, "\n" + "="*50 + "\n")
        if resultados.get('acepta_H0', False):
            self.resultados_text.insert(tk.END, "✓ SE ACEPTA H0 - Los números son uniformes\n", 'aceptado')
        else:
            self.resultados_text.insert(tk.END, "✗ SE RECHAZA H0 - Los números no son uniformes\n", 'rechazado')
        
        # Configurar tags para colores
        self.resultados_text.tag_config('aceptado', foreground='green')
        self.resultados_text.tag_config('rechazado', foreground='red')
    
    def mostrar_histograma(self):
        """Mostrar histograma de los números generados"""
        if not self.numeros_generados:
            messagebox.showwarning("Advertencia", "Primero genere números aleatorios")
            return
        
        self.ax.clear()
        self.ax.hist(self.numeros_generados, bins=20, alpha=0.7, color=self.color_azul_medio, edgecolor='black')
        self.ax.set_xlabel('Valor')
        self.ax.set_ylabel('Frecuencia')
        self.ax.set_title('Histograma de Números Pseudoaleatorios')
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
    
    def mostrar_secuencia(self):
        """Mostrar secuencia de números generados"""
        if not self.numeros_generados:
            messagebox.showwarning("Advertencia", "Primero genere números aleatorios")
            return
        
        self.ax.clear()
        self.ax.plot(self.numeros_generados, 'o-', color=self.color_amarillo, alpha=0.7, markersize=3)
        self.ax.set_xlabel('Índice')
        self.ax.set_ylabel('Valor')
        self.ax.set_title('Secuencia de Números Pseudoaleatorios')
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
    
    def exportar_numeros_txt(self):
        """Exportar números a archivo TXT"""
        if not self.numeros_generados:
            messagebox.showwarning("Advertencia", "No hay números para exportar")
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            exportador.exportar_txt(self.numeros_generados, filename)
            messagebox.showinfo("Éxito", "Números exportados correctamente")
    
    def exportar_numeros_csv(self):
        """Exportar números a archivo CSV"""
        if not self.numeros_generados:
            messagebox.showwarning("Advertencia", "No hay números para exportar")
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            exportador.exportar_csv(self.numeros_generados, filename)
            messagebox.showinfo("Éxito", "Números exportados correctamente")
    
    def exportar_resultados_json(self):
        """Exportar resultados a JSON"""
        if not self.resultados_pruebas:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            exportador.exportar_resultados(self.resultados_pruebas, filename)
            messagebox.showinfo("Éxito", "Resultados exportados correctamente")
    def crear_pestana_distribuciones(self):
        """Crear pestaña de distribuciones y variables"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Distribuciones y Variables")

        # Configurar grid
        for i in range(4):
            frame.columnconfigure(i, weight=1)
        for i in range(10):
            frame.rowconfigure(i, weight=1)

        # Título
        title = tk.Label(frame, text="GENERACIÓN DE VARIABLES ALEATORIAS",
                         font=('Arial', 12, 'bold'),
                         bg=self.color_azul_claro,
                         fg=self.color_azul_oscuro)
        title.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        # Tipo de distribución (Continua o Discreta)
        tk.Label(frame, text="Tipo de Distribución:", bg=self.color_azul_claro).grid(row=1, column=0, sticky='w', padx=5)
        self.tipo_dist_var = tk.StringVar(value="Continua")
        ttk.Combobox(frame, textvariable=self.tipo_dist_var,
                     values=["Continua", "Discreta"], width=15).grid(row=1, column=1, sticky='w', padx=5)

        # Selector de distribución
        tk.Label(frame, text="Distribución:", bg=self.color_azul_claro).grid(row=2, column=0, sticky='w', padx=5)
        self.dist_var = tk.StringVar(value="uniforme_continua")
        self.combo_distribucion = ttk.Combobox(
            frame, textvariable=self.dist_var,
            values=[
                "uniforme_continua", "exponencial", "normal_box_muller", "gamma", "weibull",
                "uniforme_discreta", "bernoulli", "binomial", "poisson", "geometrica"
            ],
            width=20
        )
        self.combo_distribucion.grid(row=2, column=1, sticky='w', padx=5)
        self.combo_distribucion.bind("<<ComboboxSelected>>", lambda e: self.actualizar_parametros_distribucion(frame))

        # Parámetros dinámicos
        self.parametros_frame = ttk.Frame(frame)
        self.parametros_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky='ew')
        self.parametros_entradas = {}
        self.actualizar_parametros_distribucion(frame)

        # Botón para generar
        gen_btn = tk.Button(frame, text="Generar Distribución",
                            bg=self.color_amarillo, fg=self.color_azul_oscuro,
                            font=('Arial', 10, 'bold'),
                            command=self.generar_distribucion)
        gen_btn.grid(row=4, column=0, columnspan=4, pady=15)

        # Área de texto para mostrar resultados
        tk.Label(frame, text="Resultados de la Distribución:", bg=self.color_azul_claro,
                 font=('Arial', 10, 'bold')).grid(row=5, column=0, columnspan=4, sticky='w')

        self.resultados_dist_text = tk.Text(frame, height=10, width=80, bg=self.color_blanco)
        self.resultados_dist_text.grid(row=6, column=0, columnspan=4, sticky='nsew')

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.resultados_dist_text.yview)
        scrollbar.grid(row=6, column=4, sticky='ns')
        self.resultados_dist_text.configure(yscrollcommand=scrollbar.set)

        # Botón de histograma
        tk.Button(frame, text="Mostrar Histograma",
                  bg=self.color_azul_medio, fg=self.color_blanco,
                  command=self.mostrar_histograma_distribucion).grid(row=7, column=0, columnspan=4, pady=10)


    def actualizar_parametros_distribucion(self, parent_frame):
        """Actualizar campos de parámetros según la distribución seleccionada"""
        for widget in self.parametros_frame.winfo_children():
            widget.destroy()
        self.parametros_entradas.clear()

        dist = self.dist_var.get()

          # Usar el diccionario importado desde utils.distribuciones
        parametros = parametros_por_dist.get(dist, [])

        parametros = parametros_por_dist.get(dist, [])
        for i, param in enumerate(parametros):
            tk.Label(self.parametros_frame, text=f"{param}:", bg=self.color_azul_claro).grid(row=i, column=0, sticky='w', padx=5)
            entry = tk.Entry(self.parametros_frame, width=10)
            entry.grid(row=i, column=1, sticky='w', padx=5)
            self.parametros_entradas[param] = entry


    def generar_distribucion(self):
        """Generar variables aleatorias según la distribución elegida"""
        if not self.numeros_generados:
            messagebox.showwarning("Advertencia", "Primero genere números pseudoaleatorios en la pestaña Generadores")
            return

        dist_name = self.dist_var.get()
        n = len(self.numeros_generados)
        params = {k: float(v.get()) if v.get() else 0 for k, v in self.parametros_entradas.items()}
        if "n_trials" in params:
           params["n_trials"] = int(params["n_trials"])
        try:
            funcion = getattr(distribuciones, dist_name)
            valores = funcion(**params, n=n, numeros_uniformes=self.numeros_generados)
            self.valores_distribucion = valores

            # Mostrar los resultados
            self.resultados_dist_text.delete(1.0, tk.END)
            for i, val in enumerate(valores[:50], 1):
                self.resultados_dist_text.insert(tk.END, f"{i}: {val:.5f}\n")

            messagebox.showinfo("Éxito", f"Se generaron {n} valores con la distribución {dist_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar distribución: {str(e)}")


    def mostrar_histograma_distribucion(self):
        """Mostrar histograma de la distribución generada"""
        if not hasattr(self, 'valores_distribucion') or not self.valores_distribucion:
            messagebox.showwarning("Advertencia", "No hay datos de distribución generados")
            return

        self.ax.clear()
        self.ax.hist(self.valores_distribucion, bins=20, alpha=0.7, color=self.color_azul_medio, edgecolor='black')
        self.ax.set_xlabel('Valor')
        self.ax.set_ylabel('Frecuencia')
        self.ax.set_title(f'Histograma - {self.dist_var.get()}')
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
    def mostrar_tabla_frecuencias(self):
        """Mostrar tabla de frecuencias de la distribución generada"""
        if not hasattr(self, 'valores_distribucion') or not self.valores_distribucion:
            messagebox.showwarning("Advertencia", "No hay datos de distribución generados")
            return

        # Crear nueva ventana emergente
        ventana = tk.Toplevel(self.root)
        ventana.title("Tabla de Frecuencias")
        ventana.geometry("700x500")
        ventana.configure(bg=self.color_azul_claro)

        # Calcular frecuencias
        datos = np.array(self.valores_distribucion)
        n = len(datos)
        num_intervalos = 10  # número fijo de clases
        minimo, maximo = np.min(datos), np.max(datos)
        amplitud = (maximo - minimo) / num_intervalos
        limites = [minimo + i * amplitud for i in range(num_intervalos + 1)]

        frecuencias = np.histogram(datos, bins=limites)[0]
        rel_frec = frecuencias / n
        acum_frec = np.cumsum(rel_frec)

        # Frame principal
        frame_tabla = ttk.Frame(ventana, padding=10)
        frame_tabla.pack(fill='both', expand=True)

        # Etiqueta título
        tk.Label(frame_tabla, text="TABLA DE FRECUENCIAS", 
                 font=('Arial', 14, 'bold'),
                 bg=self.color_azul_oscuro, fg=self.color_amarillo,
                 pady=5).pack(fill='x', pady=(0,10))

        # Crear tabla con Treeview
        columnas = ("intervalo", "frec_abs", "frec_rel", "frec_acum")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=15)
        tabla.pack(fill='both', expand=True)

        # Encabezados
        tabla.heading("intervalo", text="Intervalo")
        tabla.heading("frec_abs", text="Frec. Absoluta")
        tabla.heading("frec_rel", text="Frec. Relativa")
        tabla.heading("frec_acum", text="Frec. Acumulada")

        # Anchos
        tabla.column("intervalo", anchor="center", width=180)
        tabla.column("frec_abs", anchor="center", width=120)
        tabla.column("frec_rel", anchor="center", width=120)
        tabla.column("frec_acum", anchor="center", width=120)

        # Insertar filas
        for i in range(num_intervalos):
            intervalo = f"[{limites[i]:.2f}, {limites[i+1]:.2f})"
            tabla.insert("", "end", values=(
                intervalo,
                f"{frecuencias[i]}",
                f"{rel_frec[i]:.4f}",
                f"{acum_frec[i]:.4f}"
            ))

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(frame_tabla, orient='vertical', command=tabla.yview)
        tabla.configure(yscroll=scrollbar_y.set)
        scrollbar_y.pack(side='right', fill='y')

        # Botón cerrar
        tk.Button(ventana, text="Cerrar", bg=self.color_amarillo, fg=self.color_azul_oscuro,
                  command=ventana.destroy, font=('Arial', 10, 'bold')).pack(pady=10)


    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()
        
    def crear_pestana_juego_vida(self):
        """Crear pestaña del Juego de la Vida"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Juego de la Vida")

        # Título
        title = tk.Label(frame, text="SIMULACIÓN - JUEGO DE LA VIDA (Conway)",
                         font=('Arial', 14, 'bold'),
                         bg=self.color_azul_claro, fg=self.color_azul_oscuro)
        title.pack(pady=10)

        # Variables de control
        self.grid_size = 30
        self.running = False

        # Crear el tablero inicial aleatorio
        self.board = np.random.choice([0, 1], size=(self.grid_size, self.grid_size))

        # Crear figura de Matplotlib
        self.fig_vida, self.ax_vida = plt.subplots(figsize=(6, 6))
        self.canvas_vida = FigureCanvasTkAgg(self.fig_vida, master=frame)
        self.canvas_vida.get_tk_widget().pack(pady=10)
        self.im = self.ax_vida.imshow(self.board, cmap="Blues")
        self.ax_vida.set_title("Estado actual de la simulación")
        self.ax_vida.axis("off")

        # Botones de control
        control_frame = ttk.Frame(frame)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Iniciar", bg=self.color_amarillo, fg=self.color_azul_oscuro,
                  command=self.iniciar_juego_vida, width=12).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Pausar", bg=self.color_azul_medio, fg=self.color_blanco,
                  command=self.pausar_juego_vida, width=12).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Reiniciar", bg=self.color_amarillo, fg=self.color_azul_oscuro,
                  command=self.reiniciar_juego_vida, width=12).grid(row=0, column=2, padx=5)

    def actualizar_tablero(self):
        """Actualizar tablero según las reglas del Juego de la Vida"""
        new_board = np.copy(self.board)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Contar vecinos vivos
                vecinos = np.sum(self.board[max(0, i-1):min(self.grid_size, i+2),
                                            max(0, j-1):min(self.grid_size, j+2)]) - self.board[i, j]

                # Aplicar reglas
                if self.board[i, j] == 1 and (vecinos < 2 or vecinos > 3):
                    new_board[i, j] = 0  # Muerte
                elif self.board[i, j] == 0 and vecinos == 3:
                    new_board[i, j] = 1  # Nacimiento
        self.board = new_board

    def ejecutar_paso(self):
        """Ejecutar un paso de simulación"""
        if self.running:
            self.actualizar_tablero()
            self.im.set_data(self.board)
            self.canvas_vida.draw()
            self.root.after(200, self.ejecutar_paso)

    def iniciar_juego_vida(self):
        """Iniciar simulación"""
        if not self.running:
            self.running = True
            self.ejecutar_paso()

    def pausar_juego_vida(self):
        """Pausar simulación"""
        self.running = False

    def reiniciar_juego_vida(self):
        """Reiniciar tablero aleatoriamente"""
        self.running = False
        self.board = np.random.choice([0, 1], size=(self.grid_size, self.grid_size))
        self.im.set_data(self.board)
        self.canvas_vida.draw()




        
# Para ejecutar directamente
if __name__ == "__main__":
    app = SimulacionApp()
    app.run()
