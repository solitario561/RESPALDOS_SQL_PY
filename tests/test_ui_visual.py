"""
Script de prueba visual mejorado para verificar que todas las opciones 
de configuración sean visibles en la interfaz de usuario.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
import threading
import time

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ui():
    """Prueba visual rápida de la interfaz de usuario."""
    print("🚀 Iniciando prueba visual rápida de la UI...")
    
    try:
        # Importar y crear la aplicación
        from src.main import BackupApp
        
        # Crear ventana principal
        root = tk.Tk()
        
        # Configurar tamaño y título
        root.geometry("1000x700")
        root.title("PRUEBA VISUAL - Respaldos SQL - Todas las Configuraciones")
        
        # Crear la aplicación
        app = BackupApp(root)
        
        print("📋 Verificando componentes principales:")
        print(f"   • Frame de conexión: {'✅' if hasattr(app, 'connection_frame') else '❌'}")
        print(f"   • Frame de control: {'✅' if hasattr(app, 'control_frame') else '❌'}")
        print(f"   • Frame de logs: {'✅' if hasattr(app, 'log_frame') else '❌'}")
        
        # Verificar componentes del connection_frame
        if hasattr(app, 'connection_frame'):
            cf = app.connection_frame
            print("📋 Verificando secciones de configuración:")
            print(f"   • Combo tipo BD: {'✅' if hasattr(cf, 'db_type_combo') else '❌'}")
            print(f"   • Campo servidor: {'✅' if hasattr(cf, 'server_var') else '❌'}")
            print(f"   • Campo usuario: {'✅' if hasattr(cf, 'user_var') else '❌'}")
            print(f"   • Campo contraseña: {'✅' if hasattr(cf, 'pwd_var') else '❌'}")
            print(f"   • Campo ruta: {'✅' if hasattr(cf, 'path_var') else '❌'}")
            print(f"   • Listbox BD: {'✅' if hasattr(cf, 'db_listbox') else '❌'}")
            print(f"   • Combo frecuencia: {'✅' if hasattr(cf, 'freq_var') else '❌'}")
            print(f"   • Campo hora: {'✅' if hasattr(cf, 'time_var') else '❌'}")
        
        # Función para cerrar automáticamente
        def auto_close():
            print("\n✅ PRUEBA COMPLETADA:")
            print("   - La interfaz debe mostrar TODAS las secciones:")
            print("     📚 Conexiones anteriores")
            print("     ⚙️ Configuración de Conexión") 
            print("     💾 Selección de Bases de Datos")
            print("     📁 Configuración de Respaldo")
            print("     ⏰ Programación de Respaldos")
            print("     🎛️ Botones de Control")
            print("     📋 Logs")
            print("\n💡 Si alguna sección no es visible, hay un problema de layout.")
            print("⏳ Cerrando en 3 segundos...")
            root.after(3000, root.destroy)
        
        # Programar cierre automático después de mostrar
            root.after(2000, auto_close)
            print(f"   • Contraseña: {'✅' if hasattr(cf, 'pwd_var') else '❌'}")
            print(f"   • Lista de BD: {'✅' if hasattr(cf, 'db_listbox') else '❌'}")
            print(f"   • Ruta de respaldo: {'✅' if hasattr(cf, 'path_var') else '❌'}")
            print(f"   • Programación: {'✅' if hasattr(cf, 'freq_var') else '❌'}")
        
        print("\n🖥️ Iniciando interfaz gráfica...")
        print("   Manténgala abierta para verificar visualmente todas las opciones.")
        print("   La aplicación se cerrará automáticamente después de 5 segundos.")
        
        # Ejecutar la aplicación
        root.mainloop()
        
        print("✅ Prueba visual completada exitosamente.")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba visual: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_ui()
