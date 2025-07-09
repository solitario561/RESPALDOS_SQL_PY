"""
Script de demostración completa de la aplicación de respaldos.
"""

import os
import time
from datetime import datetime

# Importar módulos de la aplicación
from file_service import FileService, ConnectionHistoryService
from backup_controller import BackupController

class DemoApp:
    """Clase para demostrar las funcionalidades de la aplicación."""
    
    def __init__(self):
        self.logs = []
        self.controller = BackupController(self._log_callback)
    
    def _log_callback(self, message):
        """Callback para capturar logs."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(f"📝 {log_entry}")
    
    def demo_file_operations(self):
        """Demuestra las operaciones con archivos."""
        print("\n🔧 === DEMO: Operaciones con Archivos ===")
        
        # Guardar varios logs
        test_logs = [
            "Iniciando aplicación de respaldos",
            "Cargando configuración",
            "Validando conexión a base de datos",
            "Programando respaldo diario",
            "Respaldo completado exitosamente"
        ]
        
        for log in test_logs:
            self._log_callback(log)
            time.sleep(0.1)  # Pequeña pausa para simular actividad real
        
        # Guardar logs a archivo
        all_logs = "\n".join(self.logs) + "\n"
        if FileService.save_logs_to_file(all_logs):
            print("✅ Logs guardados en archivo")
        
        # Cargar logs desde archivo
        loaded = FileService.load_logs_from_file()
        print(f"✅ Logs cargados: {len(loaded.split('\n'))} líneas")
    
    def demo_connection_history(self):
        """Demuestra el historial de conexiones."""
        print("\n🔧 === DEMO: Historial de Conexiones ===")
        
        # Agregar varias conexiones de prueba
        test_connections = [
            ("PROD-SQL-01", "Ventas"),
            ("DEV-SQL-02", "Inventario"),
            ("TEST-SQL-03", "Usuarios"),
            ("BACKUP-SQL-04", "Reportes")
        ]
        
        for server, database in test_connections:
            ConnectionHistoryService.save_connection(server, database)
            print(f"✅ Conexión guardada: {server} | {database}")
        
        # Mostrar historial
        history = ConnectionHistoryService.get_connection_display_list()
        print(f"\n📋 Historial de conexiones ({len(history)} entradas):")
        for i, conn in enumerate(history, 1):
            print(f"   {i}. {conn}")
    
    def demo_controller_functionality(self):
        """Demuestra la funcionalidad del controlador."""
        print("\n🔧 === DEMO: Funcionalidad del Controlador ===")
        
        # Datos de conexión de prueba
        connection_data = {
            'server': 'localhost',
            'database': 'TestDB',
            'username': 'test_user',
            'password': 'test_pass',
            'backup_path': 'C:\\temp'
        }
        
        print("🔍 Probando validación de conexión (esperamos falla)...")
        # Esta validación fallará porque no hay servidor real
        self.controller.validate_connection(connection_data)
        
        print("🔍 Probando validación de ruta...")
        self.controller.validate_path("C:\\Windows")  # Esta ruta debería existir
        
        # Configuración de programación
        schedule_config = {
            'frequency': 'diario',
            'time': '02:00'
        }
        
        print("📅 Configurando programación...")
        # No iniciamos realmente el scheduler para esta demo
        print(f"✅ Configuración de programación: {schedule_config}")
    
    def demo_file_persistence(self):
        """Demuestra la persistencia de archivos."""
        print("\n🔧 === DEMO: Persistencia de Archivos ===")
        
        # Verificar archivos existentes
        files_to_check = ['backup_logs.txt', 'connections_history.json']
        
        for filename in files_to_check:
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                mod_time = datetime.fromtimestamp(os.path.getmtime(filename))
                print(f"✅ {filename}: {file_size} bytes, modificado: {mod_time}")
            else:
                print(f"❌ {filename}: No existe")
        
        # Leer el contenido actual del historial
        try:
            import json
            with open('connections_history.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                connections = data.get('connections', [])
                print(f"📋 Conexiones en historial: {len(connections)}")
                for conn in connections[:3]:  # Mostrar solo las primeras 3
                    server = conn.get('server', '')
                    database = conn.get('database', '')
                    last_used = conn.get('last_used', '')
                    print(f"   • {server} | {database} (último uso: {last_used[:19]})")
        except Exception as e:
            print(f"❌ Error leyendo historial: {e}")
    
    def run_complete_demo(self):
        """Ejecuta la demostración completa."""
        print("🚀 INICIANDO DEMOSTRACIÓN COMPLETA")
        print("=" * 60)
        
        try:
            self.demo_file_operations()
            self.demo_connection_history()
            self.demo_controller_functionality()
            self.demo_file_persistence()
            
            print("\n" + "=" * 60)
            print("✅ ¡Demostración completada exitosamente!")
            print(f"📊 Total de logs generados: {len(self.logs)}")
            print("🎉 Todas las funcionalidades están operativas")
            
        except Exception as e:
            print(f"\n❌ Error durante la demostración: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Función principal de la demostración."""
    demo = DemoApp()
    demo.run_complete_demo()

if __name__ == "__main__":
    main()
