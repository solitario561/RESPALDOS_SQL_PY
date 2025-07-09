#!/usr/bin/env python3
"""
Script de prueba simple para identificar dónde se cuelga la aplicación.
"""

import sys
import os
import traceback

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_step_by_step():
    """Prueba paso a paso el inicio de la aplicación."""
    
    print("INICIANDO PRUEBA PASO A PASO...")
    print("=" * 50)
    
    try:
        print("Paso 1: Importando tkinter...")
        import tkinter as tk
        print("✓ tkinter OK")
        
        print("Paso 2: Creando ventana básica...")
        root = tk.Tk()
        root.title("Test")
        print("✓ Ventana básica OK")
        
        print("Paso 3: Importando configuración...")
        from config.settings import UI_CONFIG
        print("✓ Configuración OK")
        
        print("Paso 4: Importando servicios...")
        from src.services.file_service import FileService, ConnectionHistoryService
        print("✓ Servicios OK")
        
        print("Paso 5: Probando historial de conexiones...")
        history = ConnectionHistoryService.get_connection_display_list()
        print(f"✓ Historial OK: {len(history)} conexiones")
        
        print("Paso 6: Importando controlador...")
        from src.core.backup_controller import BackupController
        print("✓ Controlador OK")
        
        print("Paso 7: Importando componentes UI...")
        from src.ui.ui_components import ConnectionFrame
        print("✓ Componentes UI OK")
        
        print("Paso 8: Creando callback dummy...")
        def dummy_callback(*args):
            print(f"Callback llamado con: {args}")
            return True
        
        print("Paso 9: Creando ConnectionFrame...")
        connection_frame = ConnectionFrame(
            root,
            dummy_callback,  # validate_connection_callback
            dummy_callback,  # validate_path_callback
            dummy_callback   # load_databases_callback
        )
        print("✓ ConnectionFrame creado OK")
        
        print("Paso 10: Configurando layout básico...")
        connection_frame.frame.pack(fill="both", expand=True)
        print("✓ Layout OK")
        
        print("Paso 11: Probando update...")
        root.update_idletasks()
        print("✓ Update OK")
        
        print("Paso 12: Cerrando ventana...")
        root.destroy()
        print("✓ Ventana cerrada OK")
        
        print("\n🎉 TODOS LOS PASOS COMPLETADOS EXITOSAMENTE")
        
    except Exception as e:
        print(f"\n❌ ERROR en el paso actual: {e}")
        print("\nTraceback completo:")
        traceback.print_exc()
        return False
    
    return True

def test_minimal_app():
    """Prueba una aplicación mínima."""
    print("\n" + "=" * 50)
    print("PROBANDO APLICACIÓN MÍNIMA...")
    print("=" * 50)
    
    try:
        import tkinter as tk
        from src.main import BackupApp
        
        print("Creando aplicación...")
        root = tk.Tk()
        
        # Configurar timeout para evitar colgado
        def timeout():
            print("⏰ Timeout - cerrando aplicación...")
            root.quit()
            root.destroy()
        
        # Timeout de 5 segundos
        root.after(5000, timeout)
        
        print("Inicializando BackupApp...")
        app = BackupApp(root)
        
        print("Iniciando mainloop con timeout...")
        root.mainloop()
        
        print("✓ Aplicación cerrada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en aplicación mínima: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Cambiar al directorio del proyecto
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)
    print(f"Directorio: {os.getcwd()}")
    
    # Ejecutar pruebas
    if test_step_by_step():
        test_minimal_app()
    else:
        print("\n⚠️ Falló la prueba paso a paso. No se ejecutará la aplicación mínima.")
