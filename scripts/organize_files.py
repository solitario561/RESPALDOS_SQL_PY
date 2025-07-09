#!/usr/bin/env python3
"""
Script para organizar y mover archivos a sus ubicaciones correctas.
"""

import os
import shutil
import sys
from pathlib import Path

def organize_files():
    """Organiza todos los archivos dispersos en sus carpetas correctas."""
    
    # Obtener el directorio raíz del proyecto
    root_dir = Path.cwd()
    
    print("🗂️ ORGANIZANDO ARCHIVOS EN ESTRUCTURA MODULAR")
    print("=" * 60)
    print(f"Directorio raíz: {root_dir}")
    
    # Definir los movimientos a realizar
    moves = [
        # SCRIPTS DE PRUEBA -> tests/
        ("test_*.py", "tests/"),
        ("prueba_*.py", "tests/"),
        ("check_*.py", "tests/"),
        ("verify_*.py", "tests/"),
        
        # SCRIPTS DE DIAGNÓSTICO -> scripts/
        ("diagnostico_*.py", "scripts/"),
        ("validador_*.py", "scripts/"),
        ("demo_*.py", "scripts/"),
        ("ejecutar_*.py", "scripts/"),
        
        # ARCHIVOS DE APLICACIÓN ANTIGUOS -> scripts/deprecated/
        ("app_*.py", "scripts/deprecated/"),
        ("main.py", "scripts/deprecated/"),  # El main.py viejo
        
        # MÓDULOS ANTIGUOS -> src/deprecated/
        ("backup_controller.py", "src/deprecated/"),
        ("database_service.py", "src/deprecated/"),
        ("file_service.py", "src/deprecated/"),
        ("ui_components.py", "src/deprecated/"),
        ("config.py", "src/deprecated/"),
        
        # DOCUMENTACIÓN -> docs/
        ("*.md", "docs/"),
        ("*.txt", "docs/"),
        
        # LOGS -> data/logs/
        ("*.log", "data/logs/"),
    ]
    
    # Crear directorios necesarios
    directories_to_create = [
        "tests",
        "scripts", 
        "scripts/deprecated",
        "src/deprecated",
        "docs",
        "data/logs"
    ]
    
    print("\n📁 Creando directorios necesarios...")
    for dir_path in directories_to_create:
        full_path = root_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {dir_path}/")
    
    # Realizar los movimientos
    moved_files = []
    errors = []
    
    print("\n🚚 Moviendo archivos...")
    
    for pattern, target_dir in moves:
        target_path = root_dir / target_dir
        
        if "*" in pattern:
            # Buscar archivos que coincidan con el patrón
            import glob
            matching_files = glob.glob(pattern)
        else:
            # Archivo específico
            matching_files = [pattern] if os.path.exists(pattern) else []
        
        for file_name in matching_files:
            source_path = root_dir / file_name
            dest_path = target_path / file_name
            
            if source_path.exists() and source_path != dest_path:
                try:
                    # Verificar que no existe ya en el destino
                    if dest_path.exists():
                        print(f"   ⚠️  {file_name} ya existe en {target_dir}, omitiendo...")
                        continue
                    
                    # Mover archivo
                    shutil.move(str(source_path), str(dest_path))
                    moved_files.append((file_name, target_dir))
                    print(f"   ✓ {file_name} -> {target_dir}")
                    
                except Exception as e:
                    errors.append((file_name, str(e)))
                    print(f"   ❌ Error moviendo {file_name}: {e}")
    
    # Manejar archivos especiales
    special_moves = [
        # Scripts de ejecución principales
        ("run_app.py", "scripts/deprecated/"),
        ("test_final.py", "tests/"),
        ("test_final_confirmatorio.py", "tests/"),
    ]
    
    print("\n🔧 Moviendo archivos especiales...")
    for file_name, target_dir in special_moves:
        source_path = root_dir / file_name
        target_path = root_dir / target_dir / file_name
        
        if source_path.exists():
            try:
                if target_path.exists():
                    print(f"   ⚠️  {file_name} ya existe en {target_dir}, omitiendo...")
                    continue
                    
                shutil.move(str(source_path), str(target_path))
                moved_files.append((file_name, target_dir))
                print(f"   ✓ {file_name} -> {target_dir}")
                
            except Exception as e:
                errors.append((file_name, str(e)))
                print(f"   ❌ Error moviendo {file_name}: {e}")
    
    # Crear archivo README en deprecated
    print("\n📝 Creando documentación...")
    
    deprecated_readme = root_dir / "scripts/deprecated/README.md"
    with open(deprecated_readme, 'w', encoding='utf-8') as f:
        f.write("""# Archivos Deprecados

Esta carpeta contiene archivos de versiones anteriores del proyecto que ya no se usan.

## Contenido:
- `app_*.py` - Versiones anteriores de la aplicación
- `main.py` - Versión anterior del archivo principal
- `run_app.py` - Scripts de ejecución anteriores

## Estado:
❌ **DEPRECADO** - No usar estos archivos

## Versión Actual:
✅ Usar `run_app_fixed.py` en el directorio raíz
""")
    
    src_deprecated_readme = root_dir / "src/deprecated/README.md"
    with open(src_deprecated_readme, 'w', encoding='utf-8') as f:
        f.write("""# Módulos Deprecados

Esta carpeta contiene módulos de versiones anteriores que han sido reemplazados.

## Contenido:
- Módulos individuales que ahora están organizados en subcarpetas
- Versiones anteriores de controladores y servicios

## Estado:
❌ **DEPRECADO** - No usar estos módulos

## Versión Actual:
✅ Usar los módulos en `src/core/`, `src/services/`, `src/ui/`
""")
    
    # Reporte final
    print("\n" + "=" * 60)
    print("📊 REPORTE DE ORGANIZACIÓN")
    print("=" * 60)
    
    print(f"\n✅ Archivos movidos exitosamente: {len(moved_files)}")
    for file_name, target in moved_files:
        print(f"   • {file_name} -> {target}")
    
    if errors:
        print(f"\n❌ Errores encontrados: {len(errors)}")
        for file_name, error in errors:
            print(f"   • {file_name}: {error}")
    
    print(f"\n📁 Estructura final recomendada:")
    print("   • tests/ - Todos los archivos de prueba")
    print("   • scripts/ - Scripts de diagnóstico y utilidades")
    print("   • scripts/deprecated/ - Archivos antiguos")
    print("   • src/deprecated/ - Módulos antiguos")
    print("   • docs/ - Documentación")
    print("   • data/logs/ - Archivos de log")
    
    print(f"\n🎉 ¡Organización completada!")
    print(f"💡 Para ejecutar la aplicación, usa: python run_app_fixed.py")

def main():
    """Función principal."""
    print("¿Desea proceder con la organización de archivos? (s/n): ", end="")
    response = input().lower().strip()
    
    if response in ['s', 'sí', 'si', 'y', 'yes']:
        organize_files()
    else:
        print("Organización cancelada.")

if __name__ == "__main__":
    main()
