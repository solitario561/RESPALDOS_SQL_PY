"""
Aplicación principal para configuración y programación de respaldos de SQL Server.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from src.core.backup_controller import BackupController
from src.ui.ui_components import (
    ConnectionFrame, 
    ScheduleFrame, 
    ControlButtonsFrame, 
    LogFrame
)
from config.settings import UI_CONFIG


class BackupApp:
    """Aplicación principal para respaldos de SQL Server."""
    
    def __init__(self, root):
        self.root = root
        self._setup_window()
        self._setup_styles()
        
        # Inicializar el controlador
        self.controller = BackupController(self._log_message)
        
        # Crear componentes de la UI
        self._create_ui_components()
        self._setup_layout()
    
    def _setup_window(self):
        """Configura la ventana principal con diseño moderno."""
        self.root.title(UI_CONFIG['window_title'])
        self.root.geometry(UI_CONFIG['window_size'])
        self.root.minsize(*UI_CONFIG['window_min_size'])
        
        # Configurar el fondo
        self.root.configure(bg=UI_CONFIG['colors']['background'])
        
        # Centrar la ventana en la pantalla
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1200x900+{x}+{y}")  # Forzar tamaño específico
    
    def _setup_styles(self):
        """Configura los estilos modernos para ttk widgets."""
        style = ttk.Style()
        
        # Configurar tema base
        style.theme_use('clam')
        
        # Estilos para LabelFrame
        style.configure(
            'Modern.TLabelframe',
            background=UI_CONFIG['colors']['surface'],
            borderwidth=1,
            relief='solid',
            fieldbackground=UI_CONFIG['colors']['surface']
        )
        
        style.configure(
            'Modern.TLabelframe.Label',
            background=UI_CONFIG['colors']['surface'],
            foreground=UI_CONFIG['colors']['primary'],
            font=UI_CONFIG['fonts']['subtitle']
        )
        
        # Estilos para Entry
        style.configure(
            'Modern.TEntry',
            fieldbackground=UI_CONFIG['colors']['surface'],
            borderwidth=1,
            relief='solid',
            padding=UI_CONFIG['padding']['small']
        )
        
        # Estilos para Combobox
        style.configure(
            'Modern.TCombobox',
            fieldbackground=UI_CONFIG['colors']['surface'],
            borderwidth=1,
            relief='solid',
            padding=UI_CONFIG['padding']['small']
        )
        
        # Estilos para Button
        style.configure(
            'Primary.TButton',
            background=UI_CONFIG['colors']['primary'],
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            font=UI_CONFIG['fonts']['button'],
            padding=(UI_CONFIG['padding']['medium'], UI_CONFIG['padding']['small'])
        )
        
        style.map(
            'Primary.TButton',
            background=[('active', '#1F5F85'), ('pressed', '#0F4F75')]
        )
        
        style.configure(
            'Success.TButton',
            background=UI_CONFIG['colors']['success'],
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            font=UI_CONFIG['fonts']['button'],
            padding=(UI_CONFIG['padding']['medium'], UI_CONFIG['padding']['small'])
        )
        
        style.map(
            'Success.TButton',
            background=[('active', '#1E7E34'), ('pressed', '#155724')]
        )
        
        style.configure(
            'Warning.TButton',
            background=UI_CONFIG['colors']['warning'],
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            font=UI_CONFIG['fonts']['button'],
            padding=(UI_CONFIG['padding']['medium'], UI_CONFIG['padding']['small'])
        )
        
        style.map(
            'Warning.TButton',
            background=[('active', '#E0A800'), ('pressed', '#D39E00')]
        )
        
        style.configure(
            'Error.TButton',
            background=UI_CONFIG['colors']['error'],
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            font=UI_CONFIG['fonts']['button'],
            padding=(UI_CONFIG['padding']['medium'], UI_CONFIG['padding']['small'])
        )
        
        style.map(
            'Error.TButton',
            background=[('active', '#BD2130'), ('pressed', '#A71E2A')]
        )
    
    def _create_ui_components(self):
        """Crea todos los componentes de la interfaz de usuario."""
        # Frame de conexión (ahora incluye programación)
        self.connection_frame = ConnectionFrame(
            self.root,
            self._validate_connection,
            self._validate_path,
            self._load_databases
        )
        
        # Frame de botones de control
        self.control_frame = ControlButtonsFrame(
            self.root,
            self._start_backup_process,
            self._stop_backup_process
        )
        
        # Frame de logs
        self.log_frame = LogFrame(self.root)
    
    def _setup_layout(self):
        """Configura el layout básico y garantizado para mostrar contenido."""
        
        # Configurar el fondo de la ventana principal
        self.root.configure(bg=UI_CONFIG['colors']['background'])
        
        # Frame de conexión - posicionamiento directo
        self.connection_frame.frame.pack(
            fill='x', 
            padx=15, 
            pady=15
        )
        
        # Frame de botones de control
        self.control_frame.frame.pack(
            pady=10
        )
        
        # Frame de logs
        self.log_frame.frame.pack(
            fill='both', 
            expand=True,
            padx=15, 
            pady=(0, 15)
        )
        
        # Configurar el manejo de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _log_message(self, message: str):
        """Callback para agregar mensajes al log."""
        self.log_frame.add_log(message)
    
    def _validate_connection(self):
        """Valida la conexión a la base de datos."""
        connection_data = self.connection_frame.get_connection_data()
        self.controller.validate_connection(connection_data)
    
    def _validate_path(self):
        """Valida la ruta de respaldo."""
        connection_data = self.connection_frame.get_connection_data()
        self.controller.validate_path(connection_data['backup_path'])
    
    def _start_backup_process(self):
        """Inicia el proceso de respaldos programados."""
        if self.controller.is_scheduler_running:
            return
        
        connection_data = self.connection_frame.get_connection_data()
        schedule_config = self.connection_frame.get_schedule_data()
        
        # Validar que tengamos los datos necesarios
        if not all([connection_data['server'], connection_data['databases'], 
                   connection_data['username'], connection_data['backup_path']]):
            self._log_message("Error: Complete todos los campos de configuración y seleccione al menos una base de datos.")
            return
        
        success = self.controller.start_scheduler(schedule_config, connection_data['databases'], connection_data['backup_path'])
        if success:
            self.control_frame.set_running_state(True)
    
    def _stop_backup_process(self):
        """Detiene el proceso de respaldos programados."""
        if not self.controller.is_scheduler_running:
            return
        
        self.controller.stop_scheduler()
        self.control_frame.set_running_state(False)
    
    def _on_closing(self):
        """Maneja el cierre de la aplicación."""
        # Detener el programador si está ejecutándose
        if self.controller.is_scheduler_running:
            self.controller.stop_scheduler()
        
        # Guardar logs finales
        self._log_message("Aplicación cerrada")
        
        # Cerrar la ventana
        self.root.destroy()
    
    def _load_databases(self, connection_data: dict):
        """Carga las bases de datos disponibles desde el servidor."""
        databases = self.controller.load_databases(connection_data)
        self.connection_frame.set_available_databases(databases)

def main():
    """Función principal para ejecutar la aplicación."""
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
