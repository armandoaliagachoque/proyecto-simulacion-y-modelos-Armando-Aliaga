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
from utils import exportador

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
            tk.Button(frame, text="Revelar Mensaje Oculto",
          bg=self.color_amarillo, fg=self.color_azul_oscuro,
          command=self.revelar_mensaje).grid(row=5, column=0, pady=10)

    
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
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()
        
def revelar_mensaje(self):
    """Revela el mensaje oculto en los números generados"""
    if not self.numeros_generados:
        messagebox.showwarning("Advertencia", "Primero genere oculte números")
        return
    
    # Indicas la longitud del mensaje que ocultaste
    longitud_mensaje = 7 
    
    mensaje_revelado = revelar_mensaje_de_numeros(self.numeros_generados, longitud_mensaje)
    
    messagebox.showinfo("Mensaje oculto", f"Mensaje oculto: {mensaje_revelado}")


def ocultar_mensaje_en_numeros(numeros, mensaje):
    """
    Oculta un mensaje de texto en el último dígito de los números pseudoaleatorios.
    """
    mensaje = mensaje.upper()
    # Solo letras A-Z → 0-25
    codigos = [(ord(c) - 65) % 10 for c in mensaje]  # modulo 10 para un dígito
    numeros_ocultos = []

    for i, num in enumerate(numeros):
        if i < len(codigos):
            # reemplazamos el último decimal por el código
            parte_entera = int(num)
            parte_decimal = float(f"0.{codigos[i]}")
            numeros_ocultos.append(parte_entera + parte_decimal)
        else:
            numeros_ocultos.append(num)
    return numeros_ocultos

        
# Para ejecutar directamente
if __name__ == "__main__":
    app = SimulacionApp()
    app.run()