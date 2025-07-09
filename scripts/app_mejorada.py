"""
Aplicación principal de respaldos SQL con detección automática de herramientas.
Versión mejorada que detecta qué motores de BD están disponibles.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from pathlib import Path

# Agregar el directorio actual al path para imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Imports del sistema de respaldos
from src.main import BackupApp
from src.utils.db_tools_checker import DatabaseToolsChecker, show_database_status_dialog
from config.settings import UI_CONFIG


class BackupApplicationWrapper:
    """Wrapper de la aplicación principal con validación de herramientas."""
    
    def __init__(self):
        self.root = None
        self.main_app = None
        self.available_tools = {}
        
    def initialize(self):
        """Inicializa la aplicación con verificación de herramientas."""
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("🗄️ Sistema de Respaldos SQL Multi-Motor")
        self.root.geometry("1200x900")
        self.root.minsize(1000, 700)
        
        # Configurar estilo
        self._configure_styles()
        
        # Verificar herramientas disponibles
        self._check_available_tools()
        
        # Mostrar splash screen con información de herramientas
        self._show_startup_info()
        
        # Crear aplicación principal
        try:
            self.main_app = BackupApp(self.root)
            self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
            
            # Agregar menú de herramientas
            self._add_tools_menu()
            
        except Exception as e:
            messagebox.showerror("Error de Inicialización", 
                               f"Error iniciando la aplicación: {e}")
            self.root.destroy()
            return False
        
        return True
    
    def _configure_styles(self):
        """Configura los estilos de la aplicación."""
        style = ttk.Style()
        
        # Tema general
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        
        # Estilos personalizados
        style.configure('Header.TLabel', 
                       font=('Arial', 16, 'bold'),
                       background=UI_CONFIG['colors']['surface'])
        
        style.configure('Info.TLabel',
                       font=('Arial', 10),
                       background=UI_CONFIG['colors']['surface'])
    
    def _check_available_tools(self):
        """Verifica qué herramientas de BD están disponibles."""
        print("🔍 Verificando herramientas de base de datos...")
        self.available_tools = DatabaseToolsChecker.get_available_db_types()
        
        available_count = sum(1 for tool in self.available_tools.values() if tool['available'])
        print(f"📊 Herramientas disponibles: {available_count}/{len(self.available_tools)}")
        
        for db_type, info in self.available_tools.items():
            status = "✅" if info['available'] else "❌"
            print(f"   {status} {info['name']}: {info['message']}")
    
    def _show_startup_info(self):
        """Muestra información de startup sobre herramientas disponibles."""
        available_dbs = [info['name'] for info in self.available_tools.values() if info['available']]
        missing_dbs = [info['name'] for info in self.available_tools.values() if not info['available']]
        
        if not available_dbs:
            # No hay herramientas disponibles
            result = messagebox.askyesno(
                "Sin Herramientas de BD",
                "⚠️ No se detectaron herramientas de base de datos instaladas.\\n\\n"
                "La aplicación puede ejecutarse, pero no podrá crear respaldos reales.\\n\\n"
                "¿Desea ver las instrucciones de instalación?",
                icon='warning'
            )
            if result:
                show_database_status_dialog(self.root)
        
        elif missing_dbs:
            # Algunas herramientas disponibles, algunas faltantes
            available_str = ", ".join(available_dbs)
            missing_str = ", ".join(missing_dbs)
            
            result = messagebox.askyesno(
                "Herramientas Parcialmente Disponibles",
                f"✅ Disponibles: {available_str}\\n"
                f"❌ Faltantes: {missing_str}\\n\\n"
                "¿Desea ver instrucciones para instalar las herramientas faltantes?",
                icon='info'
            )
            if result:
                show_database_status_dialog(self.root)
        
        else:
            # Todas las herramientas disponibles
            messagebox.showinfo(
                "Sistema Listo",
                f"🎉 Todas las herramientas están disponibles:\\n"
                f"✅ {', '.join(available_dbs)}\\n\\n"
                "El sistema está listo para crear respaldos.",
                icon='info'
            )
    
    def _add_tools_menu(self):
        """Agrega menú de herramientas a la ventana principal."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Herramientas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🔧 Herramientas", menu=tools_menu)
        
        tools_menu.add_command(
            label="📊 Estado de Herramientas BD",
            command=lambda: show_database_status_dialog(self.root)
        )
        
        tools_menu.add_separator()
        
        tools_menu.add_command(
            label="📁 Abrir Carpeta de Respaldos",
            command=self._open_backup_folder
        )
        
        tools_menu.add_command(
            label="🧪 Ejecutar Diagnóstico",
            command=self._run_diagnostics
        )
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Ayuda", menu=help_menu)
        
        help_menu.add_command(
            label="📖 Acerca de",
            command=self._show_about
        )
    
    def _open_backup_folder(self):
        """Abre la carpeta de respaldos en el explorador."""
        backup_path = "C:\\Respaldos_Test"  # Ruta por defecto de las pruebas
        
        if os.path.exists(backup_path):
            os.startfile(backup_path)
        else:
            messagebox.showinfo("Carpeta de Respaldos", 
                               f"La carpeta de respaldos no existe aún.\\n"
                               f"Se creará automáticamente cuando ejecute el primer respaldo.\\n\\n"
                               f"Ruta: {backup_path}")
    
    def _run_diagnostics(self):
        """Ejecuta el script de diagnóstico."""
        try:
            import subprocess
            script_path = current_dir / "diagnostico_detallado_respaldos.py"
            
            if script_path.exists():
                subprocess.Popen([sys.executable, str(script_path)], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
                messagebox.showinfo("Diagnóstico", 
                                   "Script de diagnóstico ejecutado en nueva ventana.")
            else:
                messagebox.showerror("Error", 
                                   f"Script de diagnóstico no encontrado: {script_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error ejecutando diagnóstico: {e}")
    
    def _show_about(self):
        """Muestra información sobre la aplicación."""
        about_text = f"""🗄️ Sistema de Respaldos SQL Multi-Motor
        
Versión: 2.0
Fecha: Julio 2025

Características:
• Soporte para SQL Server, MySQL, PostgreSQL
• Respaldos programados automáticos
• Organización automática por tipo de BD
• Historial de conexiones
• Logs detallados y exportables
• Interfaz moderna y responsive

Estado de Herramientas:"""

        for db_type, info in self.available_tools.items():
            status = "✅" if info['available'] else "❌"
            about_text += f"\\n{status} {info['name']}"

        about_text += f"""

Desarrollado para gestión profesional de respaldos.
        
📁 Carpeta de respaldos: C:\\Respaldos_Test"""

        messagebox.showinfo("Acerca de", about_text)
    
    def _on_closing(self):
        """Maneja el cierre de la aplicación."""
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
            # Detener cualquier programador activo
            if self.main_app and hasattr(self.main_app, 'controller'):
                self.main_app.controller.stop_scheduler()
            
            self.root.destroy()
    
    def run(self):
        """Ejecuta la aplicación."""
        if self.initialize():
            print("🚀 Iniciando aplicación de respaldos...")
            self.root.mainloop()
        else:
            print("❌ Error inicializando la aplicación")


def main():
    """Función principal."""
    print("=" * 60)
    print("🗄️ SISTEMA DE RESPALDOS SQL MULTI-MOTOR")
    print("=" * 60)
    print("Inicializando aplicación...")
    
    try:
        app = BackupApplicationWrapper()
        app.run()
    except KeyboardInterrupt:
        print("\\n🛑 Aplicación interrumpida por el usuario")
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        messagebox.showerror("Error Fatal", f"Error inesperado: {e}")
    finally:
        print("👋 Aplicación finalizada")


if __name__ == "__main__":
    main()
