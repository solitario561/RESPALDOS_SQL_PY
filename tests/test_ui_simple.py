"""
Script de prueba simple para verificar que la interfaz se muestre correctamente.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk
from config.settings import UI_CONFIG

def test_simple_ui():
    """Crea una versión simplificada para probar la visibilidad."""
    root = tk.Tk()
    root.title("🗃️ Test - Configurador de Respaldos")
    root.geometry("800x600")
    root.configure(bg='#F8F9FA')
    
    # Frame principal
    main_frame = tk.Frame(root, bg='#F8F9FA', padx=20, pady=20)
    main_frame.pack(fill='both', expand=True)
    
    # Título
    title_label = tk.Label(
        main_frame,
        text="🛠️ OPCIONES DE CONFIGURACIÓN",
        font=('Segoe UI', 16, 'bold'),
        bg='#F8F9FA',
        fg='#2E86AB'
    )
    title_label.pack(pady=(0, 20))
    
    # Frame de conexión
    conn_frame = tk.LabelFrame(
        main_frame,
        text="🔗 Configuración de Conexión",
        font=('Segoe UI', 12, 'bold'),
        bg='white',
        fg='#2E86AB',
        padx=15,
        pady=15
    )
    conn_frame.pack(fill='x', pady=(0, 10))
    
    # Campos de conexión
    fields = [
        ("🗄️ Tipo de BD:", ["SQL Server", "MySQL", "PostgreSQL"]),
        ("🖥️ Servidor:", None),
        ("👤 Usuario:", None),
        ("🔐 Contraseña:", None)
    ]
    
    for i, (label, values) in enumerate(fields):
        tk.Label(conn_frame, text=label, bg='white', font=('Segoe UI', 10)).grid(
            row=i, column=0, sticky='w', pady=5, padx=(0, 10)
        )
        
        if values:  # Combobox
            combo = ttk.Combobox(conn_frame, values=values, width=25)
            combo.set(values[0])
            combo.grid(row=i, column=1, sticky='w', pady=5)
        else:  # Entry
            entry = tk.Entry(conn_frame, width=30, relief='solid', bd=1)
            entry.grid(row=i, column=1, sticky='w', pady=5)
    
    # Frame de programación
    schedule_frame = tk.LabelFrame(
        main_frame,
        text="⏰ Programación de Respaldos",
        font=('Segoe UI', 12, 'bold'),
        bg='white',
        fg='#2E86AB',
        padx=15,
        pady=15
    )
    schedule_frame.pack(fill='x', pady=(0, 10))
    
    # Frecuencia
    tk.Label(schedule_frame, text="🔄 Frecuencia:", bg='white', font=('Segoe UI', 10)).grid(
        row=0, column=0, sticky='w', pady=5, padx=(0, 10)
    )
    freq_combo = ttk.Combobox(schedule_frame, values=["diario", "cada X horas"], width=25)
    freq_combo.set("diario")
    freq_combo.grid(row=0, column=1, sticky='w', pady=5)
    
    # Hora
    tk.Label(schedule_frame, text="🕐 Hora (HH:MM):", bg='white', font=('Segoe UI', 10)).grid(
        row=1, column=0, sticky='w', pady=5, padx=(0, 10)
    )
    time_entry = tk.Entry(schedule_frame, width=15, relief='solid', bd=1)
    time_entry.insert(0, "00:00")
    time_entry.grid(row=1, column=1, sticky='w', pady=5)
    
    # Frame de botones
    button_frame = tk.Frame(main_frame, bg='#F8F9FA')
    button_frame.pack(pady=20)
    
    # Botones
    start_btn = tk.Button(
        button_frame,
        text="▶️ Iniciar Respaldos",
        bg='#28A745',
        fg='white',
        font=('Segoe UI', 10, 'bold'),
        padx=20,
        pady=8,
        relief='flat'
    )
    start_btn.pack(side='left', padx=(0, 10))
    
    stop_btn = tk.Button(
        button_frame,
        text="⏹️ Detener Proceso",
        bg='#DC3545',
        fg='white',
        font=('Segoe UI', 10, 'bold'),
        padx=20,
        pady=8,
        relief='flat'
    )
    stop_btn.pack(side='left')
    
    # Mensaje de confirmación
    status_label = tk.Label(
        main_frame,
        text="✅ ¡Todas las opciones de configuración están visibles!",
        font=('Segoe UI', 11, 'bold'),
        bg='#F8F9FA',
        fg='#28A745'
    )
    status_label.pack(pady=10)
    
    print("🎯 VERIFICACIÓN:")
    print("✅ Ventana creada")
    print("✅ Frame de conexión visible")
    print("✅ Frame de programación visible") 
    print("✅ Botones de control visibles")
    print("🚀 Si puedes ver esta ventana, el problema estaba en el layout complejo.")
    
    root.mainloop()

if __name__ == "__main__":
    test_simple_ui()
