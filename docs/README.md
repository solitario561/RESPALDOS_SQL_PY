# Configurador de Respaldos SQL Server

Una aplicación de escritorio desarrollada en Python con Tkinter para automatizar y programar respaldos de bases de datos SQL Server.

## Características

- **Interfaz gráfica intuitiva**: Fácil configuración de conexiones y programación
- **Historial de conexiones**: Guarda automáticamente servidor y base de datos (sin credenciales)
- **Validación de conexión**: Verifica la conectividad con SQL Server antes de iniciar
- **Validación de rutas**: Comprueba que las rutas de respaldo existan y tengan permisos
- **Programación flexible**: Respaldos diarios a una hora específica o cada X horas
- **Logs persistentes**: Los logs se guardan automáticamente y persisten entre sesiones
- **Gestión de logs**: Opciones para limpiar, guardar y exportar logs
- **Logs en tiempo real**: Monitoreo de todas las actividades y errores
- **Arquitectura modular**: Código organizado siguiendo principios de Clean Code

## Estructura del Proyecto

```
Respaldos_sql_py/
├── src/                    # Código fuente principal
│   ├── main.py            # Aplicación principal
│   ├── core/              # Lógica de negocio central
│   │   └── backup_controller.py
│   ├── services/          # Servicios de la aplicación
│   │   ├── database_service.py
│   │   ├── file_service.py
│   │   └── scheduler_service.py
│   └── ui/                # Componentes de interfaz
│       └── ui_components.py
├── config/                # Configuraciones
│   └── settings.py
├── data/                  # Datos de la aplicación
│   ├── backup_logs.txt
│   └── connections_history.json
├── tests/                 # Pruebas y scripts de validación
│   ├── test_app.py
│   ├── demo_app.py
│   └── check_implementation.py
├── docs/                  # Documentación
│   ├── README.md
│   ├── IMPLEMENTACION_COMPLETADA.txt
│   └── REPORTE_PRUEBAS.txt
├── run_app.py            # Script principal de ejecución
└── requirements.txt      # Dependencias del proyecto
```

## Requisitos

- Python 3.7+
- SQL Server con ODBC Driver 17
- Permisos de conexión a SQL Server
- Permisos de escritura en las rutas de respaldo

## Instalación

1. Clona o descarga el proyecto
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Asegúrate de tener el ODBC Driver 17 for SQL Server instalado

## Uso

1. Ejecuta la aplicación:
   ```bash
   python run_app.py
   ```

2. Configura la conexión:
   - Servidor SQL Server
   - Base de datos
   - Usuario y contraseña
   - Ruta de respaldo (debe existir en el servidor)

3. Valida la conexión y la ruta usando los botones correspondientes

4. Configura la programación:
   - **Diario**: Especifica una hora (formato HH:MM)
   - **Cada X horas**: Especifica el intervalo en horas

5. Inicia el proceso de respaldos automáticos

## Arquitectura

El proyecto sigue principios de Clean Code y arquitectura modular:

### Separación de Responsabilidades

- **UI Components**: Manejo de la interfaz de usuario
- **Database Service**: Operaciones de base de datos y validaciones
- **Scheduler Service**: Programación y ejecución de tareas
- **Backup Controller**: Lógica de negocio principal
- **Config**: Configuraciones centralizadas

### Principios Aplicados

- **Single Responsibility Principle**: Cada clase tiene una responsabilidad específica
- **Dependency Injection**: Los servicios se inyectan en lugar de crear dependencias internas
- **Configuración centralizada**: Todas las constantes en un archivo de configuración
- **Manejo de errores consistente**: Logging y manejo de excepciones estandarizado

## Funcionalidades Técnicas

### Validación de Conexión
- Prueba la conectividad con SQL Server usando pyodbc
- Timeout configurable para evitar bloqueos

### Validación de Rutas
- Verifica existencia local de la ruta
- Usa `xp_fileexist` para validar rutas en el servidor SQL
- Comprueba permisos de escritura

### Programación de Respaldos
- Usa la librería `schedule` para programación
- Soporte para múltiples patrones de programación
- Ejecución en hilo separado para no bloquear la UI

### Generación de Respaldos
- Nombres de archivo con timestamp único
- Comando `BACKUP DATABASE` nativo de SQL Server
- Manejo específico de errores comunes (permisos, espacio en disco, etc.)

### Gestión de Logs
- **Persistencia automática**: Los logs se guardan automáticamente al generar cada entrada
- **Carga de historial**: Al iniciar la aplicación, se cargan los logs de sesiones anteriores
- **Limpieza de logs**: Opción para limpiar tanto la pantalla como el archivo de logs
- **Exportación**: Posibilidad de exportar logs a archivos con timestamp único
- **Límite de tamaño**: Automáticamente mantiene un límite máximo de líneas para evitar archivos muy grandes

### Historial de Conexiones
- **Guardado automático**: Al validar exitosamente una conexión, se guarda servidor y base de datos
- **Seguridad**: Solo guarda información no sensible (no usuarios ni contraseñas)
- **Selección rápida**: Dropdown con conexiones anteriores para uso rápido
- **Gestión de historial**: Opción para limpiar todo el historial de conexiones
- **Límite configurable**: Mantiene solo las últimas N conexiones configurables

## Troubleshooting

### Error de Conexión
- Verifica que el servidor SQL esté accesible
- Comprueba credenciales de usuario
- Asegúrate de que el ODBC Driver 17 esté instalado

### Error de Ruta
- La ruta debe existir en el servidor SQL Server
- La cuenta de servicio SQL Server debe tener permisos de escritura
- Usa rutas UNC (\\servidor\carpeta) para servidores remotos

### Error de Respaldo
- Verifica espacio disponible en el destino
- Comprueba que la base de datos esté online
- Asegúrate de que no haya respaldos en ejecución

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
