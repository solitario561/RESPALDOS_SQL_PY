"""
Componentes de la interfaz de usuario para la aplicación de respaldos.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
from typing import Callable, Optional
from config.settings import UI_CONFIG, BACKUP_CONFIG, DB_TYPES
from src.services.file_service import FileService, ConnectionHistoryService
from src.utils.db_tools_checker import show_database_status_dialog
from src.utils.db_tools_checker import show_database_status_dialog


class ConnectionFrame:
    """Frame para configuración de conexión a la base de datos."""
    
    def __init__(self, parent, validate_connection_callback: Callable, validate_path_callback: Callable, 
                 load_databases_callback: Callable):
        self.frame = ttk.LabelFrame(
            parent, 
            text="🔗 Configuración de Conexión y Programación",
            style='Modern.TLabelframe'
        )
        self.validate_connection_callback = validate_connection_callback
        self.validate_path_callback = validate_path_callback
        self.load_databases_callback = load_databases_callback
        
        # Variables de control
        self.db_type_var = tk.StringVar(value=list(DB_TYPES.keys())[0])
        self.server_var = tk.StringVar()
        self.port_var = tk.StringVar(value="1433")
        self.user_var = tk.StringVar()
        self.pwd_var = tk.StringVar()
        self.path_var = tk.StringVar()
        self.connection_history_var = tk.StringVar()
        
        # Variables para bases de datos múltiples
        self.available_databases = []
        self.selected_databases = []
        
        self._create_widgets()
        self._load_connection_history()
        self._on_db_type_change()
    
    def _create_widgets(self):
        """Crea los widgets del frame con diseño moderno."""
        # Configurar padding del frame
        self.frame.configure(padding=UI_CONFIG['padding']['large'])
        
        current_row = 0
        
        # Historial de conexiones con icono
        header_frame = tk.Frame(self.frame, bg=UI_CONFIG['colors']['surface'])
        header_frame.grid(column=0, row=current_row, columnspan=3, sticky="ew", pady=(0, UI_CONFIG['padding']['medium']))
        
        ttk.Label(
            header_frame, 
            text="📚 Conexiones anteriores:",
            font=UI_CONFIG['fonts']['body'],
            background=UI_CONFIG['colors']['surface']
        ).grid(column=0, row=0, sticky="w")
        
        self.history_combo = ttk.Combobox(
            header_frame, 
            textvariable=self.connection_history_var, 
            width=UI_CONFIG['combobox_width'], 
            state="readonly",
            style='Modern.TCombobox'
        )
        self.history_combo.grid(column=1, row=0, sticky="ew", padx=(UI_CONFIG['padding']['medium'], 0))
        self.history_combo.bind("<<ComboboxSelected>>", self._on_history_selected)
        
        header_frame.grid_columnconfigure(1, weight=1)
        current_row += 1
        
        # Crear separador visual
        separator = ttk.Separator(self.frame, orient='horizontal')
        separator.grid(column=0, row=current_row, columnspan=3, sticky="ew", pady=UI_CONFIG['padding']['medium'])
        current_row += 1
        
        # Sección de configuración de conexión
        conn_label = tk.Label(
            self.frame, 
            text="⚙️ Configuración de Conexión",
            font=UI_CONFIG['fonts']['subtitle'],
            bg=UI_CONFIG['colors']['surface'],
            fg=UI_CONFIG['colors']['primary']
        )
        conn_label.grid(column=0, row=current_row, columnspan=3, sticky="w", pady=(0, UI_CONFIG['padding']['medium']))
        current_row += 1
        
        # Frame para organizar campos de conexión
        conn_frame = tk.Frame(self.frame, bg=UI_CONFIG['colors']['surface'])
        conn_frame.grid(column=0, row=current_row, columnspan=3, sticky="ew", pady=(0, UI_CONFIG['padding']['medium']))
        
        # Tipo de Base de Datos con validación
        ttk.Label(
            conn_frame, 
            text="🗄️ Tipo de BD:",
            font=UI_CONFIG['fonts']['body'],
            background=UI_CONFIG['colors']['surface']
        ).grid(column=0, row=0, sticky="w", padx=(0, UI_CONFIG['padding']['small']))
        
        # Frame para combo + botón de estado
        db_type_frame = tk.Frame(conn_frame, bg=UI_CONFIG['colors']['surface'])
        db_type_frame.grid(column=1, row=0, sticky="w", padx=UI_CONFIG['padding']['small'])
        
        self.db_type_combo = ttk.Combobox(
            db_type_frame, 
            textvariable=self.db_type_var, 
            values=list(DB_TYPES.keys()), 
            state="readonly", 
            width=20,
            style='Modern.TCombobox'
        )
        self.db_type_combo.grid(column=0, row=0, sticky="w")
        self.db_type_combo.bind("<<ComboboxSelected>>", self._on_db_type_change)
        
        # Botón para ver estado de herramientas
        self.tools_status_btn = ttk.Button(
            db_type_frame,
            text="🔧 Estado",
            width=10,
            style='Modern.TButton'
        )
        self.tools_status_btn.grid(column=1, row=0, sticky="w", padx=(UI_CONFIG['padding']['small'], 0))
        self.tools_status_btn.configure(command=self._show_tools_status)
        
        # Servidor y Puerto en la misma fila
        ttk.Label(
            conn_frame, 
            text="🖥️ Servidor:",
            font=UI_CONFIG['fonts']['body'],
            background=UI_CONFIG['colors']['surface']
        ).grid(column=0, row=1, sticky="w", padx=(0, UI_CONFIG['padding']['small']), pady=(UI_CONFIG['padding']['small'], 0))
        
        server_port_frame = tk.Frame(conn_frame, bg=UI_CONFIG['colors']['surface'])
        server_port_frame.grid(column=1, row=1, sticky="ew", padx=UI_CONFIG['padding']['small'], pady=(UI_CONFIG['padding']['small'], 0))
        
        ttk.Entry(
            server_port_frame, 
            textvariable=self.server_var, 
            width=25,
            style='Modern.TEntry'
        ).grid(column=0, row=0, sticky="w")
        
        ttk.Label(
            server_port_frame, 
            text="Puerto:",
            font=UI_CONFIG['fonts']['small'],
            background=UI_CONFIG['colors']['surface']
        ).grid(column=1, row=0, sticky="w", padx=(UI_CONFIG['padding']['medium'], UI_CONFIG['padding']['small']))
        
        self.port_entry = ttk.Entry(
            server_port_frame, 
            textvariable=self.port_var, 
            width=8,
            style='Modern.TEntry'
        )
        self.port_entry.grid(column=2, row=0, sticky="w")
        
        # Usuario
        ttk.Label(
            conn_frame, 
            text="👤 Usuario:",
            font=UI_CONFIG['fonts']['body'],
            background=UI_CONFIG['colors']['surface']
        ).grid(column=0, row=2, sticky="w", padx=(0, UI_CONFIG['padding']['small']), pady=(UI_CONFIG['padding']['small'], 0))
        
        ttk.Entry(
            conn_frame, 
            textvariable=self.user_var, 
            width=UI_CONFIG['entry_width'],
            style='Modern.TEntry'
        ).grid(column=1, row=2, sticky="w", padx=UI_CONFIG['padding']['small'], pady=(UI_CONFIG['padding']['small'], 0))
        current_row += 1
        
        # Contraseña
        ttk.Label(
            conn_frame, 
            text="🔐 Contraseña:",
            font=UI_CONFIG['fonts']['body'],
            background=UI_CONFIG['colors']['surface']
        ).grid(column=0, row=3, sticky="w", padx=(0, UI_CONFIG['padding']['small']), pady=(UI_CONFIG['padding']['small'], 0))
        
        password_frame = tk.Frame(conn_frame, bg=UI_CONFIG['colors']['surface'])
        password_frame.grid(column=1, row=3, sticky="ew", padx=UI_CONFIG['padding']['small'], pady=(UI_CONFIG['padding']['small'], 0))
        
        ttk.Entry(
            password_frame, 
            textvariable=self.pwd_var, 
            show="*", 
            width=25,
            style='Modern.TEntry'
        ).grid(column=0, row=0, sticky="w")
        
        # Botón de validación de conexión
        ttk.Button(
            password_frame, 
            text="✅ Validar Conexión", 
            command=self._validate_and_save_connection,
            style='Success.TButton'
        ).grid(column=1, row=0, padx=(UI_CONFIG['padding']['medium'], 0))
        
        current_row += 1
        
        # Separador
        separator2 = ttk.Separator(self.frame, orient='horizontal')
        separator2.grid(column=0, row=current_row, columnspan=3, sticky="ew", pady=UI_CONFIG['padding']['medium'])
        current_row += 1
        
        # Frame para bases de datos con diseño moderno
        db_label = tk.Label(
            self.frame, 
            text="💾 Selección de Bases de Datos",
            font=UI_CONFIG['fonts']['subtitle'],
            bg=UI_CONFIG['colors']['surface'],
            fg=UI_CONFIG['colors']['primary']
        )
        db_label.grid(column=0, row=current_row, columnspan=3, sticky="w", pady=(0, UI_CONFIG['padding']['small']))
        current_row += 1
        
        db_frame = tk.Frame(self.frame, bg=UI_CONFIG['colors']['surface'])
        db_frame.grid(column=0, row=current_row, columnspan=3, sticky="ew", pady=(0, UI_CONFIG['padding']['medium']))
        
        # Botón para cargar bases de datos
        ttk.Button(
            db_frame, 
            text="🔄 Cargar Bases de Datos", 
            command=self._load_databases,
            style='Primary.TButton'
        ).grid(row=0, column=0, sticky="w", padx=(0, UI_CONFIG['padding']['medium']), pady=UI_CONFIG['padding']['small'])
        
        # Frame para listbox con scrollbar
        db_selection_frame = tk.Frame(db_frame, bg=UI_CONFIG['colors']['surface'])
        db_selection_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=UI_CONFIG['padding']['small'])
        
        # Listbox para mostrar y seleccionar bases de datos con diseño moderno
        listbox_frame = tk.Frame(db_selection_frame, relief='solid', bd=1, bg=UI_CONFIG['colors']['border'])
        listbox_frame.pack(fill="both", expand=True, padx=UI_CONFIG['padding']['small'])
        
        self.db_listbox = tk.Listbox(
            listbox_frame, 
            selectmode=tk.MULTIPLE, 
            height=6,
            font=UI_CONFIG['fonts']['body'],
            bg=UI_CONFIG['colors']['surface'],
            fg=UI_CONFIG['colors']['text'],
            selectbackground=UI_CONFIG['colors']['primary'],
            selectforeground='white',
            relief='flat',
            bd=0
        )
        self.db_listbox.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        
        # Scrollbar para la listbox
        db_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.db_listbox.yview)
        db_scrollbar.pack(side="right", fill="y")
        self.db_listbox.configure(yscrollcommand=db_scrollbar.set)
        
        current_row += 1
        
        # Configurar redimensionamiento del frame principal
        self.frame.grid_columnconfigure(0, weight=1)
        current_row += 1
        
        # Separador final
        separator3 = ttk.Separator(self.frame, orient='horizontal')
        separator3.grid(column=0, row=current_row, columnspan=3, sticky="ew", pady=UI_CONFIG['padding']['medium'])
        current_row += 1
        
        # Sección de ruta de respaldo
        path_label = tk.Label(
            self.frame, 
            text="📁 Configuración de Respaldo",
            font=UI_CONFIG['fonts']['subtitle'],
            bg=UI_CONFIG['colors']['surface'],
            fg=UI_CONFIG['colors']['primary']
        )
        path_label.grid(column=0, row=current_row, columnspan=3, sticky="w", pady=(0, UI_CONFIG['padding']['small']))
        current_row += 1
        
        # Frame para ruta de respaldo
        path_frame = tk.Frame(self.frame, bg=UI_CONFIG['colors']['surface'])
        path_frame.grid(column=0, row=current_row, columnspan=3, sticky="ew", pady=(0, UI_CONFIG['padding']['medium']))
        
        # Ruta de Respaldo
        ttk.Label(
            path_frame, 
            text="💾 Ruta de Respaldo:",
            font=UI_CONFIG['fonts']['body'],
            background=UI_CONFIG['colors']['surface']
        ).grid(column=0, row=0, sticky="w", padx=(0, UI_CONFIG['padding']['small']))
        
        ttk.Entry(
            path_frame, 
            textvariable=self.path_var, 
            width=UI_CONFIG['entry_width'],
            style='Modern.TEntry'
        ).grid(column=1, row=0, sticky="ew", padx=UI_CONFIG['padding']['small'])
        
        # Botón de validación de ruta
        ttk.Button(
            path_frame, 
            text="✅ Validar Ruta", 
            command=self.validate_path_callback,
            style='Primary.TButton'
        ).grid(column=2, row=0, padx=(UI_CONFIG['padding']['medium'], 0))
        
        current_row += 1
        
        # Separador final  
        separator4 = ttk.Separator(self.frame, orient='horizontal')
        separator4.grid(column=0, row=current_row, columnspan=3, sticky="ew", pady=UI_CONFIG['padding']['medium'])
        current_row += 1
        
        # Sección de programación
        schedule_label = tk.Label(
            self.frame, 
            text="⏰ Programación de Respaldos",
            font=UI_CONFIG['fonts']['subtitle'],
            bg=UI_CONFIG['colors']['surface'],
            fg=UI_CONFIG['colors']['primary']
        )
        schedule_label.grid(column=0, row=current_row, columnspan=3, sticky="w", pady=(0, UI_CONFIG['padding']['small']))
        current_row += 1
        
        # Frame para programación
        schedule_frame = tk.Frame(self.frame, bg=UI_CONFIG['colors']['surface'])
        schedule_frame.grid(column=0, row=current_row, columnspan=3, sticky="ew", pady=(0, UI_CONFIG['padding']['medium']))
        
        # Variables para programación
        self.freq_var = tk.StringVar(value=BACKUP_CONFIG['default_frequency'])
        self.time_var = tk.StringVar(value=BACKUP_CONFIG['default_time'])
        self.interval_var = tk.StringVar(value="6")
        
        # Frecuencia
        ttk.Label(
            schedule_frame, 
            text="🔄 Frecuencia:",
            font=UI_CONFIG['fonts']['body'],
            background=UI_CONFIG['colors']['surface']
        ).grid(column=0, row=0, sticky="w", padx=(0, UI_CONFIG['padding']['small']))
        
        self.freq_menu = ttk.Combobox(
            schedule_frame, 
            textvariable=self.freq_var, 
            values=BACKUP_CONFIG['frequency_options'], 
            state="readonly",
            width=20,
            style='Modern.TCombobox'
        )
        self.freq_menu.grid(column=1, row=0, sticky="w", padx=UI_CONFIG['padding']['small'])
        self.freq_menu.bind("<<ComboboxSelected>>", self._on_frequency_change)
        
        # Hora para diario
        self.time_label = ttk.Label(
            schedule_frame, 
            text="🕐 Hora (HH:MM):",
            font=UI_CONFIG['fonts']['body'],
            background=UI_CONFIG['colors']['surface']
        )
        self.time_label.grid(column=0, row=1, sticky="w", padx=(0, UI_CONFIG['padding']['small']), pady=(UI_CONFIG['padding']['small'], 0))
        
        self.time_entry = ttk.Entry(
            schedule_frame, 
            textvariable=self.time_var, 
            width=10,
            style='Modern.TEntry'
        )
        self.time_entry.grid(column=1, row=1, sticky="w", padx=UI_CONFIG['padding']['small'], pady=(UI_CONFIG['padding']['small'], 0))
        
        # Intervalo para cada X horas
        self.interval_label = ttk.Label(
            schedule_frame, 
            text="⏱️ Intervalo (horas):",
            font=UI_CONFIG['fonts']['body'],
            background=UI_CONFIG['colors']['surface']
        )
        self.interval_label.grid(column=0, row=2, sticky="w", padx=(0, UI_CONFIG['padding']['small']), pady=(UI_CONFIG['padding']['small'], 0))
        
        self.interval_spinbox = ttk.Spinbox(
            schedule_frame, 
            textvariable=self.interval_var,
            from_=BACKUP_CONFIG['min_interval_hours'], 
            to=BACKUP_CONFIG['max_interval_hours'], 
            width=UI_CONFIG['spinbox_width'],
            style='Modern.TCombobox'
        )
        self.interval_spinbox.grid(column=1, row=2, sticky="w", padx=UI_CONFIG['padding']['small'], pady=(UI_CONFIG['padding']['small'], 0))
        
        # Configurar la visualización inicial de la programación
        self._on_frequency_change()
        
        current_row += 1
        
        # Configurar redimensionamiento del frame principal
        self.frame.grid_columnconfigure(0, weight=1)
        conn_frame.grid_columnconfigure(1, weight=1)
        db_frame.grid_columnconfigure(0, weight=1)
        path_frame.grid_columnconfigure(1, weight=1)
    
    def _show_tools_status(self):
        """Muestra el estado de las herramientas de base de datos."""
        try:
            # Obtener la ventana principal (root)
            root = self.frame.winfo_toplevel()
            show_database_status_dialog(root)
        except Exception as e:
            messagebox.showerror("Error", f"Error mostrando estado de herramientas: {e}")
    
    def _on_db_type_change(self, event=None):
        """Maneja el cambio en el tipo de base de datos."""
        db_type = self.db_type_var.get()
        
        # Actualizar puerto por defecto
        default_ports = {
            'SQL Server': '1433',
            'MySQL': '3306',
            'PostgreSQL': '5432'
        }
        
        self.port_var.set(default_ports.get(db_type, '1433'))
        
        # Limpiar lista de bases de datos
        self.db_listbox.delete(0, tk.END)
        self.available_databases = []
        self.selected_databases = []
    
    def _on_frequency_change(self, event=None):
        """Maneja el cambio en la frecuencia de respaldos."""
        frequency = self.freq_var.get()
        
        if frequency == "diario":
            # Mostrar controles de hora
            self.time_label.grid()
            self.time_entry.grid()
            # Ocultar controles de intervalo
            self.interval_label.grid_remove()
            self.interval_spinbox.grid_remove()
        elif frequency == "cada X horas":
            # Ocultar controles de hora
            self.time_label.grid_remove()
            self.time_entry.grid_remove()
            # Mostrar controles de intervalo
            self.interval_label.grid()
            self.interval_spinbox.grid()
    
    def get_schedule_data(self) -> dict:
        """Obtiene los datos de programación configurados."""
        return {
            'frequency': self.freq_var.get(),
            'time': self.time_var.get() if self.freq_var.get() == "diario" else None,
            'interval_hours': int(self.interval_var.get()) if self.freq_var.get() == "cada X horas" else None
        }
    
    def _load_databases(self):
        """Carga las bases de datos disponibles."""
        connection_data = self.get_connection_data()
        self.load_databases_callback(connection_data)
    
    def set_available_databases(self, databases: list):
        """Establece las bases de datos disponibles en el listbox."""
        self.available_databases = databases
        self.db_listbox.delete(0, tk.END)
        
        for db in databases:
            self.db_listbox.insert(tk.END, db)
    
    def get_selected_databases(self) -> list:
        """Obtiene las bases de datos seleccionadas."""
        selected_indices = self.db_listbox.curselection()
        return [self.available_databases[i] for i in selected_indices]
    
    def _load_connection_history(self):
        """Carga el historial de conexiones."""
        try:
            history = ConnectionHistoryService.get_connection_display_list()
            self.history_combo['values'] = tuple(history)  # Convertir a tupla para evitar problemas
            if history:
                print(f"🔧 DEBUG: Historial cargado: {len(history)} conexiones")
            else:
                print("🔧 DEBUG: No hay historial de conexiones")
        except Exception as e:
            print(f"🔧 DEBUG: Error cargando historial: {e}")
            self.history_combo['values'] = ()
    
    def _on_history_selected(self, event=None):
        """Maneja la selección de una conexión del historial."""
        try:
            selected = self.connection_history_var.get()
            if not selected:
                return
                
            print(f"🔧 DEBUG: Seleccionado del historial: {selected}")
            
            db_type, server, port, databases = ConnectionHistoryService.parse_connection_string(selected)
            
            if server:  # Solo proceder si tenemos datos válidos
                self.db_type_var.set(db_type)
                self.server_var.set(server)
                self.port_var.set(str(port))
                
                # Cargar bases de datos en el listbox
                if databases and databases != ["(conexión validada)"]:
                    self.set_available_databases(databases)
                    
                    # Seleccionar todas las bases de datos por defecto
                    for i in range(len(databases)):
                        self.db_listbox.selection_set(i)
                    
                    print(f"🔧 DEBUG: Cargadas {len(databases)} bases de datos del historial")
                else:
                    print("🔧 DEBUG: No hay bases de datos específicas en el historial")
            else:
                print("🔧 DEBUG: Datos de conexión inválidos en el historial")
                
        except Exception as e:
            print(f"🔧 DEBUG: Error en _on_history_selected: {e}")
    
    def _clear_history(self):
        """Limpia el historial de conexiones."""
        if MessageHelper.show_confirm("Confirmar", "¿Está seguro de que desea limpiar el historial de conexiones?"):
            if ConnectionHistoryService.clear_connections_history():
                self.history_combo['values'] = ()
                self.connection_history_var.set("")
                MessageHelper.show_success("Éxito", "Historial de conexiones limpiado correctamente.")
            else:
                MessageHelper.show_error("Error", "No se pudo limpiar el historial de conexiones.")
    
    def _validate_and_save_connection(self):
        """Valida la conexión y guarda en el historial si es exitosa."""
        # Ejecutar la validación original
        if self.validate_connection_callback():
            # Si la validación fue exitosa, guardar en el historial
            # (incluso sin bases de datos seleccionadas)
            self._save_current_connection_to_history()
    
    def _save_current_connection_to_history(self):
        """Guarda la conexión actual al historial."""
        try:
            db_type_key = DB_TYPES.get(self.db_type_var.get())
            server = self.server_var.get()
            port = int(self.port_var.get()) if self.port_var.get().isdigit() else 1433
            
            # Intentar obtener bases de datos seleccionadas, si no hay usar las disponibles
            selected_dbs = self.get_selected_databases()
            if not selected_dbs and hasattr(self, 'available_databases'):
                selected_dbs = self.available_databases  # Usar todas las disponibles
            
            if server:  # Solo necesitamos servidor para guardar
                # Si no hay bases de datos, crear una lista vacía para indicar que la conexión funcionó
                if not selected_dbs:
                    selected_dbs = ["(conexión validada)"]  # Placeholder para indicar conexión exitosa
                
                if ConnectionHistoryService.save_connection(db_type_key, server, port, selected_dbs):
                    print(f"🔧 DEBUG: Conexión guardada en historial: {server}:{port}")
                    self._load_connection_history()  # Recargar el historial
                else:
                    print(f"🔧 DEBUG: Error guardando conexión en historial")
            else:
                print(f"🔧 DEBUG: No se puede guardar conexión sin servidor")
        except Exception as e:
            print(f"🔧 DEBUG: Error en _save_current_connection_to_history: {e}")
    
    def update_databases_list(self, databases: list):
        """Actualiza la lista de bases de datos y guarda la conexión al historial."""
        self.available_databases = databases
        self.db_listbox.delete(0, tk.END)
        
        for db in databases:
            self.db_listbox.insert(tk.END, db)
        
        # Guardar conexión al historial cuando se cargan las bases de datos exitosamente
        if databases:  # Solo si hay bases de datos
            self._save_current_connection_to_history()
    
    def get_connection_data(self) -> dict:
        """Retorna los datos de conexión."""
        return {
            'db_type': DB_TYPES.get(self.db_type_var.get()),
            'server': self.server_var.get(),
            'port': int(self.port_var.get()) if self.port_var.get().isdigit() else 1433,
            'username': self.user_var.get(),
            'password': self.pwd_var.get(),
            'databases': self.get_selected_databases(),
            'backup_path': self.path_var.get()
        }


class ScheduleFrame:
    """Frame para configuración de programación de respaldos."""
    
    def __init__(self, parent):
        self.parent = parent
        self.freq_var = tk.StringVar(value=BACKUP_CONFIG['default_frequency'])
        self.time_var = tk.StringVar(value=BACKUP_CONFIG['default_time'])
        
        self._create_widgets()
        self._configure_frequency_change()
    
    def _create_widgets(self):
        """Crea los widgets del frame de programación."""
        # Frecuencia
        ttk.Label(self.parent, text="Frecuencia:").grid(column=0, row=10, sticky="w")
        self.freq_menu = ttk.Combobox(self.parent, textvariable=self.freq_var, 
                                     values=BACKUP_CONFIG['frequency_options'], state="readonly")
        self.freq_menu.grid(column=1, row=10)
        self.freq_menu.bind("<<ComboboxSelected>>", self._on_frequency_change)
        
        # Hora para diario
        self.time_label = ttk.Label(self.parent, text="Hora (HH:MM):")
        self.time_entry = ttk.Entry(self.parent, textvariable=self.time_var, width=10)
        
        # Intervalo para cada X horas
        self.interval_label = ttk.Label(self.parent, text="Intervalo (horas):")
        self.interval_entry = ttk.Spinbox(self.parent, 
                                        from_=BACKUP_CONFIG['min_interval_hours'], 
                                        to=BACKUP_CONFIG['max_interval_hours'], 
                                        width=UI_CONFIG['spinbox_width'])
    
    def _configure_frequency_change(self):
        """Configura la visualización inicial basada en la frecuencia."""
        self._on_frequency_change()
    
    def _on_frequency_change(self, event=None):
        """Maneja el cambio en la selección de frecuencia."""
        if self.freq_var.get() == "diario":
            self.time_label.grid(column=0, row=11, sticky="w")
            self.time_entry.grid(column=1, row=11, sticky="w")
            self.interval_label.grid_remove()
            self.interval_entry.grid_remove()
        else:
            self.time_label.grid_remove()
            self.time_entry.grid_remove()
            self.interval_label.grid(column=0, row=11, sticky="w")
            self.interval_entry.grid(column=1, row=11, sticky="w")
    
    def get_schedule_config(self) -> dict:
        """Retorna la configuración de programación."""
        config = {
            'frequency': self.freq_var.get(),
            'time': self.time_var.get()
        }
        
        if self.freq_var.get() != "diario":
            config['interval_hours'] = int(self.interval_entry.get())
        
        return config


class ControlButtonsFrame:
    """Frame para botones de control del sistema."""
    
    def __init__(self, parent, start_callback: Callable, stop_callback: Callable):
        self.frame = tk.Frame(parent, bg=UI_CONFIG['colors']['background'])
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crea los botones de control con diseño moderno."""
        # Crear frame central para los botones
        button_container = tk.Frame(self.frame, bg=UI_CONFIG['colors']['background'])
        button_container.pack(expand=True)
        
        # Botón Iniciar con icono y estilo moderno
        self.start_btn = ttk.Button(
            button_container, 
            text="▶️ Iniciar Respaldos", 
            command=self.start_callback,
            style='Success.TButton'
        )
        self.start_btn.grid(column=0, row=0, padx=UI_CONFIG['padding']['medium'])
        
        # Botón Detener con icono y estilo moderno
        self.stop_btn = ttk.Button(
            button_container, 
            text="⏹️ Detener Proceso", 
            command=self.stop_callback, 
            state="disabled",
            style='Error.TButton'
        )
        self.stop_btn.grid(column=1, row=0, padx=UI_CONFIG['padding']['medium'])
    
    def set_running_state(self, running: bool):
        """Configura el estado de los botones según si está ejecutándose."""
        if running:
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
        else:
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")


