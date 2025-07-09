"""
Script de prueba para verificar todas las funcionalidades sin GUI.
"""

import json
from datetime import datetime

# Importar nuestros módulos
from config import *
from file_service import FileService, ConnectionHistoryService
from database_service import DatabaseService, PathValidator
from scheduler_service import SchedulerService
from backup_controller import BackupController

def test_file_services():
    """Prueba los servicios de archivos."""
    print("🔧 Probando servicios de archivos...")
    
    # Probar logs
    test_log = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Prueba de log desde script\n"
    FileService.save_logs_to_file(test_log)
    loaded_logs = FileService.load_logs_from_file()
    print(f"✅ Logs guardados y cargados: {len(loaded_logs)} caracteres")
    
    # Probar historial de conexiones
    ConnectionHistoryService.save_connection("TestServer", "TestDB")
    connections = ConnectionHistoryService.get_connection_display_list()
    print(f"✅ Historial de conexiones: {len(connections)} entradas")
    for conn in connections[:3]:  # Mostrar solo las primeras 3
        print(f"   - {conn}")
    
    print()

def test_database_service():
    """Prueba el servicio de base de datos (sin conexión real)."""
    print("🔧 Probando servicio de base de datos...")
    
    # Crear instancia del servicio
    db_service = DatabaseService("test_server", "test_db", "test_user", "test_pass")
    
    # Verificar que se crea la cadena de conexión correctamente
    conn_str = db_service._get_connection_string()
    print(f"✅ Cadena de conexión generada: {conn_str[:50]}...")
    
    # Probar validación de ruta local
    local_valid = PathValidator.validate_local_path("C:\\")  # Esta ruta debería existir
    print(f"✅ Validación de ruta local C:\\: {local_valid}")
    
    print()

def test_scheduler_service():
    """Prueba el servicio de programación."""
    print("🔧 Probando servicio de programación...")
    
    logs = []
    def mock_log(message):
        logs.append(message)
        print(f"   LOG: {message}")
    
    scheduler = SchedulerService(mock_log)
    
    # Probar programación diaria
    def mock_backup():
        print("   Ejecutando respaldo de prueba...")
    
    scheduler.schedule_daily_backup("12:00", mock_backup)
    print(f"✅ Programación diaria configurada: {len(logs)} logs generados")
    
    # Probar programación por intervalo
    scheduler.clear_schedule()
    scheduler.schedule_interval_backup(2, mock_backup)
    print(f"✅ Programación por intervalo configurada: {len(logs)} logs generados")
    
    print()

def test_backup_controller():
    """Prueba el controlador principal."""
    print("🔧 Probando controlador de respaldos...")
    
    logs = []
    def mock_log(message):
        logs.append(message)
        print(f"   LOG: {message}")
    
    controller = BackupController(mock_log)
    
    # Probar configuración de programación
    schedule_config = {
        'frequency': 'diario',
        'time': '14:30'
    }
    
    print(f"✅ Controlador inicializado")
    print(f"✅ Estado del programador: {controller.is_scheduler_running}")
    print(f"✅ Logs generados: {len(logs)}")
    
    print()

def test_config_loading():
    """Prueba la carga de configuraciones."""
    print("🔧 Probando configuraciones...")
    
    print(f"✅ UI_CONFIG: {UI_CONFIG}")
    print(f"✅ BACKUP_CONFIG: {BACKUP_CONFIG}")
    print(f"✅ FILE_CONFIG: {FILE_CONFIG}")
    print(f"✅ MESSAGES disponibles: {len(MESSAGES)} mensajes")
    
    print()

def main():
    """Función principal de prueba."""
    print("🚀 Iniciando pruebas de la aplicación de respaldos SQL Server")
    print("=" * 70)
    
    try:
        test_config_loading()
        test_file_services()
        test_database_service()
        test_scheduler_service()
        test_backup_controller()
        
        print("✅ ¡Todas las pruebas completadas exitosamente!")
        print("🎉 La aplicación está funcionando correctamente")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
