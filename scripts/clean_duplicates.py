#!/usr/bin/env python3
"""
Script para limpiar archivos duplicados en el directorio raíz.
"""

import os
import shutil
from pathlib import Path

def clean_duplicates():
    """Limpia archivos duplicados del directorio raíz."""
    
    root_dir = Path.cwd()
    
    print("🧹 LIMPIANDO ARCHIVOS DUPLICADOS")
    print("=" * 50)
    
    # Archivos que existen tanto en raíz como en subcarpetas
    files_to_remove = [
        # Tests que ya están en tests/
        "test_app.py",
        "test_backup_system.py", 
        "test_dimensions.py",
        "test_final.py",
        "test_final_confirmatorio.py",
        "test_respaldo_real.py",
        "test_respaldo_sql_server.py",
        "test_simple.py",
        "test_simple_respaldo.py",
        "test_ui_simple.py",
        "test_ui_visual.py",
        "test_visibilidad.py",
        "prueba_final_respaldos.py",
        "check_implementation.py",
        "verify_structure.py",
        
        # Scripts que ya están en scripts/
        "diagnostico_detallado_respaldos.py",
        "diagnostico_respaldos.py",
        "validador_herramientas_bd.py",
        "ejecutar_app.py",
        
        # Documentación que ya está en docs/
        "CONFIGURACION_COMPLETA.md",
        "DISEÑO_MODERNO_COMPLETADO.md",
        "LAYOUT_ARREGLADO.md",
        "PROBLEMA_RESUELTO.md",
        "REORGANIZACION_COMPLETADA.md",
        "SOLUCION_FINAL.md",
        "IMPLEMENTACION_COMPLETADA.txt",
        "REPORTE_PRUEBAS.txt",
    ]
    
    removed_count = 0
    
    print("Removiendo duplicados del directorio raíz...")
    
    for file_name in files_to_remove:
        file_path = root_dir / file_name
        
        if file_path.exists() and file_path.is_file():
            try:
                # Verificar que existe la copia en la ubicación correcta
                if file_name.startswith('test_') or file_name.startswith('prueba_') or file_name.startswith('check_') or file_name.startswith('verify_'):
                    target_exists = (root_dir / "tests" / file_name).exists()
                elif file_name.startswith('diagnostico_') or file_name.startswith('validador_') or file_name.startswith('ejecutar_'):
                    target_exists = (root_dir / "scripts" / file_name).exists()
                elif file_name.endswith('.md') or file_name.endswith('.txt'):
                    target_exists = (root_dir / "docs" / file_name).exists()
                else:
                    target_exists = False
                
                if target_exists:
                    file_path.unlink()
                    print(f"   ✓ Removido: {file_name}")
                    removed_count += 1
                else:
                    print(f"   ⚠️  {file_name} no tiene copia en destino, manteniendo...")
                    
            except Exception as e:
                print(f"   ❌ Error removiendo {file_name}: {e}")
    
    # Limpiar __pycache__ obsoleto
    pycache_dir = root_dir / "__pycache__"
    if pycache_dir.exists():
        try:
            shutil.rmtree(pycache_dir)
            print(f"   ✓ Removido: __pycache__/")
            removed_count += 1
        except Exception as e:
            print(f"   ❌ Error removiendo __pycache__: {e}")
    
    print(f"\n✅ Se removieron {removed_count} archivos/carpetas duplicados")
    
    # Mostrar estructura limpia final
    print(f"\n📁 ESTRUCTURA FINAL LIMPIA:")
    print("=" * 50)
    
    important_items = [
        "run_app_fixed.py",
        "config/",
        "src/",
        "tests/",
        "scripts/", 
        "docs/",
        "data/"
    ]
    
    for item in important_items:
        path = root_dir / item
        if path.exists():
            if path.is_dir():
                file_count = len([f for f in path.rglob('*') if f.is_file()])
                print(f"   📁 {item} ({file_count} archivos)")
            else:
                print(f"   📄 {item}")
        else:
            print(f"   ❌ {item} (no existe)")
    
    print(f"\n🎯 COMANDOS PRINCIPALES:")
    print("=" * 30)
    print("▶️  Ejecutar aplicación:")
    print("    python run_app_fixed.py")
    print()
    print("🧪 Ejecutar pruebas:")
    print("    python tests/test_simple_respaldo.py")
    print()
    print("🔧 Diagnóstico:")
    print("    python scripts/diagnostico_detallado_respaldos.py")
    print()
    print("📚 Ver documentación:")
    print("    dir docs")

if __name__ == "__main__":
    print("¿Desea limpiar archivos duplicados? (s/n): ", end="")
    response = input().lower().strip()
    
    if response in ['s', 'sí', 'si', 'y', 'yes']:
        clean_duplicates()
    else:
        print("Limpieza cancelada.")
