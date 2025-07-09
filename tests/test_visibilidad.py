"""
Prueba visual para confirmar que TODAS las opciones son visibles sin scroll.
"""

import sys
import os
import tkinter as tk

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_visibilidad_completa():
    """Prueba que todas las opciones sean visibles en una ventana más grande."""
    
    try:
        from src.main import BackupApp
        
        # Crear ventana más grande
        root = tk.Tk()
        root.title("PRUEBA FINAL - Layout Simplificado - Todas las opciones visibles")
        
        # Crear aplicación
        app = BackupApp(root)
        
        print("✅ Aplicación creada con layout simplificado")
        print(f"📐 Tamaño de ventana: {root.winfo_reqwidth()}x{root.winfo_reqheight()}")
        print("")
        print("🔍 VERIFICACIÓN VISUAL:")
        print("   ✅ ¿Ves el combo de 'Conexiones anteriores'?")
        print("   ✅ ¿Ves el selector de 'Tipo de BD'?")
        print("   ✅ ¿Ves los campos de Servidor y Puerto?")
        print("   ✅ ¿Ves los campos de Usuario y Contraseña?")
        print("   ✅ ¿Ves el botón 'Validar Conexión'?")
        print("   ✅ ¿Ves el botón 'Cargar Bases de Datos'?")
        print("   ✅ ¿Ves la lista de selección de bases de datos?")
        print("   ✅ ¿Ves el campo 'Ruta de Respaldo'?")
        print("   ✅ ¿Ves el botón 'Validar Ruta'?")
        print("   ✅ ¿Ves el selector de 'Frecuencia'?")
        print("   ✅ ¿Ves el campo de 'Hora'?")
        print("   ✅ ¿Ves los botones 'Iniciar/Detener'?")
        print("   ✅ ¿Ves el área de logs en la parte inferior?")
        print("")
        print("📝 Si puedes ver TODAS estas opciones sin hacer scroll,")
        print("   ¡el problema está resuelto!")
        
        # Mensaje de log para verificar funcionalidad
        app._log_message("🎉 Aplicación iniciada correctamente - Todas las opciones son visibles")
        app._log_message("📋 Verifica que puedas ver todas las secciones de configuración")
        app._log_message("🔧 Layout simplificado sin problemas de scroll")
        
        def mostrar_resultado():
            print("")
            print("🎯 RESULTADO DE LA PRUEBA:")
            if input("¿Puedes ver TODAS las opciones de configuración? (s/n): ").lower() == 's':
                print("🎉 ¡ÉXITO! El problema ha sido resuelto completamente.")
                print("✅ Todas las configuraciones son visibles")
                print("✅ No se requiere scroll")
                print("✅ Layout optimizado")
            else:
                print("❌ Aún hay problemas de visibilidad")
                print("💡 Posibles soluciones:")
                print("   - Aumentar más el tamaño de ventana")
                print("   - Reducir el tamaño de algunos componentes")
                print("   - Reorganizar el layout")
            
            root.destroy()
        
        # Programar verificación manual
        root.after(3000, mostrar_resultado)
        
        # Ejecutar
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎯 PRUEBA FINAL DE VISIBILIDAD SIN SCROLL")
    print("=" * 50)
    test_visibilidad_completa()
