"""
Script para migrar el historial de conexiones al nuevo formato.
"""

import json
import os
from datetime import datetime

def migrate_connection_history():
    """Migra el historial de conexiones al nuevo formato."""
    history_file = "data/connections_history.json"
    
    if not os.path.exists(history_file):
        print("No hay archivo de historial para migrar.")
        return
    
    try:
        # Leer el archivo actual
        with open(history_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        connections = data.get('connections', [])
        migrated_connections = []
        
        print(f"Migrando {len(connections)} conexiones...")
        
        for conn in connections:
            # Formato antiguo -> nuevo formato
            migrated_conn = {
                'db_type': 'sql_server',  # Asumir SQL Server por defecto
                'server': conn.get('server', ''),
                'port': 1433,  # Puerto por defecto
                'databases': [conn.get('database', '')] if conn.get('database') else [],
                'last_used': conn.get('last_used', datetime.now().isoformat())
            }
            
            if migrated_conn['server'] and migrated_conn['databases']:
                migrated_connections.append(migrated_conn)
                print(f"✓ Migrada conexión: {migrated_conn['server']} -> {migrated_conn['databases']}")
        
        # Crear respaldo del archivo original
        backup_file = f"{history_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(history_file, backup_file)
        print(f"✓ Respaldo creado: {backup_file}")
        
        # Guardar el nuevo formato
        new_data = {'connections': migrated_connections}
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Migración completada. {len(migrated_connections)} conexiones migradas.")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")

if __name__ == "__main__":
    migrate_connection_history()
