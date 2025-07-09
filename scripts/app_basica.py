"""
Versión básica y simple de la aplicación para verificar visibilidad.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def crear_app_basica():
    """Crea una versión básica de la aplicación para verificar que todo funcione."""
    
    # Ventana principal
    root = tk.Tk()
    root.title("🗃️ Respaldos SQL - Versión Básica")
    root.geometry("1200x900")
    root.configure(bg='#F8F9FA')
    
    # Frame principal
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill='both', expand=True)
    
    # Título
    title_label = tk.Label(
        main_frame, 
        text="🗃️ Configurador de Respaldos Multi-BD",
        font=('Segoe UI', 16, 'bold'),
        bg='#F8F9FA',
        fg='#2E86AB'
    )
    title_label.pack(pady=(0, 20))
    
    # Frame de configuración de conexión
    conn_frame = ttk.LabelFrame(main_frame, text="🔗 Configuración de Conexión", padding="15")
    conn_frame.pack(fill='x', pady=(0, 15))
    
    # Tipo de BD
    tk.Label(conn_frame, text="🗄️ Tipo de BD:").grid(row=0, column=0, sticky='w', padx=(0, 10))
    tipo_combo = ttk.Combobox(conn_frame, values=['SQL Server', 'MySQL', 'PostgreSQL'], state='readonly')
    tipo_combo.set('SQL Server')
    tipo_combo.grid(row=0, column=1, sticky='ew', padx=(0, 20))
    
    # Servidor
    tk.Label(conn_frame, text="🖥️ Servidor:").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
    servidor_entry = ttk.Entry(conn_frame, width=30)
    servidor_entry.grid(row=1, column=1, sticky='ew', padx=(0, 20), pady=(10, 0))
    
    # Puerto
    tk.Label(conn_frame, text="🔌 Puerto:").grid(row=1, column=2, sticky='w', padx=(10, 10), pady=(10, 0))
    puerto_entry = ttk.Entry(conn_frame, width=10)
    puerto_entry.insert(0, "1433")
    puerto_entry.grid(row=1, column=3, sticky='w', pady=(10, 0))
    
    # Usuario
    tk.Label(conn_frame, text="👤 Usuario:").grid(row=2, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
    usuario_entry = ttk.Entry(conn_frame, width=30)
    usuario_entry.grid(row=2, column=1, sticky='ew', padx=(0, 20), pady=(10, 0))
    
    # Contraseña
    tk.Label(conn_frame, text="🔐 Contraseña:").grid(row=3, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
    password_entry = ttk.Entry(conn_frame, width=30, show="*")
    password_entry.grid(row=3, column=1, sticky='ew', padx=(0, 20), pady=(10, 0))
    
    # Botón validar conexión
    validar_btn = ttk.Button(conn_frame, text="✅ Validar Conexión")
    validar_btn.grid(row=3, column=2, columnspan=2, padx=(10, 0), pady=(10, 0))
    
    # Configurar expansión de columnas
    conn_frame.grid_columnconfigure(1, weight=1)
    
    # Frame de bases de datos
    db_frame = ttk.LabelFrame(main_frame, text="💾 Selección de Bases de Datos", padding="15")
    db_frame.pack(fill='x', pady=(0, 15))
    
    # Botón cargar BD
    cargar_btn = ttk.Button(db_frame, text="🔄 Cargar Bases de Datos")
    cargar_btn.pack(anchor='w', pady=(0, 10))
    
    # Lista de BD
    listframe = tk.Frame(db_frame)
    listframe.pack(fill='x')
    
    db_listbox = tk.Listbox(listframe, height=4, selectmode='multiple')
    db_listbox.pack(side='left', fill='both', expand=True)
    
    scrollbar = ttk.Scrollbar(listframe, orient='vertical', command=db_listbox.yview)
    scrollbar.pack(side='right', fill='y')
    db_listbox.config(yscrollcommand=scrollbar.set)
    
    # Agregar elementos de ejemplo
    for i, db in enumerate(['master', 'model', 'msdb', 'tempdb']):
        db_listbox.insert(i, db)
    
    # Frame de respaldo
    backup_frame = ttk.LabelFrame(main_frame, text="📁 Configuración de Respaldo", padding="15")
    backup_frame.pack(fill='x', pady=(0, 15))
    
    # Ruta de respaldo
    tk.Label(backup_frame, text="💾 Ruta:").grid(row=0, column=0, sticky='w', padx=(0, 10))
    ruta_entry = ttk.Entry(backup_frame, width=50)
    ruta_entry.grid(row=0, column=1, sticky='ew', padx=(0, 10))
    validar_ruta_btn = ttk.Button(backup_frame, text="✅ Validar Ruta")
    validar_ruta_btn.grid(row=0, column=2)
    
    backup_frame.grid_columnconfigure(1, weight=1)
    
    # Frame de programación
    prog_frame = ttk.LabelFrame(main_frame, text="⏰ Programación", padding="15")
    prog_frame.pack(fill='x', pady=(0, 15))
    
    # Frecuencia
    tk.Label(prog_frame, text="🔄 Frecuencia:").grid(row=0, column=0, sticky='w', padx=(0, 10))
    freq_combo = ttk.Combobox(prog_frame, values=['Diario', 'Semanal', 'Cada X horas'], state='readonly')
    freq_combo.set('Diario')
    freq_combo.grid(row=0, column=1, sticky='w', padx=(0, 20))
    
    # Hora
    tk.Label(prog_frame, text="🕐 Hora:").grid(row=0, column=2, sticky='w', padx=(10, 10))
    hora_entry = ttk.Entry(prog_frame, width=10)
    hora_entry.insert(0, "02:00")
    hora_entry.grid(row=0, column=3, sticky='w')
    
    # Frame de control
    control_frame = tk.Frame(main_frame)
    control_frame.pack(pady=20)
    
    # Botones de control
    iniciar_btn = tk.Button(
        control_frame, 
        text="🚀 Iniciar Respaldos", 
        bg='#28A745', 
        fg='white', 
        font=('Segoe UI', 11, 'bold'),
        padx=20, 
        pady=8
    )
    iniciar_btn.pack(side='left', padx=(0, 10))
    
    detener_btn = tk.Button(
        control_frame, 
        text="⏹️ Detener Respaldos", 
        bg='#DC3545', 
        fg='white', 
        font=('Segoe UI', 11, 'bold'),
        padx=20, 
        pady=8
    )
    detener_btn.pack(side='left')
    
    # Frame de logs
    log_frame = ttk.LabelFrame(main_frame, text="📋 Registro de Actividades", padding="10")
    log_frame.pack(fill='both', expand=True)
    
    # Área de texto para logs
    from tkinter import scrolledtext
    log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap='word')
    log_text.pack(fill='both', expand=True)
    
    # Mensaje inicial
    log_text.insert('end', "🎉 Aplicación iniciada correctamente\n")
    log_text.insert('end', "📋 Todas las secciones son visibles:\n")
    log_text.insert('end', "   ✅ Configuración de conexión\n")
    log_text.insert('end', "   ✅ Selección de bases de datos\n")
    log_text.insert('end', "   ✅ Configuración de respaldo\n")
    log_text.insert('end', "   ✅ Programación\n")
    log_text.insert('end', "   ✅ Botones de control\n")
    log_text.insert('end', "   ✅ Registro de logs\n")
    log_text.insert('end', "\n🚀 ¡La aplicación está lista para usar!\n")
    
    return root

if __name__ == "__main__":
    print("🚀 Creando aplicación básica y visible...")
    app = crear_app_basica()
    print("✅ Aplicación creada - Verificando que todo sea visible...")
    app.mainloop()
