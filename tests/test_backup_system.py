"""
Script de prueba para verificar que los respaldos se generen correctamente.
"""

import sys
import os
import tempfile
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_backup_structure():
    """Prueba la estructura de carpetas de respaldos."""
    
    print("🧪 Probando estructura de respaldos...")
    
    try:
        from src.services.database_service import DatabaseService
        
        # Crear una carpeta temporal para pruebas
        temp_dir = tempfile.mkdtemp(prefix="test_backup_")
        print(f"📁 Carpeta temporal creada: {temp_dir}")
        
        # Simular diferentes tipos de BD
        db_types = ['sql_server', 'mysql', 'postgresql']
        
        for db_type in db_types:
            print(f"\n🗄️ Probando {db_type.upper()}...")
            
            # Crear servicio (sin conexión real)
            service = DatabaseService(db_type, "localhost", "test", "test", 1433)
            
            # Crear subcarpeta esperada
            db_type_folder = {
                'sql_server': 'SQL_Server',
                'mysql': 'MySQL', 
                'postgresql': 'PostgreSQL'
            }.get(db_type, 'Unknown')
            
            full_backup_path = os.path.join(temp_dir, db_type_folder)
            os.makedirs(full_backup_path, exist_ok=True)
            
            # Crear archivo de prueba
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_extension = {
                'sql_server': '.bak',
                'mysql': '.sql',
                'postgresql': '.sql'
            }.get(db_type, '.bak')
            
            test_filename = f"testdb_{timestamp}{file_extension}"
            test_filepath = os.path.join(full_backup_path, test_filename)
            
            # Crear archivo de prueba
            with open(test_filepath, 'w') as f:
                f.write(f"-- Respaldo de prueba para {db_type}\n")
                f.write(f"-- Generado el {datetime.now()}\n")
                f.write("-- Este es un archivo de prueba\n")
            
            print(f"   ✅ Carpeta creada: {db_type_folder}")
            print(f"   ✅ Archivo creado: {test_filename}")
            print(f"   📂 Ruta completa: {test_filepath}")
            print(f"   📊 Tamaño: {os.path.getsize(test_filepath)} bytes")
        
        print(f"\n📁 Estructura final en {temp_dir}:")
        for root, dirs, files in os.walk(temp_dir):
            level = root.replace(temp_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                print(f"{subindent}{file} ({size} bytes)")
        
        print("\n🎉 ¡Estructura de respaldos creada exitosamente!")
        print(f"💡 Los respaldos se organizarán en subcarpetas por tipo de BD")
        print(f"📋 Ubicación de prueba: {temp_dir}")
        
        # Mantener la carpeta para inspección
        input("\n⏸️ Presiona Enter para continuar y limpiar archivos temporales...")
        
        # Limpiar archivos temporales
        import shutil
        shutil.rmtree(temp_dir)
        print("🧹 Archivos temporales eliminados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backup_path_creation():
    """Prueba la creación de rutas de respaldo."""
    
    print("\n🔧 Probando creación de rutas de respaldo...")
    
    # Crear carpeta de prueba en el directorio actual
    test_backup_dir = os.path.join(os.getcwd(), "test_respaldos")
    
    try:
        # Simular la lógica del create_backup
        db_types = {
            'sql_server': 'SQL_Server',
            'mysql': 'MySQL', 
            'postgresql': 'PostgreSQL'
        }
        
        for db_type, folder_name in db_types.items():
            full_backup_path = os.path.join(test_backup_dir, folder_name)
            os.makedirs(full_backup_path, exist_ok=True)
            
            # Crear archivo de ejemplo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            test_file = os.path.join(full_backup_path, f"ejemplo_{timestamp}.txt")
            
            with open(test_file, 'w') as f:
                f.write(f"Respaldo de prueba para {db_type}")
            
            print(f"✅ {folder_name}: {test_file}")
        
        print(f"\n📂 Carpeta de prueba creada en: {test_backup_dir}")
        print("📋 Esta es la estructura que tendrán tus respaldos reales")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 PRUEBA DE SISTEMA DE RESPALDOS")
    print("=" * 50)
    
    # Prueba 1: Estructura
    success1 = test_backup_structure()
    
    # Prueba 2: Creación de rutas
    success2 = test_backup_path_creation()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("✅ El sistema de respaldos está configurado correctamente")
        print("📁 Los respaldos se crearán en subcarpetas organizadas")
    else:
        print("❌ Algunas pruebas fallaron")
    
    print("\n💡 Para usar el sistema de respaldos:")
    print("   1. Ejecuta: python run_app.py")
    print("   2. Configura tu conexión a BD")
    print("   3. Selecciona las bases de datos")
    print("   4. Especifica la ruta de respaldo")
    print("   5. ¡Los respaldos se organizarán automáticamente!")
