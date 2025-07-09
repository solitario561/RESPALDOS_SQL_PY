"""
APLICACIÓN DE RESPALDOS SQL - VERSIÓN FINAL
===========================================

🎉 ¡PROBLEMA RESUELTO! 

El problema era que el frame de configuración era demasiado alto (743px) 
para la ventana estándar (700px), causando que algunas opciones de 
configuración no fueran visibles.

✅ SOLUCIÓN IMPLEMENTADA:
- Se agregó SCROLL al área de configuración
- Ahora TODAS las opciones son accesibles
- Layout optimizado con PanedWindow
- Scroll con rueda del mouse habilitado

📋 TODAS LAS CONFIGURACIONES AHORA VISIBLES:
✅ 📚 Historial de conexiones anteriores
✅ 🗄️ Tipo de base de datos (SQL Server, MySQL, PostgreSQL)
✅ 🖥️ Servidor y puerto
✅ 👤 Usuario y contraseña  
✅ 🔄 Botón cargar bases de datos
✅ 💾 Lista de selección múltiple de bases de datos
✅ 📁 Ruta de respaldo
✅ ⏰ Programación (frecuencia y hora)
✅ 🎛️ Botones de control (Iniciar/Detener)
✅ 📋 Área de logs

🚀 CARACTERÍSTICAS COMPLETAS:
- Soporte para SQL Server, MySQL y PostgreSQL
- Conexiones con historial persistente
- Selección múltiple de bases de datos
- Programación automática de respaldos
- Logs persistentes con exportación
- Interfaz moderna y profesional
- Scroll para accesibilidad total

📝 PARA USAR LA APLICACIÓN:
python run_app.py

¡La aplicación está lista y todas las opciones son completamente accesibles!
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Ejecuta la aplicación principal con todas las configuraciones visibles."""
    
    print("🚀 Iniciando Aplicación de Respaldos SQL...")
    print("📋 Todas las opciones de configuración están disponibles")
    print("🖱️ Usa la rueda del mouse para scroll si es necesario")
    print("=" * 60)
    
    try:
        import tkinter as tk
        from src.main import BackupApp
        
        # Crear y configurar la ventana principal
        root = tk.Tk()
        
        # Crear la aplicación
        app = BackupApp(root)
        
        print("✅ Aplicación iniciada exitosamente")
        print("🔍 Verifica que puedas ver todas las secciones:")
        print("   - Conexiones anteriores")
        print("   - Configuración de conexión")
        print("   - Selección de bases de datos")
        print("   - Configuración de respaldo")
        print("   - Programación de respaldos")
        print("   - Botones de control")
        print("   - Logs")
        
        # Ejecutar la aplicación
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
