"""
Script de verificación para comprobar que la aplicación funciona correctamente.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba que todos los imports funcionen correctamente."""
    try:
        print("Probando imports...")
        
        # Probar imports de configuración
        from config.settings import UI_CONFIG, DATABASE_CONFIG, BACKUP_CONFIG
        print("✓ Config imports - OK")
        
        # Probar imports de servicios
        from src.services.database_service import DatabaseService
        from src.services.file_service import FileService
        from src.services.scheduler_service import SchedulerService
        print("✓ Services imports - OK")
        
        # Probar imports de core
        from src.core.backup_controller import BackupController
        print("✓ Core imports - OK")
        
        # Probar imports de UI
        from src.ui.ui_components import ConnectionFrame, LogFrame
        print("✓ UI imports - OK")
        
        # Probar import principal
        from src.main import BackupApp
        print("✓ Main import - OK")
        
        print("\n🎉 ¡Todos los imports funcionan correctamente!")
        print("🚀 La aplicación está lista para ejecutarse con: python run_app.py")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de import: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE ESTRUCTURA DEL PROYECTO")
    print("=" * 60)
    
    success = test_imports()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ VERIFICACIÓN FALLÓ")
        print("=" * 60)
        sys.exit(1)
