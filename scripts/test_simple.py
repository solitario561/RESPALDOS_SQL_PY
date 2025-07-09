#!/usr/bin/env python3
"""
Prueba simplificada de la aplicación sin threading.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Función principal simplificada."""
    print("INICIANDO APLICACIÓN CORREGIDA...")
    print("=" * 50)
    
    try:
        import tkinter as tk
        from src.main import BackupApp
        
        print("✓ Imports exitosos")
        
        # Crear y configurar la ventana
        root = tk.Tk()
        print("✓ Ventana root creada")
        
        print("🔧 Creando BackupApp...")
        app = BackupApp(root)
        print("✓ BackupApp creada exitosamente")
        
        # Programar auto-cierre para evitar colgado
        def auto_close():
            print("🔄 Auto-cerrando aplicación...")
            root.quit()
        
        root.after(5000, auto_close)  # Cerrar automáticamente en 5 segundos
        
        print("🚀 Iniciando mainloop (auto-cierre en 5 segundos)...")
        root.mainloop()
        
        print("✅ Aplicación funcionó correctamente!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Cambiar al directorio del proyecto
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)
    print(f"Directorio: {os.getcwd()}")
    
    main()