class LogFrame:
    """Frame para mostrar logs de actividad."""
    
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(
            parent, 
            text="📋 Logs de Actividad",
            style='Modern.TLabelframe'
        )
        self._create_widgets()
        self._load_previous_logs()
    
    def _create_widgets(self):
        """Crea el widget de logs y botones de control con diseño moderno."""
        # Configurar padding del frame
        self.frame.configure(padding=UI_CONFIG['padding']['medium'])
        
        # Frame para botones con diseño mejorado
        buttons_frame = tk.Frame(self.frame, bg=UI_CONFIG['colors']['surface'])
        buttons_frame.pack(fill="x", pady=(0, UI_CONFIG['padding']['medium']))
        
        # Título de la sección
        title_label = tk.Label(
            buttons_frame,
            text="🛠️ Controles de Logs:",
            font=UI_CONFIG['fonts']['body'],
            bg=UI_CONFIG['colors']['surface'],
            fg=UI_CONFIG['colors']['text_secondary']
        )
        title_label.pack(side="left", padx=(0, UI_CONFIG['padding']['medium']))
        
        # Botones de control de logs con iconos
        ttk.Button(
            buttons_frame, 
            text="🗑️ Limpiar", 
            command=self._clear_logs,
            style='Warning.TButton'
        ).pack(side="left", padx=(0, UI_CONFIG['padding']['small']))
        
        ttk.Button(
            buttons_frame, 
            text="💾 Guardar", 
            command=self._save_logs,
            style='Primary.TButton'
        ).pack(side="left", padx=(0, UI_CONFIG['padding']['small']))
        
        ttk.Button(
            buttons_frame, 
            text="📤 Exportar", 
            command=self._export_logs,
            style='Primary.TButton'
        ).pack(side="left")
        
        # Frame contenedor para el texto de logs con borde
        log_container = tk.Frame(
            self.frame, 
            relief='solid', 
            bd=1, 
            bg=UI_CONFIG['colors']['border']
        )
        log_container.pack(fill="both", expand=True)
        
        # Widget de texto para logs con diseño moderno
        self.log_text = scrolledtext.ScrolledText(
            log_container, 
            state="disabled", 
            height=UI_CONFIG['log_height'],
            font=UI_CONFIG['fonts']['body'],
            bg=UI_CONFIG['colors']['surface'],
            fg=UI_CONFIG['colors']['text'],
            relief='flat',
            bd=0,
            wrap=tk.WORD
        )
        self.log_text.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Configurar tags para diferentes tipos de mensajes
        self.log_text.tag_config("info", foreground=UI_CONFIG['colors']['text'])
        self.log_text.tag_config("success", foreground=UI_CONFIG['colors']['success'])
        self.log_text.tag_config("warning", foreground=UI_CONFIG['colors']['warning'])
        self.log_text.tag_config("error", foreground=UI_CONFIG['colors']['error'])
        self.log_text.tag_config("header", foreground=UI_CONFIG['colors']['primary'], font=UI_CONFIG['fonts']['subtitle'])
    
    def _load_previous_logs(self):
        """Carga los logs anteriores al iniciar."""
        previous_logs = FileService.load_logs_from_file()
        if previous_logs:
            self.log_text.configure(state="normal")
            self.log_text.insert(tk.END, previous_logs)
            if not previous_logs.endswith('\n'):
                self.log_text.insert(tk.END, '\n')
            self.log_text.insert(tk.END, f"{'='*50}\n")
            self.log_text.insert(tk.END, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sesión iniciada\n")
            self.log_text.insert(tk.END, f"{'='*50}\n")
            self.log_text.configure(state="disabled")
            self.log_text.see(tk.END)
    
    def _clear_logs(self):
        """Limpia los logs de la pantalla y del archivo."""
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea limpiar todos los logs?"):
            self.log_text.configure(state="normal")
            self.log_text.delete(1.0, tk.END)
            self.log_text.configure(state="disabled")
            
            # Limpiar también el archivo
            if FileService.clear_logs_file():
                self.add_log("Logs limpiados correctamente.")
            else:
                self.add_log("Error al limpiar el archivo de logs.")
    
    def _save_logs(self):
        """Guarda los logs actuales en el archivo."""
        content = self.log_text.get(1.0, tk.END)
        if FileService.save_logs_to_file(content):
            messagebox.showinfo("Éxito", "Logs guardados correctamente.")
        else:
            messagebox.showerror("Error", "No se pudieron guardar los logs.")
    
    def _export_logs(self):
        """Exporta los logs a un archivo con timestamp."""
        from tkinter import filedialog
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"backup_logs_{timestamp}.txt"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialname=default_filename
        )
        
        if filename:
            try:
                content = self.log_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Éxito", f"Logs exportados a: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron exportar los logs: {e}")
    
    def add_log(self, message: str):
        """Agrega un mensaje al log con formato y colores."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Determinar el tipo de mensaje y aplicar color
        tag = "info"  # Por defecto
        if any(word in message.lower() for word in ["error", "falló", "fallo", "failed"]):
            tag = "error"
        elif any(word in message.lower() for word in ["éxito", "exitoso", "completado", "success"]):
            tag = "success"
        elif any(word in message.lower() for word in ["advertencia", "warning", "atención"]):
            tag = "warning"
        elif message.startswith("===") or message.startswith("---"):
            tag = "header"
        
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, log_entry, tag)
        self.log_text.configure(state="disabled")
        self.log_text.see(tk.END)
        
        # Guardar automáticamente cada nuevo log
        content = self.log_text.get(1.0, tk.END)
        FileService.save_logs_to_file(content)


class MessageHelper:
    """Clase auxiliar para mostrar mensajes al usuario."""
    
    @staticmethod
    def show_success(title: str, message: str):
        """Muestra un mensaje de éxito."""
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_error(title: str, message: str):
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)
    
    @staticmethod
    def show_confirm(title: str, message: str) -> bool:
        """Muestra un diálogo de confirmación."""
        return messagebox.askyesno(title, message)
