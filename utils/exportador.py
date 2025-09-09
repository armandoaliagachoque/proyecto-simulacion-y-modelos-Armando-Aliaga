import json
import csv
from datetime import datetime

def exportar_txt(numeros, filename):
    """Exporta números a archivo de texto"""
    with open(filename, 'w') as f:
        f.write(f"Números generados - {datetime.now()}\n")
        f.write("=" * 50 + "\n")
        for i, num in enumerate(numeros):
            f.write(f"r{i}: {num:.6f}\n")

def exportar_csv(numeros, filename):
    """Exporta números a CSV"""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Índice', 'Valor'])
        for i, num in enumerate(numeros):
            writer.writerow([i, num])

def exportar_resultados(resultados, filename):
    """Exporta resultados de pruebas a JSON"""
    with open(filename, 'w') as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)