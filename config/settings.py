"""
Configuración y constantes de la aplicación.
"""

# Configuración de la base de datos
DATABASE_CONFIG = {
    'sql_server': {
        'driver': 'ODBC Driver 17 for SQL Server',
        'timeout': 5,
        'backup_command': 'BACKUP DATABASE [{database}] TO DISK = N\'{path}\' WITH INIT;',
        'test_query': 'SELECT 1',
        'file_extension': '.bak'
    },
    'mysql': {
        'driver': 'mysql+pymysql',
        'timeout': 5,
        'backup_command': 'mysqldump --host={host} --user={user} --password={password} {database}',
        'test_query': 'SELECT 1',
        'file_extension': '.sql'
    },
    'postgresql': {
        'driver': 'postgresql+psycopg2',
        'timeout': 5,
        'backup_command': 'pg_dump --host={host} --username={user} --dbname={database}',
        'test_query': 'SELECT 1',
        'file_extension': '.sql'
    }
}

# Tipos de base de datos soportados
DB_TYPES = {
    'SQL Server': 'sql_server',
    'MySQL': 'mysql',
    'PostgreSQL': 'postgresql'
}

# Configuración de la UI
UI_CONFIG = {
    'window_title': '🗃️ Configurador de Respaldos Multi-BD',
    'window_size': '1200x900',  # Ventana más grande para mostrar todo
    'window_min_size': (1000, 800),
    'entry_width': 30,
    'spinbox_width': 5,
    'log_height': 8,  # Logs más pequeños para dar espacio a configuración
    'combobox_width': 28,
    
    # Colores del tema
    'colors': {
        'primary': '#2E86AB',      # Azul principal
        'secondary': '#A23B72',    # Rosa secundario
        'accent': '#F18F01',       # Naranja acento
        'success': '#28A745',      # Verde éxito
        'warning': '#FFC107',      # Amarillo advertencia
        'error': '#DC3545',        # Rojo error
        'background': '#F8F9FA',   # Fondo claro
        'surface': '#FFFFFF',      # Superficie blanca
        'text': '#212529',         # Texto oscuro
        'text_secondary': '#6C757D', # Texto secundario
        'border': '#DEE2E6'        # Borde gris claro
    },
    
    # Fuentes
    'fonts': {
        'title': ('Segoe UI', 14, 'bold'),
        'subtitle': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'small': ('Segoe UI', 9),
        'button': ('Segoe UI', 10, 'bold')
    },
    
    # Espaciado y dimensiones
    'padding': {
        'small': 5,
        'medium': 10,
        'large': 15,
        'xlarge': 20
    },
    
    # Estilos de widgets
    'styles': {
        'frame_relief': 'flat',
        'frame_border': 1,
        'button_relief': 'flat',
        'entry_relief': 'flat',
        'listbox_relief': 'flat'
    }
}

# Configuración de respaldos
BACKUP_CONFIG = {
    'frequency_options': ['diario', 'cada X horas'],
    'default_frequency': 'diario',
    'default_time': '00:00',
    'min_interval_hours': 1,
    'max_interval_hours': 24
}

# Configuración de archivos
FILE_CONFIG = {
    'logs_file': 'data/backup_logs.txt',
    'connections_file': 'data/connections_history.json',
    'max_log_lines': 1000,
    'max_connections_history': 10
}

# Mensajes de la aplicación
MESSAGES = {
    'connection_success': 'Conexión exitosa.',
    'connection_error': 'No se pudo conectar: {}',
    'path_validation_success': 'La ruta existe local y en servidor, y tiene permisos.',
    'path_validation_error': 'Error de Ruta',
    'backup_completed': 'Respaldo completado: {}',
    'backup_error': 'Error en respaldo: {}',
    'access_denied': 'Error en respaldo: Acceso denegado en el servidor. Asegúrate de que la cuenta de servicio SQL Server tenga permisos en \'{}\'.',
    'scheduler_started': 'Proceso de respaldos iniciado.',
    'scheduler_stopped': 'Proceso de respaldos detenido.',
    'daily_scheduled': 'Programado respaldo diario a las {}',
    'interval_scheduled': 'Programado respaldo cada {} horas'
}
