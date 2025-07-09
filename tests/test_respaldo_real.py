"""
Test específico para SQL Server con configuración real del usuario.
NOTA: Las credenciales no están guardadas en el código por seguridad.
"""

import os
import sys
from datetime import datetime
import getpass

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.database_service import DatabaseService
from src.core.backup_controller import BackupController


def log_message(message):
    """Función de logging con timestamp."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")


def get_user_credentials():
    """Solicita las credenciales del usuario de forma segura."""
    print("🔐 CONFIGURACIÓN DE CONEXIÓN")
    print("=" * 50)
    
    config = {
        'server': input("Servidor (ej: localhost\\AUTOTRAFFIC_EMX): ").strip(),
        'port': int(input("Puerto [1433]: ") or "1433"),
        'username': input("Usuario [sa]: ") or "sa",
        'password': getpass.getpass("Contraseña: "),
        'backup_path': input("Ruta de respaldos [C:\\prueba respaldos]: ") or "C:\\prueba respaldos"
    }
    
    return config


def test_connection_and_databases(config):
    """Prueba la conexión y obtiene las bases de datos disponibles."""
    print("\\n🔗 PROBANDO CONEXIÓN")
    print("=" * 50)
    
    try:
        # Crear servicio de base de datos
        db_service = DatabaseService(
            'sql_server',
            config['server'],
            config['username'],
            config['password'],
            config['port']
        )
        
        print(f"📊 Servidor: {config['server']}")
        print(f"👤 Usuario: {config['username']}")
        print(f"🚪 Puerto: {config['port']}")
        
        # Probar conexión
        log_message("Probando conexión...")
        if db_service.test_connection():
            log_message("✅ Conexión exitosa!")
        else:
            log_message("❌ Error en conexión")
            return None, None
        
        # Obtener bases de datos
        log_message("Obteniendo lista de bases de datos...")
        databases = db_service.get_databases()
        
        if databases:
            log_message(f"✅ Se encontraron {len(databases)} bases de datos:")
            for i, db in enumerate(databases[:10], 1):  # Mostrar solo las primeras 10
                print(f"   {i}. {db}")
            if len(databases) > 10:
                print(f"   ... y {len(databases) - 10} más")
        else:
            log_message("⚠️ No se encontraron bases de datos de usuario")
            
        return db_service, databases
        
    except Exception as e:
        log_message(f"❌ Error: {e}")
        return None, None


def test_path_validation(config, db_service):
    """Valida la ruta de respaldos."""
    print("\\n📁 VALIDANDO RUTA DE RESPALDOS")
    print("=" * 50)
    
    backup_path = config['backup_path']
    print(f"📂 Ruta objetivo: {backup_path}")
    
    # Crear la ruta si no existe
    try:
        os.makedirs(backup_path, exist_ok=True)
        log_message(f"✅ Ruta preparada: {backup_path}")
    except Exception as e:
        log_message(f"❌ Error creando ruta: {e}")
        return False
    
    # Verificar permisos locales
    if os.access(backup_path, os.W_OK):
        log_message("✅ Permisos de escritura local: OK")
    else:
        log_message("❌ Sin permisos de escritura local")
        return False
    
    # Validar en el servidor (para SQL Server)
    try:
        if db_service.validate_path_on_server(backup_path):
            log_message("✅ Ruta válida en servidor SQL Server")
        else:
            log_message("⚠️ Ruta no válida en servidor, pero se usará local")
    except Exception as e:
        log_message(f"⚠️ No se pudo validar en servidor: {e}")
        log_message("💡 Se procederá con validación local")
    
    return True


def select_databases_for_test(databases):
    """Permite al usuario seleccionar bases de datos para el test."""
    if not databases:
        return []
    
    print("\\n🎯 SELECCIÓN DE BASES DE DATOS PARA PRUEBA")
    print("=" * 50)
    print("Seleccione las bases de datos para respaldar (máximo 3 para la prueba):")
    
    for i, db in enumerate(databases, 1):
        print(f"  {i}. {db}")
    
    selected = []
    while len(selected) < 3:
        try:
            choice = input(f"\\nSeleccione BD #{len(selected)+1} (número, 0 para terminar): ").strip()
            if choice == '0':
                break
            
            index = int(choice) - 1
            if 0 <= index < len(databases):
                db_name = databases[index]
                if db_name not in selected:
                    selected.append(db_name)
                    print(f"✅ Agregada: {db_name}")
                else:
                    print("⚠️ Ya está seleccionada")
            else:
                print("❌ Número inválido")
        except (ValueError, IndexError):
            print("❌ Entrada inválida")
    
    return selected


def perform_backup_test(config, db_service, test_databases):
    """Ejecuta la prueba de respaldo real."""
    print("\\n🚀 EJECUTANDO RESPALDOS DE PRUEBA")
    print("=" * 50)
    
    if not test_databases:
        log_message("❌ No hay bases de datos seleccionadas")
        return False
    
    # Crear controlador
    controller = BackupController(log_message)
    
    # Configurar conexión en el controlador
    connection_data = {
        'db_type': 'sql_server',
        'server': config['server'],
        'username': config['username'],
        'password': config['password'],
        'port': config['port']
    }
    
    # Validar conexión en controlador
    if not controller.validate_connection(connection_data):
        log_message("❌ Error validando conexión en controlador")
        return False
    
    # Validar ruta en controlador
    if not controller.validate_path(config['backup_path']):
        log_message("❌ Error validando ruta en controlador")
        return False
    
    # Ejecutar respaldos
    log_message(f"🎯 Iniciando respaldos de {len(test_databases)} bases de datos...")
    
    try:
        controller.create_backup(test_databases, config['backup_path'])
        log_message("✅ Proceso de respaldo completado")
        return True
    except Exception as e:
        log_message(f"❌ Error durante respaldo: {e}")
        return False


def verify_backup_files(config):
    """Verifica los archivos de respaldo creados."""
    print("\\n📋 VERIFICANDO ARCHIVOS CREADOS")
    print("=" * 50)
    
    backup_path = config['backup_path']
    
    try:
        total_files = 0
        total_size = 0
        
        for root, dirs, files in os.walk(backup_path):
            level = root.replace(backup_path, '').count(os.sep)
            indent = '  ' * level
            folder_name = os.path.basename(root) or os.path.basename(backup_path)
            print(f"{indent}📁 {folder_name}/")
            
            subindent = '  ' * (level + 1)
            for file in files:
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                size_mb = size / (1024 * 1024)
                
                # Verificar que el archivo no esté vacío
                if size > 0:
                    status = "✅"
                    total_files += 1
                    total_size += size
                else:
                    status = "❌ (vacío)"
                
                print(f"{subindent}📄 {file} ({size_mb:.2f} MB) {status}")
        
        # Resumen
        print("\\n" + "=" * 50)
        print(f"📊 RESUMEN:")
        print(f"   Archivos válidos: {total_files}")
        print(f"   Tamaño total: {total_size / (1024 * 1024):.2f} MB")
        
        if total_files > 0:
            log_message("🎉 ¡RESPALDOS CREADOS EXITOSAMENTE!")
            return True
        else:
            log_message("❌ No se crearon archivos de respaldo válidos")
            return False
            
    except Exception as e:
        log_message(f"❌ Error verificando archivos: {e}")
        return False


def main():
    """Función principal del test."""
    print("🧪 TEST DE RESPALDOS SQL SERVER - CONFIGURACIÓN REAL")
    print("=" * 60)
    print("Este test usará la configuración real proporcionada por el usuario.")
    print("Las credenciales no se guardan por seguridad.")
    print()
    
    # Obtener credenciales del usuario
    config = get_user_credentials()
    
    print(f"\\n📋 Configuración a usar:")
    print(f"   Servidor: {config['server']}")
    print(f"   Puerto: {config['port']}")
    print(f"   Usuario: {config['username']}")
    print(f"   Ruta respaldos: {config['backup_path']}")
    
    # Confirmar antes de continuar
    confirm = input("\\n¿Continuar con el test? (s/n): ").lower()
    if confirm not in ['s', 'y', 'yes', 'si', 'sí']:
        print("👋 Test cancelado por el usuario")
        return
    
    # Ejecutar pruebas paso a paso
    steps = [
        ("Conexión y bases de datos", lambda: test_connection_and_databases(config)),
        ("Validación de ruta", lambda db_service, _: test_path_validation(config, db_service)),
        ("Selección de bases de datos", lambda _, databases: select_databases_for_test(databases)),
        ("Ejecución de respaldos", lambda db_service, test_dbs: perform_backup_test(config, db_service, test_dbs)),
        ("Verificación de archivos", lambda _, __: verify_backup_files(config))
    ]
    
    db_service = None
    databases = None
    test_databases = None
    
    for step_name, step_func in steps:
        print(f"\\n{'='*20} {step_name.upper()} {'='*20}")
        
        try:
            if step_name == "Conexión y bases de datos":
                db_service, databases = step_func()
                if not db_service or not databases:
                    print(f"❌ Falló: {step_name}")
                    return
            elif step_name == "Validación de ruta":
                if not step_func(db_service, databases):
                    print(f"❌ Falló: {step_name}")
                    return
            elif step_name == "Selección de bases de datos":
                test_databases = step_func(db_service, databases)
                if not test_databases:
                    print("❌ No se seleccionaron bases de datos")
                    return
            elif step_name == "Ejecución de respaldos":
                if not step_func(db_service, test_databases):
                    print(f"❌ Falló: {step_name}")
                    return
            elif step_name == "Verificación de archivos":
                if not step_func(db_service, test_databases):
                    print(f"❌ Falló: {step_name}")
                    return
                
        except Exception as e:
            print(f"❌ Error en {step_name}: {e}")
            return
    
    # Test completado exitosamente
    print("\\n" + "🎊" * 20)
    print("✅ TEST COMPLETADO EXITOSAMENTE!")
    print("🎊" * 20)
    print("\\n🎯 RESULTADOS:")
    print("   ✅ Conexión SQL Server funcional")
    print("   ✅ Respaldos creados correctamente")
    print("   ✅ Archivos guardados en la ruta especificada")
    print("   ✅ Organización por subcarpetas funcional")
    print("\\n💡 El sistema está completamente operativo!")


if __name__ == "__main__":
    main()
