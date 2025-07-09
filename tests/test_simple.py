"""
Script de prueba simple para verificar visibilidad de componentes.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simple():
    """Prueba simple y rápida."""
    print("🧪 Prueba rápida de visibilidad de componentes...")
    
    try:
        import tkinter as tk
        from src.main import BackupApp
        
        # Crear ventana
        root = tk.Tk()
        root.geometry("1000x700")
        root.title("PRUEBA - Todas las configuraciones deben ser visibles")
        
        # Crear aplicación
        app = BackupApp(root)
        
        print("✅ Aplicación creada exitosamente")
        print("\n📋 VERIFICAR QUE SEAN VISIBLES:")
        print("   📚 Historial de conexiones")
        print("   🗄️ Tipo de base de datos")
        print("   🖥️ Servidor y puerto")
        print("   👤 Usuario y contraseña")
        print("   💾 Lista de bases de datos")
        print("   📁 Ruta de respaldo")
        print("   ⏰ Programación (frecuencia y hora)")
        print("   🎛️ Botones de control")
        print("   📋 Área de logs")
        
        # Función para auto-cerrar
        def cerrar():
            print("\n🔍 Si todas las secciones son visibles, ¡la aplicación funciona correctamente!")
            print("❌ Si falta alguna sección, hay un problema de layout.")
            root.destroy()
        
        # Auto-cerrar en 5 segundos
        root.after(5000, cerrar)
        
        # Ejecutar
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple()
