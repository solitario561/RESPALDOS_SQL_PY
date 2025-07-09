"""
Script principal para ejecutar la aplicación de respaldos SQL.
"""

import sys
import os

# Agregar el directorio raíz al path para imports relativos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import tkinter as tk
    from src.main import BackupApp
    
    # Configurar la aplicación
    root = tk.Tk()
    app = BackupApp(root)
    
    # Ejecutar la aplicación
    root.mainloop()
