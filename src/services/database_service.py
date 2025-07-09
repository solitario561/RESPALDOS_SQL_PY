"""
Servicios de base de datos para la aplicación de respaldos.
"""

import pyodbc
import subprocess
import os
from datetime import datetime
from typing import List, Dict, Optional
from config.settings import DATABASE_CONFIG, DB_TYPES


class DatabaseService:
    """Servicio para operaciones de base de datos multi-motor."""
    
    def __init__(self, db_type: str, server: str, username: str, password: str, port: int = None):
        self.db_type = db_type
        self.server = server
        self.username = username
        self.password = password
        self.port = port or self._get_default_port(db_type)
        self.config = DATABASE_CONFIG.get(db_type, {})
    
    def _get_default_port(self, db_type: str) -> int:
        """Obtiene el puerto por defecto según el tipo de base de datos."""
        default_ports = {
            'sql_server': 1433,
            'mysql': 3306,
            'postgresql': 5432
        }
        return default_ports.get(db_type, 1433)
    
    def _get_connection_string(self, database: str = 'master') -> str:
        """Genera la cadena de conexión según el tipo de base de datos."""
        if self.db_type == 'sql_server':
            return (
                f"DRIVER={{{self.config['driver']}}};"
                f"SERVER={self.server},{self.port};"
                f"DATABASE={database};"
                f"UID={self.username};"
                f"PWD={self.password}"
            )
        elif self.db_type == 'mysql':
            return f"mysql+pymysql://{self.username}:{self.password}@{self.server}:{self.port}/{database}"
        elif self.db_type == 'postgresql':
            return f"postgresql+psycopg2://{self.username}:{self.password}@{self.server}:{self.port}/{database}"
        else:
            raise ValueError(f"Tipo de base de datos no soportado: {self.db_type}")
    
    def test_connection(self, database: str = None) -> bool:
        """Prueba la conexión a la base de datos."""
        try:
            if self.db_type == 'sql_server':
                return self._test_sql_server_connection(database or 'master')
            elif self.db_type == 'mysql':
                return self._test_mysql_connection(database or 'information_schema')
            elif self.db_type == 'postgresql':
                return self._test_postgresql_connection(database or 'postgres')
            else:
                raise ValueError(f"Tipo de base de datos no soportado: {self.db_type}")
        except Exception:
            raise
    
    def _test_sql_server_connection(self, database: str) -> bool:
        """Prueba conexión específica para SQL Server."""
        conn_str = self._get_connection_string(database)
        with pyodbc.connect(conn_str, timeout=self.config['timeout']):
            pass
        return True
    
    def _test_mysql_connection(self, database: str) -> bool:
        """Prueba conexión específica para MySQL."""
        try:
            import mysql.connector
            connection = mysql.connector.connect(
                host=self.server,
                port=self.port,
                user=self.username,
                password=self.password,
                database=database,
                connection_timeout=self.config['timeout']
            )
            connection.close()
            return True
        except ImportError:
            raise Exception("MySQL connector no está instalado. Instale: pip install mysql-connector-python")
    
    def _test_postgresql_connection(self, database: str) -> bool:
        """Prueba conexión específica para PostgreSQL."""
        try:
            import psycopg2
            connection = psycopg2.connect(
                host=self.server,
                port=self.port,
                user=self.username,
                password=self.password,
                database=database,
                connect_timeout=self.config['timeout']
            )
            connection.close()
            return True
        except ImportError:
            raise Exception("PostgreSQL connector no está instalado. Instale: pip install psycopg2-binary")
    
    def get_databases(self) -> List[str]:
        """Obtiene la lista de bases de datos disponibles."""
        try:
            if self.db_type == 'sql_server':
                return self._get_sql_server_databases()
            elif self.db_type == 'mysql':
                return self._get_mysql_databases()
            elif self.db_type == 'postgresql':
                return self._get_postgresql_databases()
            else:
                return []
        except Exception:
            raise
    
    def _get_sql_server_databases(self) -> List[str]:
        """Obtiene bases de datos de SQL Server."""
        conn_str = self._get_connection_string('master')
        with pyodbc.connect(conn_str, timeout=self.config['timeout']) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sys.databases WHERE database_id > 4")  # Excluir bases del sistema
            return [row[0] for row in cursor.fetchall()]
    
    def _get_mysql_databases(self) -> List[str]:
        """Obtiene bases de datos de MySQL."""
        import mysql.connector
        connection = mysql.connector.connect(
            host=self.server,
            port=self.port,
            user=self.username,
            password=self.password,
            connection_timeout=self.config['timeout']
        )
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in cursor.fetchall()]
        connection.close()
        # Excluir bases del sistema
        system_dbs = ['information_schema', 'mysql', 'performance_schema', 'sys']
        return [db for db in databases if db not in system_dbs]
    
    def _get_postgresql_databases(self) -> List[str]:
        """Obtiene bases de datos de PostgreSQL."""
        import psycopg2
        connection = psycopg2.connect(
            host=self.server,
            port=self.port,
            user=self.username,
            password=self.password,
            database='postgres',
            connect_timeout=self.config['timeout']
        )
        cursor = connection.cursor()
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
        databases = [row[0] for row in cursor.fetchall()]
        connection.close()
        # Excluir bases del sistema
        system_dbs = ['postgres']
        return [db for db in databases if db not in system_dbs]
    
    def validate_path_on_server(self, path: str) -> bool:
        """Valida si una ruta existe en el servidor."""
        if self.db_type == 'sql_server':
            try:
                conn_str = self._get_connection_string('master')
                with pyodbc.connect(conn_str, timeout=self.config['timeout']) as conn:
                    cursor = conn.cursor()
                    cursor.execute("EXEC master.dbo.xp_fileexist ?", (path,))
                    row = cursor.fetchone()
                    
                    if row:
                        exists = row[0]
                        is_dir = row[1] if len(row) > 1 else 0
                        return exists == 1 or is_dir == 1
                    return False
            except Exception:
                raise
        else:
            # Para MySQL y PostgreSQL, solo validamos localmente
            return os.path.isdir(path) and os.access(path, os.W_OK)
    
    def create_backup(self, database: str, backup_path: str) -> str:
        """Crea un respaldo de la base de datos con organización por tipo de BD."""
        
        # Crear subcarpeta para el tipo de base de datos
        db_type_folder = {
            'sql_server': 'SQL_Server',
            'mysql': 'MySQL', 
            'postgresql': 'PostgreSQL'
        }.get(self.db_type, 'Unknown')
        
        # Crear la ruta completa con subcarpeta
        full_backup_path = os.path.join(backup_path, db_type_folder)
        
        # Crear la carpeta si no existe
        os.makedirs(full_backup_path, exist_ok=True)
        
        # Generar nombre del archivo con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_extension = self.config.get('file_extension', '.bak')
        filename = f"{database}_{timestamp}{file_extension}"
        fullpath = os.path.join(full_backup_path, filename)
        
        try:
            if self.db_type == 'sql_server':
                result_path = self._create_sql_server_backup(database, fullpath)
                print(f"🔧 DEBUG: _create_sql_server_backup retornó: {result_path}")
                return result_path
            elif self.db_type == 'mysql':
                return self._create_mysql_backup(database, fullpath)
            elif self.db_type == 'postgresql':
                return self._create_postgresql_backup(database, fullpath)
            else:
                raise ValueError(f"Tipo de base de datos no soportado: {self.db_type}")
        except Exception as e:
            print(f"🔧 DEBUG: Error en método específico de respaldo: {e}")
            # Si hay error, eliminar archivo parcial si existe
            if os.path.exists(fullpath):
                try:
                    os.remove(fullpath)
                except:
                    pass
            raise Exception(f"Error creando respaldo de {database}: {str(e)}")
        
        # Esta parte nunca debería ejecutarse porque los métodos específicos ya hacen return
        print(f"🔧 DEBUG: ⚠️ Código después del return - esto no debería ejecutarse")
        
        # Verificar que el archivo se creó correctamente
        print(f"🔧 DEBUG: Verificando existencia del archivo: {fullpath}")
        if not os.path.exists(fullpath):
            print(f"🔧 DEBUG: ❌ Archivo no existe")
            raise Exception(f"El archivo de respaldo no se creó: {fullpath}")
        else:
            print(f"🔧 DEBUG: ✅ Archivo existe")
            
        # Verificar que el archivo no esté vacío
        file_size = os.path.getsize(fullpath)
        print(f"🔧 DEBUG: Tamaño del archivo: {file_size} bytes")
        if file_size == 0:
            print(f"🔧 DEBUG: ❌ Archivo está vacío, eliminando...")
            os.remove(fullpath)
            raise Exception(f"El archivo de respaldo está vacío: {fullpath}")
        else:
            print(f"🔧 DEBUG: ✅ Archivo tiene contenido válido")
            
        return fullpath
    
    def _create_sql_server_backup(self, database: str, fullpath: str) -> str:
        """Crea respaldo específico para SQL Server."""
        try:
            # Debug: mostrar información del respaldo
            print(f"🔧 DEBUG: Iniciando respaldo SQL Server")
            print(f"   Base de datos: {database}")
            print(f"   Ruta destino: {fullpath}")
            print(f"   Directorio: {os.path.dirname(fullpath)}")
            
            # Verificar que el directorio existe
            dir_path = os.path.dirname(fullpath)
            if not os.path.exists(dir_path):
                print(f"🔧 DEBUG: Creando directorio: {dir_path}")
                os.makedirs(dir_path, exist_ok=True)
            
            conn_str = self._get_connection_string(database)
            print(f"🔧 DEBUG: Cadena de conexión configurada")
            
            with pyodbc.connect(conn_str, autocommit=True, timeout=300) as conn:
                cursor = conn.cursor()
                # Escapar comillas en el path
                safe_path = fullpath.replace("'", "''")
                backup_query = f"BACKUP DATABASE [{database}] TO DISK = N'{safe_path}' WITH INIT, COMPRESSION;"
                
                print(f"🔧 DEBUG: Ejecutando comando SQL:")
                print(f"   {backup_query}")
                
                cursor.execute(backup_query)
                print(f"🔧 DEBUG: Comando SQL ejecutado sin errores")
                
            # Verificar que el archivo se creó
            print(f"🔧 DEBUG: Verificando archivo creado...")
            
            # Pequeño delay para asegurar que SQL Server termine
            import time
            time.sleep(1)
            
            if os.path.exists(fullpath):
                file_size = os.path.getsize(fullpath)
                print(f"🔧 DEBUG: ✅ Archivo encontrado, tamaño: {file_size} bytes")
                
                # Verificar permisos del archivo
                try:
                    with open(fullpath, 'rb') as f:
                        f.read(1)  # Intentar leer 1 byte
                    print(f"🔧 DEBUG: ✅ Archivo accesible para lectura")
                except Exception as e:
                    print(f"🔧 DEBUG: ⚠️ Problema accediendo al archivo: {e}")
                
                return fullpath
            else:
                print(f"🔧 DEBUG: ❌ Archivo no encontrado en: {fullpath}")
                
                # Listar archivos en el directorio para debug
                try:
                    dir_files = os.listdir(dir_path)
                    print(f"🔧 DEBUG: Archivos en directorio {dir_path}:")
                    for f in dir_files:
                        print(f"🔧 DEBUG:   - {f}")
                    
                    # Buscar archivos similares
                    base_name = os.path.basename(fullpath)
                    similar_files = [f for f in dir_files if database in f and '.bak' in f]
                    if similar_files:
                        print(f"🔧 DEBUG: Archivos similares encontrados: {similar_files}")
                        # Usar el archivo más reciente si existe
                        latest_file = max(similar_files, key=lambda x: os.path.getctime(os.path.join(dir_path, x)))
                        latest_path = os.path.join(dir_path, latest_file)
                        print(f"🔧 DEBUG: Usando archivo más reciente: {latest_path}")
                        return latest_path
                        
                except Exception as e:
                    print(f"🔧 DEBUG: Error listando directorio: {e}")
                
                raise Exception(f"El archivo de respaldo no se generó en: {fullpath}")
                
        except pyodbc.Error as e:
            error_msg = str(e)
            print(f"🔧 DEBUG: Error de pyodbc: {error_msg}")
            if 'operating system error 5' in error_msg.lower():
                raise Exception(f"Sin permisos para escribir en: {fullpath}")
            elif 'operating system error 3' in error_msg.lower():
                raise Exception(f"La ruta no existe: {os.path.dirname(fullpath)}")
            else:
                raise Exception(f"Error de SQL Server: {error_msg}")
        except Exception as e:
            print(f"🔧 DEBUG: Error general: {str(e)}")
            raise Exception(f"Error creando respaldo SQL Server: {str(e)}")
    
    def _create_mysql_backup(self, database: str, fullpath: str) -> str:
        """Crea respaldo específico para MySQL."""
        try:
            # Verificar que mysqldump está disponible
            check_cmd = ['mysqldump', '--version']
            result = subprocess.run(check_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("mysqldump no está disponible. Instale MySQL client tools.")
            
            cmd = [
                'mysqldump',
                f'--host={self.server}',
                f'--port={self.port}',
                f'--user={self.username}',
                f'--password={self.password}',
                '--single-transaction',
                '--routines',
                '--triggers',
                '--lock-tables=false',
                '--set-gtid-purged=OFF',
                database
            ]
            
            # Crear el directorio si no existe
            os.makedirs(os.path.dirname(fullpath), exist_ok=True)
            
            with open(fullpath, 'w', encoding='utf-8') as f:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True, timeout=300)
                if result.returncode != 0:
                    stderr_output = result.stderr
                    if 'Access denied' in stderr_output:
                        raise Exception("Credenciales incorrectas o sin permisos")
                    elif 'Unknown database' in stderr_output:
                        raise Exception(f"La base de datos '{database}' no existe")
                    else:
                        raise Exception(f"Error en mysqldump: {stderr_output}")
            
            # Verificar que el archivo se creó y no está vacío
            if not os.path.exists(fullpath) or os.path.getsize(fullpath) == 0:
                raise Exception("El respaldo está vacío o no se generó")
                
            return fullpath
            
        except subprocess.TimeoutExpired:
            raise Exception("El respaldo excedió el tiempo límite (5 minutos)")
        except Exception as e:
            if os.path.exists(fullpath):
                try:
                    os.remove(fullpath)
                except:
                    pass
            raise Exception(f"Error creando respaldo MySQL: {str(e)}")
    
    def _create_postgresql_backup(self, database: str, fullpath: str) -> str:
        """Crea respaldo específico para PostgreSQL."""
        try:
            # Verificar que pg_dump está disponible
            check_cmd = ['pg_dump', '--version']
            result = subprocess.run(check_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("pg_dump no está disponible. Instale PostgreSQL client tools.")
            
            # Configurar variables de entorno para PostgreSQL
            env = os.environ.copy()
            env['PGPASSWORD'] = self.password
            
            cmd = [
                'pg_dump',
                f'--host={self.server}',
                f'--port={self.port}',
                f'--username={self.username}',
                '--format=custom',
                '--no-password',
                '--verbose',
                '--compress=6',
                database
            ]
            
            # Crear el directorio si no existe
            os.makedirs(os.path.dirname(fullpath), exist_ok=True)
            
            with open(fullpath, 'wb') as f:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, env=env, timeout=300)
                if result.returncode != 0:
                    stderr_output = result.stderr.decode()
                    if 'authentication failed' in stderr_output.lower():
                        raise Exception("Credenciales incorrectas")
                    elif 'does not exist' in stderr_output.lower():
                        raise Exception(f"La base de datos '{database}' no existe")
                    else:
                        raise Exception(f"Error en pg_dump: {stderr_output}")
            
            # Verificar que el archivo se creó y no está vacío
            if not os.path.exists(fullpath) or os.path.getsize(fullpath) == 0:
                raise Exception("El respaldo está vacío o no se generó")
                
            return fullpath
            
        except subprocess.TimeoutExpired:
            raise Exception("El respaldo excedió el tiempo límite (5 minutos)")
        except Exception as e:
            if os.path.exists(fullpath):
                try:
                    os.remove(fullpath)
                except:
                    pass
            raise Exception(f"Error creando respaldo PostgreSQL: {str(e)}")
    


class PathValidator:
    """Validador de rutas locales y remotas."""
    
    @staticmethod
    def validate_local_path(path: str) -> bool:
        """Valida si una ruta local existe y tiene permisos de escritura."""
        return os.path.isdir(path) and os.access(path, os.W_OK)
    
    @staticmethod
    def validate_remote_path(db_service: DatabaseService, path: str) -> bool:
        """Valida si una ruta existe en el servidor remoto."""
        try:
            return db_service.validate_path_on_server(path)
        except Exception:
            return False
    
    @classmethod
    def validate_path(cls, db_service: DatabaseService, path: str) -> tuple[bool, bool]:
        """Valida una ruta tanto local como remotamente."""
        local_valid = cls.validate_local_path(path)
        remote_valid = cls.validate_remote_path(db_service, path)
        return local_valid, remote_valid
