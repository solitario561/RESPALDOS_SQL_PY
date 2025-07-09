#!/usr/bin/env python3
"""
Script para probar la aplicación corregida con timeouts y debug.
"""

import sys
import os
import traceback
import threading
import time

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_app_with_timeout():
    """Prueba la aplicación con timeout y debug mejorado."""
    print("PROBANDO APLICACIÓN CORREGIDA...")
    print("=" * 50)
    
    try:
        import tkinter as tk
        from src.main import BackupApp
        
        print("✓ Imports exitosos")
        
        # Crear la aplicación
        root = tk.Tk()
        print("✓ Ventana root creada")
        
        # Variable para controlar si la app se inicializó
        app_ready = threading.Event()
        app_error = threading.Event()
        error_msg = ""
        
        def create_app():
            """Crear la aplicación en un hilo separado para timeout."""
            try:
                nonlocal error_msg
                print("🔧 Iniciando BackupApp...")
                app = BackupApp(root)
                print("✓ BackupApp inicializada correctamente")
                app_ready.set()
            except Exception as e:
                nonlocal error_msg
                error_msg = str(e)
                print(f"❌ Error creando BackupApp: {e}")
                traceback.print_exc()
                app_error.set()
        
        # Iniciar la creación de la app en un hilo separado
        app_thread = threading.Thread(target=create_app, daemon=True)
        app_thread.start()
        
        # Esperar hasta 10 segundos por la inicialización
        print("⏳ Esperando inicialización (máximo 10 segundos)...")
        
        for i in range(10):
            if app_ready.is_set():
                print("✓ Aplicación inicializada exitosamente")
                break
            elif app_error.is_set():
                print(f"❌ Error durante inicialización: {error_msg}")
                return False
            else:
                print(f"   ... esperando ({i+1}/10)")
                time.sleep(1)
        else:
            print("⏰ Timeout - la aplicación no se inicializó en 10 segundos")
            return False
        
        # Si llegamos aquí, la app se inicializó correctamente
        print("🎉 Inicialización exitosa!")
        
        # Programar cierre automático
        def auto_close():
            print("🔄 Cerrando aplicación automáticamente...")
            root.quit()
            root.destroy()
        
        root.after(3000, auto_close)  # Cerrar después de 3 segundos
        
        print("🚀 Iniciando mainloop...")
        root.mainloop()
        
        print("✓ Aplicación cerrada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        traceback.print_exc()
        return False

def test_ui_components_separately():
    """Prueba los componentes de UI por separado."""
    print("\n" + "=" * 50)
    print("PROBANDO COMPONENTES UI POR SEPARADO...")
    print("=" * 50)
    
    try:
        import tkinter as tk
        from src.ui.ui_components import ConnectionFrame
        
        root = tk.Tk()
        root.title("Test Componentes")
        
        print("✓ Ventana creada")
        
        # Callbacks dummy
        def dummy_validate(*args):
            print("Callback validación llamado")
            return True
        
        def dummy_load(*args):
            print("Callback carga llamado")
            return ["test_db1", "test_db2"]
        
        print("Creando ConnectionFrame...")
        conn_frame = ConnectionFrame(
            root,
            dummy_validate,
            dummy_validate, 
            dummy_load
        )
        
        print("✓ ConnectionFrame creado")
        
        # Layout
        conn_frame.frame.pack(fill="both", expand=True)
        root.update_idletasks()
        
        print("✓ Layout configurado")
        
        # Auto-close
        root.after(2000, lambda: root.destroy())
        root.mainloop()
        
        print("✓ Componentes UI funcionan correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en componentes UI: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Cambiar al directorio del proyecto
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)
    print(f"Directorio: {os.getcwd()}")
    
    # Ejecutar pruebas
    print("INICIANDO PRUEBAS DE LA APLICACIÓN CORREGIDA")
    print("=" * 60)
    
    # Primero probar componentes por separado
    if test_ui_components_separately():
        print("\n✅ Componentes UI funcionan - procediendo con aplicación completa")
        test_app_with_timeout()
    else:
        print("\n❌ Los componentes UI fallan - no se probará la aplicación completa")
