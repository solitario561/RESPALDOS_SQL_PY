"""
Script para verificar dimensiones y scroll de la interfaz.
"""

import sys
import os
import tkinter as tk

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_scroll_and_dimensions():
    """Verifica si necesitamos scroll o si todo es visible."""
    
    try:
        from src.main import BackupApp
        
        # Crear ventana con tamaño específico
        root = tk.Tk()
        root.geometry("1000x700")
        root.title("PRUEBA SCROLL - Verificar todas las configuraciones")
        
        # Crear aplicación
        app = BackupApp(root)
        
        # Actualizar para obtener dimensiones reales
        root.update_idletasks()
        
        # Información de la ventana
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        
        print(f"📐 Dimensiones de ventana: {window_width}x{window_height}")
        
        # Verificar el frame de conexión
        if hasattr(app, 'connection_frame'):
            cf = app.connection_frame
            frame_height = cf.frame.winfo_reqheight()
            frame_width = cf.frame.winfo_reqwidth()
            
            print(f"📋 Frame de conexión: {frame_width}x{frame_height}")
            
            # Verificar si necesitamos scroll
            if frame_height > (window_height - 150):  # 150 para botones y logs
                print("⚠️ PROBLEMA: El frame de conexión es muy alto, algunas opciones podrían no ser visibles")
                print("💡 SOLUCIÓN: Necesitamos agregar scroll o reorganizar el layout")
            else:
                print("✅ El frame de conexión debería ser completamente visible")
        
        # Verificar todos los widgets hijos del frame de conexión
        if hasattr(app, 'connection_frame'):
            children = app.connection_frame.frame.winfo_children()
            print(f"\n🔢 Número de widgets en el frame de conexión: {len(children)}")
            
            # Lista de elementos que deberían estar presentes
            expected_elements = [
                "history_combo", "db_type_combo", "server_var", "port_entry",
                "user_var", "pwd_var", "db_listbox", "path_var", 
                "freq_menu", "time_entry"
            ]
            
            present_elements = []
            for element in expected_elements:
                if hasattr(app.connection_frame, element):
                    present_elements.append(element)
                    print(f"   ✅ {element}")
                else:
                    print(f"   ❌ {element} - FALTANTE")
            
            print(f"\n📊 Elementos presentes: {len(present_elements)}/{len(expected_elements)}")
            
            if len(present_elements) == len(expected_elements):
                print("🎉 ¡TODOS los elementos de configuración están presentes!")
            else:
                print("⚠️ Faltan algunos elementos de configuración")
        
        # Mantener la ventana abierta por unos segundos para inspección visual
        def close_window():
            print("\n🔍 INSPECCIÓN VISUAL COMPLETADA")
            print("Si todas las secciones están visibles en la ventana, ¡todo funciona correctamente!")
            root.destroy()
        
        root.after(8000, close_window)  # Cerrar después de 8 segundos
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Verificando dimensiones y visibilidad de todos los componentes...")
    test_scroll_and_dimensions()
