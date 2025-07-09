"""
Integración del validador de herramientas en la aplicación principal.
"""

import subprocess
import sys
import os
from typing import Dict, List


class DatabaseToolsChecker:
    """Verificador rápido de herramientas de base de datos."""
    
    @staticmethod
    def check_sql_server() -> tuple[bool, str]:
        """Verifica disponibilidad de SQL Server."""
        try:
            import pyodbc
            drivers = pyodbc.drivers()
            sql_drivers = [d for d in drivers if 'SQL Server' in d]
            if sql_drivers:
                return True, f"✅ SQL Server disponible ({sql_drivers[0]})"
            else:
                return False, "❌ Driver SQL Server no encontrado"
        except ImportError:
            return False, "❌ pyodbc no instalado"
    
    @staticmethod
    def check_mysql() -> tuple[bool, str]:
        """Verifica disponibilidad de MySQL."""
        try:
            result = subprocess.run(['mysqldump', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return True, "✅ MySQL disponible"
            else:
                return False, "❌ mysqldump no funciona"
        except FileNotFoundError:
            return False, "❌ mysqldump no encontrado"
        except Exception:
            return False, "❌ Error verificando MySQL"
    
    @staticmethod
    def check_postgresql() -> tuple[bool, str]:
        """Verifica disponibilidad de PostgreSQL."""
        try:
            result = subprocess.run(['pg_dump', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return True, "✅ PostgreSQL disponible"
            else:
                return False, "❌ pg_dump no funciona"
        except FileNotFoundError:
            return False, "❌ pg_dump no encontrado"
        except Exception:
            return False, "❌ Error verificando PostgreSQL"
    
    @classmethod
    def get_available_db_types(cls) -> Dict[str, Dict]:
        """Obtiene información de todos los tipos de BD disponibles."""
        checks = {
            'sql_server': ('SQL Server', cls.check_sql_server),
            'mysql': ('MySQL', cls.check_mysql),
            'postgresql': ('PostgreSQL', cls.check_postgresql)
        }
        
        result = {}
        for db_type, (name, check_func) in checks.items():
            available, message = check_func()
            result[db_type] = {
                'name': name,
                'available': available,
                'message': message,
                'display_name': f"{name} ({message})"
            }
        
        return result
    
    @classmethod
    def get_install_instructions(cls, db_type: str) -> str:
        """Obtiene instrucciones de instalación para un tipo de BD."""
        instructions = {
            'mysql': """Para habilitar MySQL:
1. Descargar MySQL Installer: https://dev.mysql.com/downloads/installer/
2. Instalar "MySQL Client Tools"
3. Agregar al PATH: C:\\Program Files\\MySQL\\MySQL Server X.X\\bin
4. Reiniciar la aplicación""",
            
            'postgresql': """Para habilitar PostgreSQL:
1. Descargar PostgreSQL: https://www.postgresql.org/download/windows/
2. Instalar incluyendo "Command Line Tools"
3. Agregar al PATH: C:\\Program Files\\PostgreSQL\\XX\\bin
4. Reiniciar la aplicación""",
            
            'sql_server': """Para habilitar SQL Server:
1. Instalar: pip install pyodbc
2. Descargar ODBC Driver: https://aka.ms/odbc17
3. Ejecutar instalador ODBC Driver
4. Reiniciar la aplicación"""
        }
        
        return instructions.get(db_type, "No se encontraron instrucciones para este motor.")


def show_database_status_dialog(parent=None):
    """Muestra un diálogo con el estado de las herramientas de BD."""
    import tkinter as tk
    from tkinter import ttk, messagebox
    
    # Crear ventana
    dialog = tk.Toplevel(parent) if parent else tk.Tk()
    dialog.title("Estado de Herramientas de Base de Datos")
    dialog.geometry("600x500")
    dialog.resizable(True, True)
    
    # Configurar estilo
    dialog.configure(bg='#f0f0f0')
    
    # Frame principal
    main_frame = ttk.Frame(dialog, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Título
    title_label = ttk.Label(main_frame, text="🔧 Estado de Herramientas de Base de Datos", 
                           font=('Arial', 14, 'bold'))
    title_label.pack(pady=(0, 10))
    
    # Obtener estado
    db_status = DatabaseToolsChecker.get_available_db_types()
    
    # Frame de estado
    status_frame = ttk.LabelFrame(main_frame, text="Estado Actual", padding="10")
    status_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    # Mostrar cada motor
    for db_type, info in db_status.items():
        db_frame = ttk.Frame(status_frame)
        db_frame.pack(fill=tk.X, pady=5)
        
        # Status
        status_label = ttk.Label(db_frame, text=info['message'], font=('Arial', 10))
        status_label.pack(side=tk.LEFT)
        
        # Botón de instrucciones si no está disponible
        if not info['available']:
            def show_instructions(db=db_type):
                instructions = DatabaseToolsChecker.get_install_instructions(db)
                messagebox.showinfo(f"Instalar {info['name']}", instructions)
            
            ttk.Button(db_frame, text="Ver Instrucciones", 
                      command=show_instructions).pack(side=tk.RIGHT)
    
    # Resumen
    available_count = sum(1 for info in db_status.values() if info['available'])
    total_count = len(db_status)
    
    summary_label = ttk.Label(main_frame, 
                             text=f"📊 Resumen: {available_count}/{total_count} motores disponibles",
                             font=('Arial', 11, 'bold'))
    summary_label.pack(pady=(10, 0))
    
    # Botón cerrar
    ttk.Button(main_frame, text="Cerrar", command=dialog.destroy).pack(pady=(10, 0))
    
    # Centrar ventana
    if parent:
        dialog.transient(parent)
        dialog.grab_set()
        
        # Centrar en la ventana padre
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (600 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (500 // 2)
        dialog.geometry(f"600x500+{x}+{y}")
    
    return dialog


if __name__ == "__main__":
    # Prueba del diálogo
    show_database_status_dialog()
