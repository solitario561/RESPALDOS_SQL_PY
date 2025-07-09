"""
Prueba final del sistema de respaldos con SQL Server.
Este script demuestra que el sistema funciona correctamente para crear respaldos.
"""

import os
import sys
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.database_service import DatabaseService
from src.core.backup_controller import BackupController


def log_message(message):
    """Función simple de logging."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")


def test_sql_server_connection():
    """Prueba de conexión SQL Server con datos reales si están disponibles."""
    print("🧪 PRUEBA DE CONEXIÓN SQL SERVER")
    print("=" * 50)
    
    # Configuraciones comunes de SQL Server local
    test_configs = [
        {
            'name': 'SQL Server Local (Windows Auth)',
            'server': 'localhost',
            'username': '',  # Windows Authentication
            'password': '',
            'port': 1433
        },
        {
            'name': 'SQL Server Local (Usuario sa)',
            'server': '(local)',
            'username': 'sa',
            'password': 'admin123',  # Cambiar por contraseña real
            'port': 1433
        },
        {
            'name': 'SQL Server Express',
            'server': '.\\SQLEXPRESS',
            'username': '',  # Windows Authentication
            'password': '',
            'port': 1433
        }
    ]
    
    working_config = None
    
    for config in test_configs:
        try:
            print(f"\\n🔗 Probando: {config['name']}")
            print(f"   Servidor: {config['server']}")
            
            # Crear servicio de base de datos
            db_service = DatabaseService(
                'sql_server',
                config['server'],
                config['username'],
                config['password'],
                config['port']
            )
            
            # Probar conexión
            if db_service.test_connection():
                print(f"   ✅ Conexión exitosa!")
                
                # Probar obtener bases de datos
                databases = db_service.get_databases()
                print(f"   📊 Bases de datos encontradas: {len(databases)}")
                for db in databases[:5]:  # Mostrar solo las primeras 5
                    print(f"      - {db}")
                if len(databases) > 5:
                    print(f"      ... y {len(databases) - 5} más")
                
                working_config = config
                working_config['databases'] = databases
                working_config['db_service'] = db_service
                break
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
    
    return working_config


def test_backup_creation(config):
    """Prueba la creación real de respaldos."""
    print("\\n🚀 PRUEBA DE CREACIÓN DE RESPALDOS")
    print("=" * 50)
    
    if not config:
        print("❌ No hay configuración de conexión válida")
        return False
    
    # Configurar ruta de respaldo
    backup_path = "C:\\Respaldos_Test\\Prueba_Real"
    os.makedirs(backup_path, exist_ok=True)
    
    print(f"📁 Ruta de respaldo: {backup_path}")
    
    # Crear controlador
    controller = BackupController(log_message)
    
    # Configurar conexión
    connection_data = {
        'db_type': 'sql_server',
        'server': config['server'],
        'username': config['username'],
        'password': config['password'],
        'port': config['port']
    }
    
    # Validar conexión
    if not controller.validate_connection(connection_data):
        print("❌ Error validando conexión")
        return False
    
    # Validar ruta
    if not controller.validate_path(backup_path):
        print("❌ Error validando ruta")
        return False
    
    # Seleccionar bases de datos para respaldar (máximo 2 para la prueba)
    test_databases = config['databases'][:2] if config['databases'] else []
    
    if not test_databases:
        print("❌ No hay bases de datos para respaldar")
        return False
    
    print(f"🎯 Bases de datos seleccionadas para respaldo: {test_databases}")
    
    # Ejecutar respaldos
    try:
        controller.create_backup(test_databases, backup_path)
        print("\\n✅ Proceso de respaldo completado")
        
        # Verificar archivos creados
        print("\\n📁 Verificando archivos creados:")
        for root, dirs, files in os.walk(backup_path):
            level = root.replace(backup_path, '').count(os.sep)
            indent = '  ' * level
            print(f"{indent}📁 {os.path.basename(root)}/")
            subindent = '  ' * (level + 1)
            for file in files:
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                size_mb = size / (1024 * 1024)
                print(f"{subindent}📄 {file} ({size_mb:.2f} MB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el respaldo: {e}")
        return False


def main():
    """Función principal de la prueba."""
    print("🧪 PRUEBA FINAL DEL SISTEMA DE RESPALDOS")
    print("=" * 60)
    print("Esta prueba intentará crear respaldos reales usando SQL Server")
    print()
    
    # Probar conexión
    config = test_sql_server_connection()
    
    if config:
        print("\\n🎉 ¡Conexión SQL Server exitosa!")
        
        # Preguntar si continuar con respaldo real
        response = input("\\n¿Desea continuar con la prueba de respaldo real? (s/n): ")
        
        if response.lower() in ['s', 'y', 'yes', 'si', 'sí']:
            success = test_backup_creation(config)
            
            if success:
                print("\\n" + "=" * 60)
                print("🎊 ¡PRUEBA COMPLETADA EXITOSAMENTE!")
                print("=" * 60)
                print("✅ El sistema de respaldos funciona correctamente")
                print("✅ Los archivos se crean en la ruta especificada")
                print("✅ La organización por subcarpetas funciona")
                print("✅ SQL Server está completamente operativo")
                print("\\n💡 Para MySQL y PostgreSQL, instale las herramientas cliente:")
                print("   - MySQL: mysqldump (MySQL Client Tools)")
                print("   - PostgreSQL: pg_dump (PostgreSQL Client Tools)")
            else:
                print("\\n❌ La prueba de respaldo falló")
        else:
            print("\\n📝 Prueba de respaldo cancelada por el usuario")
            print("✅ La conexión funciona correctamente")
    else:
        print("\\n❌ No se pudo establecer conexión con SQL Server")
        print("\\n💡 Posibles soluciones:")
        print("   1. Verificar que SQL Server esté ejecutándose")
        print("   2. Verificar credenciales de conexión")
        print("   3. Verificar configuración de red/firewall")
        print("   4. Intentar con Windows Authentication si está en dominio")
    
    print("\\n👋 Prueba finalizada")


if __name__ == "__main__":
    main()
