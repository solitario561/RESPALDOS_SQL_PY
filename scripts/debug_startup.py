#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas durante el inicio de la aplicación.
"""

import sys
import os
import traceback
import logging

# Configurar logging para debug
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug_startup.log'),
        logging.StreamHandler()
    ]
)

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Prueba la importación de todos los módulos."""
    print("=== PROBANDO IMPORTS ===")
    
    try:
        print("1. Importando tkinter...")
        import tkinter as tk
        print("   ✓ tkinter importado correctamente")
        
        print("2. Importando configuración...")
        from config.settings import UI_CONFIG
        print("   ✓ config.settings importado correctamente")
        
        print("3. Importando controlador...")
        from src.core.backup_controller import BackupController
        print("   ✓ backup_controller importado correctamente")
        
        print("4. Importando componentes UI...")
        from src.ui.ui_components import (
            ConnectionFrame, 
            ScheduleFrame, 
            ControlButtonsFrame, 
            LogFrame
        )
        print("   ✓ ui_components importado correctamente")
        
        print("5. Importando aplicación principal...")
        from src.main import BackupApp
        print("   ✓ main.BackupApp importado correctamente")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en imports: {e}")
        traceback.print_exc()
        return False

def test_ui_creation():
    """Prueba la creación de la interfaz de usuario."""
    print("\n=== PROBANDO CREACIÓN DE UI ===")
    
    try:
        import tkinter as tk
        from src.main import BackupApp
        
        print("1. Creando ventana root...")
        root = tk.Tk()
        print("   ✓ Ventana root creada")
        
        print("2. Iniciando BackupApp...")
        app = BackupApp(root)
        print("   ✓ BackupApp inicializada")
        
        print("3. Configurando geometría...")
        root.update_idletasks()
        print(f"   ✓ Geometría configurada: {root.geometry()}")
        
        print("4. Destruyendo ventana...")
        root.destroy()
        print("   ✓ Ventana destruida correctamente")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en creación de UI: {e}")
        traceback.print_exc()
        return False

def test_file_access():
    """Prueba el acceso a archivos de configuración."""
    print("\n=== PROBANDO ACCESO A ARCHIVOS ===")
    
    try:
        print("1. Verificando estructura de directorios...")
        dirs = ['config', 'data', 'src', 'scripts']
        for dir_name in dirs:
            if os.path.exists(dir_name):
                print(f"   ✓ {dir_name}/ existe")
            else:
                print(f"   ❌ {dir_name}/ NO existe")
        
        print("2. Verificando archivos de configuración...")
        config_files = [
            'config/settings.py',
            'data/connections_history.json'
        ]
        
        for file_path in config_files:
            if os.path.exists(file_path):
                print(f"   ✓ {file_path} existe")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(f"   ✓ {file_path} legible ({len(content)} chars)")
                except Exception as e:
                    print(f"   ❌ Error leyendo {file_path}: {e}")
            else:
                print(f"   ❌ {file_path} NO existe")
        
        print("3. Probando carga de historial de conexiones...")
        from src.services.file_service import FileService
        file_service = FileService()
        history = file_service.load_connection_history()
        print(f"   ✓ Historial cargado: {len(history)} conexiones")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en acceso a archivos: {e}")
        traceback.print_exc()
        return False

def main():
    """Función principal de diagnóstico."""
    print("INICIANDO DIAGNÓSTICO DE STARTUP")
    print("=" * 50)
    
    # Cambiar al directorio del proyecto
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)
    print(f"Directorio de trabajo: {os.getcwd()}")
    
    # Ejecutar pruebas
    tests = [
        ("Imports", test_imports),
        ("Acceso a archivos", test_file_access),
        ("Creación de UI", test_ui_creation)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name.upper()} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ ERROR CRÍTICO en {test_name}: {e}")
            traceback.print_exc()
            results[test_name] = False
    
    # Resumen final
    print(f"\n{'='*50}")
    print("RESUMEN DE DIAGNÓSTICO:")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 Todos los tests pasaron. La aplicación debería funcionar correctamente.")
        print("Si aún se cuelga, puede ser un problema de evento de UI o threading.")
    else:
        print("\n⚠️  Hay problemas que deben ser resueltos antes de ejecutar la aplicación.")
    
    print(f"\nLog detallado guardado en: debug_startup.log")

if __name__ == "__main__":
    main()
