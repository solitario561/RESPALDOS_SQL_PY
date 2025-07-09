#!/usr/bin/env python3
"""
Script final para completar la organización de archivos restantes.
"""

import os
import shutil
import sys
from pathlib import Path

def complete_organization():
    """Completa la organización moviendo los archivos restantes."""
    
    root_dir = Path.cwd()
    
    print("🔧 COMPLETANDO ORGANIZACIÓN DE ARCHIVOS")
    print("=" * 50)
    
    # Archivos específicos que quedan por mover
    remaining_moves = [
        # Tests
        ("test_*.py", "tests/"),
        ("prueba_*.py", "tests/"),
        ("check_*.py", "tests/"),
        ("verify_*.py", "tests/"),
        
        # Scripts
        ("diagnostico_*.py", "scripts/"),
        ("validador_*.py", "scripts/"),
        ("ejecutar_*.py", "scripts/"),
        
        # Documentación
        ("*.md", "docs/"),
        ("*.txt", "docs/"),
    ]
    
    moved_count = 0
    
    for pattern, target_dir in remaining_moves:
        target_path = root_dir / target_dir
        
        if "*" in pattern:
            import glob
            matching_files = [f for f in glob.glob(pattern) if os.path.isfile(f)]
        else:
            matching_files = [pattern] if os.path.exists(pattern) and os.path.isfile(pattern) else []
        
        for file_name in matching_files:
            source_path = root_dir / file_name
            dest_path = target_path / file_name
            
            if source_path.exists() and source_path.is_file():
                try:
                    if not dest_path.exists():
                        shutil.move(str(source_path), str(dest_path))
                        print(f"   ✓ {file_name} -> {target_dir}")
                        moved_count += 1
                    else:
                        print(f"   ⚠️  {file_name} ya existe en {target_dir}")
                        
                except Exception as e:
                    print(f"   ❌ Error moviendo {file_name}: {e}")
    
    print(f"\n✅ Se movieron {moved_count} archivos adicionales")
    
    # Mostrar estructura final
    print("\n📁 ESTRUCTURA FINAL:")
    print("=" * 50)
    
    def show_directory_tree(path, prefix="", max_depth=2, current_depth=0):
        if current_depth >= max_depth:
            return
            
        items = sorted([item for item in path.iterdir() if not item.name.startswith('.')])
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item.name}")
            
            if item.is_dir() and current_depth < max_depth - 1:
                next_prefix = prefix + ("    " if is_last else "│   ")
                show_directory_tree(item, next_prefix, max_depth, current_depth + 1)
    
    show_directory_tree(root_dir)
    
    print(f"\n🎯 ARCHIVOS PRINCIPALES PARA USAR:")
    print("=" * 50)
    print("✅ EJECUTAR APLICACIÓN:")
    print("   python run_app_fixed.py")
    print()
    print("🧪 EJECUTAR PRUEBAS:")
    print("   python tests/test_simple_respaldo.py")
    print("   python tests/prueba_final_respaldos.py")
    print()
    print("🔧 DIAGNÓSTICO:")
    print("   python scripts/diagnostico_detallado_respaldos.py")
    print("   python scripts/validador_herramientas_bd.py")
    print()
    print("📚 DOCUMENTACIÓN:")
    print("   Ver archivos en docs/")

if __name__ == "__main__":
    complete_organization()
