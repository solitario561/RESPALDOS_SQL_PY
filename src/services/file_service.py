"""
Servicio para manejo de archivos de logs y historial de conexiones.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from config.settings import FILE_CONFIG


class FileService:
    """Servicio para manejo de archivos de la aplicación."""
    
    @staticmethod
    def save_logs_to_file(logs_content: str) -> bool:
        """Guarda los logs en un archivo."""
        try:
            with open(FILE_CONFIG['logs_file'], 'w', encoding='utf-8') as f:
                f.write(logs_content)
            return True
        except Exception:
            return False
    
    @staticmethod
    def load_logs_from_file() -> str:
        """Carga los logs desde el archivo."""
        try:
            if os.path.exists(FILE_CONFIG['logs_file']):
                with open(FILE_CONFIG['logs_file'], 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Limitar el número de líneas para evitar archivos muy grandes
                    lines = content.split('\n')
                    if len(lines) > FILE_CONFIG['max_log_lines']:
                        lines = lines[-FILE_CONFIG['max_log_lines']:]
                        content = '\n'.join(lines)
                        # Guardar la versión truncada
                        FileService.save_logs_to_file(content)
                    return content
            return ""
        except Exception:
            return ""
    
    @staticmethod
    def clear_logs_file() -> bool:
        """Limpia el archivo de logs."""
        try:
            if os.path.exists(FILE_CONFIG['logs_file']):
                os.remove(FILE_CONFIG['logs_file'])
            return True
        except Exception:
            return False


class ConnectionHistoryService:
    """Servicio para manejo del historial de conexiones."""
    
    @staticmethod
    def load_connections_history() -> List[Dict[str, str]]:
        """Carga el historial de conexiones desde el archivo."""
        try:
            if os.path.exists(FILE_CONFIG['connections_file']):
                with open(FILE_CONFIG['connections_file'], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('connections', [])
            return []
        except Exception:
            return []
    
    @staticmethod
    def save_connection(db_type: str, server: str, port: int, databases: List[str]) -> bool:
        """Guarda una nueva conexión al historial."""
        if not server:
            return False
        
        # Si no hay bases de datos, usar una lista vacía (conexión validada sin BDs específicas)
        if not databases:
            databases = []
        
        try:
            connections = ConnectionHistoryService.load_connections_history()
            
            # Crear nueva conexión
            new_connection = {
                'db_type': db_type,
                'server': server,
                'port': port,
                'databases': databases,
                'last_used': datetime.now().isoformat()
            }
            
            # Remover duplicados (mismo tipo, servidor y puerto)
            connections = [
                conn for conn in connections 
                if not (conn.get('db_type') == db_type and 
                       conn.get('server') == server and 
                       conn.get('port') == port)
            ]
            
            # Agregar la nueva conexión al inicio
            connections.insert(0, new_connection)
            
            # Mantener solo las últimas N conexiones
            connections = connections[:FILE_CONFIG['max_connections_history']]
            
            # Guardar al archivo
            data = {'connections': connections}
            with open(FILE_CONFIG['connections_file'], 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_connection_display_list() -> List[str]:
        """Obtiene una lista formateada para mostrar en combobox."""
        connections = ConnectionHistoryService.load_connections_history()
        display_list = []
        
        for conn in connections:
            db_type = conn.get('db_type', 'sql_server')
            # Convertir clave interna a nombre para mostrar
            type_display = {
                'sql_server': 'SQL Server',
                'mysql': 'MySQL', 
                'postgresql': 'PostgreSQL'
            }.get(db_type, 'SQL Server')
            
            server = conn.get('server', '')
            port = conn.get('port', 1433)
            databases = conn.get('databases', [])
            
            if server:
                if databases and databases != ["(conexión validada)"]:
                    db_count = len(databases)
                    display_text = f"{type_display} | {server}:{port} | {db_count} BD(s)"
                else:
                    display_text = f"{type_display} | {server}:{port} | Sin BDs específicas"
                display_list.append(display_text)
        
        return display_list
    
    @staticmethod
    def parse_connection_string(connection_string: str) -> tuple[str, str, int, List[str]]:
        """Parsea una cadena de conexión del formato 'tipo | servidor:puerto | X BD(s)'."""
        try:
            parts = connection_string.split(' | ')
            if len(parts) >= 3:
                db_type_display = parts[0].strip()
                server_port = parts[1].strip()
                
                # Convertir nombre de display a clave interna
                db_type_key = {
                    'SQL Server': 'sql_server',
                    'MySQL': 'mysql',
                    'PostgreSQL': 'postgresql'
                }.get(db_type_display, 'sql_server')
                
                # Parsear servidor y puerto
                if ':' in server_port:
                    server, port_str = server_port.split(':')
                    port = int(port_str)
                else:
                    server = server_port
                    port = 1433  # Puerto por defecto
                
                # Buscar la conexión completa en el historial para obtener las bases de datos
                connections = ConnectionHistoryService.load_connections_history()
                for conn in connections:
                    if (conn.get('db_type') == db_type_key and 
                        conn.get('server') == server and 
                        conn.get('port') == port):
                        databases = conn.get('databases', [])
                        return db_type_display, server, port, databases
                
                return db_type_display, server, port, []
            return "", "", 0, []
        except Exception:
            return "", "", 0, []
    
    @staticmethod
    def clear_connections_history() -> bool:
        """Limpia todo el historial de conexiones."""
        try:
            if os.path.exists(FILE_CONFIG['connections_file']):
                os.remove(FILE_CONFIG['connections_file'])
            return True
        except Exception:
            return False
