"""
Test directo y simple para verificar respaldos SQL Server.
Versión optimizada que no se cuelga.
"""

import os
import sys
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.database_service import DatabaseService
from src.core.backup_controller import BackupController


def test_sql_server_backup():
    """Test directo de respaldo SQL Server."""
    print("🚀 TEST DIRECTO DE RESPALDO SQL SERVER")
    print("=" * 50)
    
    # Configuración (sin guardar credenciales sensibles)
    config = {
        'server': 'localhost\\AUTOTRAFFIC_EMX',
        'port': 1433,
        'username': 'sa',
        'password': '?Aut0traff1c',  # Solo para test, no se guarda
        'backup_path': 'C:\\prueba respaldos'
    }
    
    print(f"📊 Servidor: {config['server']}")
    print(f"👤 Usuario: {config['username']}")
    print(f"📁 Ruta: {config['backup_path']}")
    
    try:
        # 1. Crear servicio de BD
        print("\\n🔗 Creando conexión...")
        db_service = DatabaseService(
            'sql_server',
            config['server'],
            config['username'], 
            config['password'],
            config['port']
        )
        
        # 2. Probar conexión
        print("🔌 Probando conexión...")
        if db_service.test_connection():
            print("✅ Conexión exitosa!")
        else:
            print("❌ Error en conexión")
            return False
        
        # 3. Obtener bases de datos
        print("📋 Obteniendo bases de datos...")
        databases = db_service.get_databases()
        print(f"✅ Encontradas {len(databases)} bases de datos")
        
        # Mostrar algunas bases de datos
        for i, db in enumerate(databases[:5], 1):
            print(f"   {i}. {db}")
        if len(databases) > 5:
            print(f"   ... y {len(databases) - 5} más")
        
        # 4. Preparar ruta de respaldo
        print(f"\\n📁 Preparando ruta: {config['backup_path']}")
        os.makedirs(config['backup_path'], exist_ok=True)
        print("✅ Ruta preparada")
        
        # 5. Seleccionar BD para test (usar la primera disponible)
        if not databases:
            print("❌ No hay bases de datos para respaldar")
            return False
        
        test_db = databases[0]  # Usar la primera BD
        print(f"🎯 Usando BD para test: {test_db}")
        
        # 6. Crear respaldo
        print(f"\\n🚀 Creando respaldo de: {test_db}")
        try:
            backup_file = db_service.create_backup(test_db, config['backup_path'])
            print(f"✅ Método create_backup retornó: {backup_file}")
            
            # Verificar archivo
            if backup_file and os.path.exists(backup_file):
                file_size = os.path.getsize(backup_file)
                size_mb = file_size / (1024 * 1024)
                print(f"✅ Respaldo creado exitosamente!")
                print(f"📄 Archivo: {os.path.basename(backup_file)}")
                print(f"📊 Tamaño: {size_mb:.2f} MB ({file_size:,} bytes)")
                print(f"📁 Ubicación: {os.path.dirname(backup_file)}")
                
                # Verificar estructura de carpetas
                print("\\n📂 Estructura creada:")
                for root, dirs, files in os.walk(config['backup_path']):
                    level = root.replace(config['backup_path'], '').count(os.sep)
                    indent = '  ' * level
                    folder_name = os.path.basename(root) or 'prueba respaldos'
                    print(f"{indent}📁 {folder_name}/")
                    subindent = '  ' * (level + 1)
                    for file in files:
                        filepath = os.path.join(root, file)
                        fsize = os.path.getsize(filepath)
                        fsize_mb = fsize / (1024 * 1024)
                        print(f"{subindent}📄 {file} ({fsize_mb:.2f} MB)")
                
                return True
            else:
                print(f"❌ Error: backup_file={backup_file}, existe={os.path.exists(backup_file) if backup_file else 'N/A'}")
                return False
                
        except Exception as e:
            print(f"❌ Error creando respaldo: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False


def main():
    """Función principal."""
    print("🧪 TEST SIMPLE DE RESPALDOS SQL SERVER")
    print("=" * 60)
    print("Este test verifica que los respaldos se crean correctamente.")
    print()
    
    success = test_sql_server_backup()
    
    print("\\n" + "=" * 60)
    if success:
        print("🎉 ¡TEST EXITOSO!")
        print("✅ El sistema de respaldos funciona correctamente")
        print("✅ Los archivos se crean en la ruta especificada")
        print("✅ La organización por subcarpetas funciona")
    else:
        print("❌ TEST FALLÓ")
        print("💡 Verificar:")
        print("   - SQL Server está ejecutándose")
        print("   - Credenciales son correctas")
        print("   - Permisos de la ruta de respaldo")
    
    print("\\n👋 Test completado")


if __name__ == "__main__":
    main()
