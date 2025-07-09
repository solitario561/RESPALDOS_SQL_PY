#!/usr/bin/env python3
"""
Script principal para ejecutar la aplicación de respaldos SQL corregida.
"""

import sys
import os

# Agregar el directorio raíz al path para imports relativos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Función principal para ejecutar la aplicación."""
    try:
        print("🚀 Iniciando Aplicación de Respaldos SQL...")
        
        import tkinter as tk
        from src.main import BackupApp
        
        # Configurar la aplicación
        root = tk.Tk()
        app = BackupApp(root)
        
        print("✅ Aplicación iniciada exitosamente")
        print("📋 Para cerrar la aplicación, use el botón X de la ventana")
        
        # Ejecutar la aplicación
        root.mainloop()
        
        print("👋 Aplicación cerrada")
        
    except KeyboardInterrupt:
        print("\n⏹️ Aplicación interrumpida por el usuario")
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrese de que todas las dependencias estén instaladas")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
