"""
Controlador principal de la aplicación de respaldos SQL Server.
"""

import os
from typing import Optional
from src.services.database_service import DatabaseService, PathValidator
from src.services.scheduler_service import SchedulerService
from src.ui.ui_components import MessageHelper
from config.settings import MESSAGES


class BackupController:
    """Controlador principal para la lógica de respaldos."""
    
    def __init__(self, log_callback):
        self.log_callback = log_callback
        self.db_service: Optional[DatabaseService] = None
        self.scheduler_service = SchedulerService(log_callback)
        self.message_helper = MessageHelper()
    
    def validate_connection(self, connection_data: dict) -> bool:
        """Valida la conexión a la base de datos."""
        try:
            self.db_service = DatabaseService(
                connection_data['db_type'],
                connection_data['server'],
                connection_data['username'],
                connection_data['password'],
                connection_data['port']
            )
            
            # Probar conexión con la primera base de datos disponible o una por defecto
            test_database = None
            if connection_data.get('databases'):
                test_database = connection_data['databases'][0]
            
            self.db_service.test_connection(test_database)
            
            self.message_helper.show_success("Validación Exitosa", MESSAGES['connection_success'])
            self.log_callback("Validación de conexión: exitosa.")
            return True
            
        except Exception as e:
            error_msg = MESSAGES['connection_error'].format(e)
            self.message_helper.show_error("Error de Conexión", error_msg)
            self.log_callback(f"Validación de conexión: fallida - {e}")
            return False
    
    def load_databases(self, connection_data: dict) -> list:
        """Carga las bases de datos disponibles desde el servidor."""
        try:
            if not self.db_service:
                # Crear servicio temporal para cargar bases de datos
                temp_service = DatabaseService(
                    connection_data['db_type'],
                    connection_data['server'],
                    connection_data['username'],
                    connection_data['password'],
                    connection_data['port']
                )
            else:
                temp_service = self.db_service
            
            databases = temp_service.get_databases()
            self.log_callback(f"Cargadas {len(databases)} bases de datos del servidor.")
            return databases
            
        except Exception as e:
            self.log_callback(f"Error cargando bases de datos: {e}")
            self.message_helper.show_error("Error", f"No se pudieron cargar las bases de datos: {e}")
            return []
    
    def validate_path(self, path: str) -> bool:
        """Valida la ruta de respaldo con lógica mejorada."""
        if not self.db_service:
            self.message_helper.show_error("Error", "Primero debe validar la conexión a la base de datos.")
            return False
        
        try:
            local_valid, remote_valid = PathValidator.validate_path(self.db_service, path)
            
            # Para bases locales o cuando local es válido, aceptar
            if local_valid:
                if remote_valid:
                    self.message_helper.show_success("Validación Exitosa", "Ruta válida tanto local como remotamente.")
                    self.log_callback(f"✅ Ruta válida: {path} (local y servidor)")
                else:
                    # Solo local válido - permitir para MySQL/PostgreSQL o conexiones locales
                    if self.db_service.db_type in ['mysql', 'postgresql'] or 'localhost' in self.db_service.server.lower():
                        self.message_helper.show_success("Validación Exitosa", "Ruta local válida.")
                        self.log_callback(f"✅ Ruta válida localmente: {path}")
                    else:
                        self.message_helper.show_warning("Advertencia", "Ruta válida localmente pero no verificada en servidor remoto.")
                        self.log_callback(f"⚠️ Ruta válida local pero no remota: {path}")
                return True
            else:
                # Crear la carpeta si no existe
                try:
                    os.makedirs(path, exist_ok=True)
                    if os.path.exists(path) and os.access(path, os.W_OK):
                        self.message_helper.show_success("Ruta Creada", f"Carpeta creada exitosamente: {path}")
                        self.log_callback(f"✅ Carpeta creada: {path}")
                        return True
                except Exception as e:
                    self.log_callback(f"❌ Error creando carpeta: {e}")
                
                self.message_helper.show_error("Error de Ruta", f"No se puede acceder o crear la ruta: {path}")
                self.log_callback(f"❌ Ruta inválida: {path}")
                return False
                
        except Exception as e:
            self.log_callback(f"❌ Error durante validación de ruta: {e}")
            # En caso de error de validación, intentar usar la ruta de todos modos si es local
            if os.path.exists(path) or self._try_create_path(path):
                self.log_callback(f"⚠️ Usando ruta a pesar de error de validación: {path}")
                return True
            return False
    
    def _try_create_path(self, path: str) -> bool:
        """Intenta crear la ruta especificada."""
        try:
            os.makedirs(path, exist_ok=True)
            return os.path.exists(path) and os.access(path, os.W_OK)
        except:
            return False
    
    def create_backup(self, databases: list, backup_path: str) -> None:
        """Ejecuta la tarea de respaldo para múltiples bases de datos."""
        if not self.db_service:
            self.log_callback("❌ Error: No hay conexión a base de datos configurada.")
            return
        
        if not databases:
            self.log_callback("❌ Error: No hay bases de datos seleccionadas para respaldar.")
            return
        
        # Crear carpeta base si no existe
        if not os.path.exists(backup_path):
            try:
                os.makedirs(backup_path, exist_ok=True)
                self.log_callback(f"📁 Carpeta de respaldos creada: {backup_path}")
            except Exception as e:
                self.log_callback(f"❌ Error creando carpeta de respaldos: {e}")
                return
        
        db_type_name = {
            'sql_server': 'SQL Server',
            'mysql': 'MySQL',
            'postgresql': 'PostgreSQL'
        }.get(self.db_service.db_type, 'Desconocido')
        
        self.log_callback(f"🚀 Iniciando respaldos de {len(databases)} base(s) de datos ({db_type_name})")
        self.log_callback(f"📂 Ruta base: {backup_path}")
        
        successful_backups = []
        failed_backups = []
        
        for i, database in enumerate(databases, 1):
            try:
                self.log_callback(f"📦 Respaldando BD {i}/{len(databases)}: {database}...")
                
                fullpath = self.db_service.create_backup(database, backup_path)
                
                # Obtener información del archivo creado
                file_size = os.path.getsize(fullpath) if os.path.exists(fullpath) else 0
                size_mb = file_size / (1024 * 1024)
                
                successful_backups.append(database)
                self.log_callback(f"✅ Respaldo completado: {database}")
                self.log_callback(f"   📁 Archivo: {os.path.basename(fullpath)}")
                self.log_callback(f"   📊 Tamaño: {size_mb:.2f} MB")
                self.log_callback(f"   🗂️ Ubicación: {os.path.dirname(fullpath)}")
                
            except Exception as e:
                failed_backups.append(database)
                error_msg = str(e)
                
                # Mensajes de error más descriptivos
                if 'sin permisos' in error_msg.lower() or 'access denied' in error_msg.lower():
                    self.log_callback(f"❌ Error de permisos para {database}: {error_msg}")
                    self.log_callback(f"   💡 Sugerencia: Verificar permisos de escritura en {backup_path}")
                elif 'no existe' in error_msg.lower() or 'not exist' in error_msg.lower():
                    self.log_callback(f"❌ Base de datos no encontrada: {database}")
                elif 'timeout' in error_msg.lower() or 'tiempo' in error_msg.lower():
                    self.log_callback(f"❌ Timeout en respaldo de {database}: El proceso tardó demasiado")
                else:
                    self.log_callback(f"❌ Error respaldando {database}: {error_msg}")
        
        # Resumen final
        self.log_callback("=" * 50)
        if successful_backups:
            self.log_callback(f"🎉 Respaldos exitosos: {len(successful_backups)} BD(s)")
            for db in successful_backups:
                self.log_callback(f"   ✅ {db}")
        
        if failed_backups:
            self.log_callback(f"💥 Respaldos fallidos: {len(failed_backups)} BD(s)")
            for db in failed_backups:
                self.log_callback(f"   ❌ {db}")
        
        total_msg = f"📊 Total procesado: {len(databases)} BD(s) | Exitosos: {len(successful_backups)} | Fallidos: {len(failed_backups)}"
        self.log_callback(total_msg)
        self.log_callback("=" * 50)
    
    def start_scheduler(self, schedule_config: dict, databases: list, backup_path: str) -> bool:
        """Inicia el programador de respaldos para múltiples bases de datos."""
        if not self.db_service:
            self.log_callback("Error: Debe validar la conexión antes de iniciar el programador.")
            return False
        
        if not databases:
            self.log_callback("Error: Debe seleccionar al menos una base de datos.")
            return False
        
        self.scheduler_service.clear_schedule()
        
        # Crear función de respaldo con las bases de datos y ruta configuradas
        backup_function = lambda: self.create_backup(databases, backup_path)
        
        # Programar según la configuración
        if schedule_config['frequency'] == "diario":
            self.scheduler_service.schedule_daily_backup(schedule_config['time'], backup_function)
        else:
            self.scheduler_service.schedule_interval_backup(
                schedule_config['interval_hours'], backup_function
            )
        
        self.scheduler_service.start()
        return True
    
    def stop_scheduler(self) -> None:
        """Detiene el programador de respaldos."""
        self.scheduler_service.stop()
    
    @property
    def is_scheduler_running(self) -> bool:
        """Indica si el programador está ejecutándose."""
        return self.scheduler_service.is_running
