"""
Diagnóstico detallado del sistema de respaldos.
Este script ejecuta pruebas paso a paso para identificar el problema específico.
"""

import os
import sys
import subprocess
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.database_service import DatabaseService, PathValidator
from src.core.backup_controller import BackupController


def test_basic_file_creation():
    """Prueba básica de creación de archivos."""
    print("=" * 60)
    print("🔧 PRUEBA 1: Creación básica de archivos")
    print("=" * 60)
    
    test_dir = "C:\\Respaldos_Test"
    test_file = os.path.join(test_dir, "test_file.txt")
    
    try:
        # Crear directorio
        os.makedirs(test_dir, exist_ok=True)
        print(f"✅ Directorio creado: {test_dir}")
        
        # Crear archivo de prueba
        with open(test_file, 'w') as f:
            f.write("Archivo de prueba - " + str(datetime.now()))
        
        if os.path.exists(test_file):
            size = os.path.getsize(test_file)
            print(f"✅ Archivo creado exitosamente: {test_file}")
            print(f"📊 Tamaño: {size} bytes")
            
            # Limpiar
            os.remove(test_file)
            print("🧹 Archivo de prueba eliminado")
            return True
        else:
            print("❌ El archivo no se pudo crear")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba básica: {e}")
        return False


def test_sql_server_tools():
    """Prueba la disponibilidad de herramientas de SQL Server."""
    print("\n" + "=" * 60)
    print("🔧 PRUEBA 2: Herramientas de SQL Server")
    print("=" * 60)
    
    # Verificar si pyodbc está disponible
    try:
        import pyodbc
        drivers = pyodbc.drivers()
        print("✅ pyodbc está disponible")
        print(f"📋 Drivers disponibles: {drivers}")
        
        # Verificar driver de SQL Server
        sql_drivers = [d for d in drivers if 'SQL Server' in d]
        if sql_drivers:
            print(f"✅ Driver SQL Server encontrado: {sql_drivers[0]}")
            return True
        else:
            print("❌ No se encontró driver de SQL Server")
            return False
            
    except ImportError as e:
        print(f"❌ pyodbc no está disponible: {e}")
        return False


def test_mysql_tools():
    """Prueba la disponibilidad de herramientas de MySQL."""
    print("\n" + "=" * 60)
    print("🔧 PRUEBA 3: Herramientas de MySQL")
    print("=" * 60)
    
    # Verificar mysqldump
    try:
        result = subprocess.run(['mysqldump', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ mysqldump disponible: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error ejecutando mysqldump: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ mysqldump no encontrado en PATH")
        return False
    except Exception as e:
        print(f"❌ Error verificando mysqldump: {e}")
        return False


def test_postgresql_tools():
    """Prueba la disponibilidad de herramientas de PostgreSQL."""
    print("\n" + "=" * 60)
    print("🔧 PRUEBA 4: Herramientas de PostgreSQL")
    print("=" * 60)
    
    # Verificar pg_dump
    try:
        result = subprocess.run(['pg_dump', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ pg_dump disponible: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error ejecutando pg_dump: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ pg_dump no encontrado en PATH")
        return False
    except Exception as e:
        print(f"❌ Error verificando pg_dump: {e}")
        return False


def test_path_validation():
    """Prueba la validación de rutas."""
    print("\n" + "=" * 60)
    print("🔧 PRUEBA 5: Validación de rutas")
    print("=" * 60)
    
    test_paths = [
        "C:\\Respaldos_Test",
        "C:\\Users\\Public\\Respaldos",
        os.path.expanduser("~/Desktop/Respaldos"),
        "."  # Directorio actual
    ]
    
    results = []
    for path in test_paths:
        try:
            # Crear el directorio si no existe
            abs_path = os.path.abspath(path)
            os.makedirs(abs_path, exist_ok=True)
            
            # Verificar existencia y permisos
            exists = os.path.exists(abs_path)
            writable = os.access(abs_path, os.W_OK) if exists else False
            
            print(f"📁 Ruta: {abs_path}")
            print(f"   Existe: {'✅' if exists else '❌'}")
            print(f"   Escribible: {'✅' if writable else '❌'}")
            
            if exists and writable:
                # Prueba de escritura real
                test_file = os.path.join(abs_path, "test_write.tmp")
                try:
                    with open(test_file, 'w') as f:
                        f.write("test")
                    os.remove(test_file)
                    print(f"   Escritura real: ✅")
                    results.append((abs_path, True))
                except Exception as e:
                    print(f"   Escritura real: ❌ ({e})")
                    results.append((abs_path, False))
            else:
                results.append((abs_path, False))
                
        except Exception as e:
            print(f"❌ Error procesando {path}: {e}")
            results.append((path, False))
    
    return results


def test_backup_with_mock_db():
    """Prueba la creación de respaldos con una base de datos simulada."""
    print("\n" + "=" * 60)
    print("🔧 PRUEBA 6: Simulación de respaldo")
    print("=" * 60)
    
    # Usar una ruta que sabemos que funciona
    backup_dir = "C:\\Respaldos_Test"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Simular la estructura de carpetas que crearía el sistema
    db_types = ['SQL_Server', 'MySQL', 'PostgreSQL']
    
    for db_type in db_types:
        try:
            # Crear subcarpeta
            subfolder = os.path.join(backup_dir, db_type)
            os.makedirs(subfolder, exist_ok=True)
            print(f"✅ Subcarpeta creada: {subfolder}")
            
            # Crear archivo de respaldo simulado
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            extensions = {'SQL_Server': '.bak', 'MySQL': '.sql', 'PostgreSQL': '.dump'}
            ext = extensions.get(db_type, '.bak')
            
            filename = f"test_db_{timestamp}{ext}"
            filepath = os.path.join(subfolder, filename)
            
            # Crear archivo con contenido
            with open(filepath, 'w') as f:
                f.write(f"# Respaldo simulado para {db_type}\n")
                f.write(f"# Creado: {datetime.now()}\n")
                f.write("# Contenido de prueba...\n")
                f.write("SELECT 'Hello World' AS mensaje;\n" * 100)  # Contenido más grande
            
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"✅ Archivo simulado creado: {filename}")
                print(f"📊 Tamaño: {size} bytes")
            else:
                print(f"❌ No se pudo crear archivo para {db_type}")
                
        except Exception as e:
            print(f"❌ Error creando respaldo simulado para {db_type}: {e}")


def show_system_info():
    """Muestra información del sistema."""
    print("\n" + "=" * 60)
    print("🖥️ INFORMACIÓN DEL SISTEMA")
    print("=" * 60)
    
    print(f"🐍 Python: {sys.version}")
    print(f"💻 SO: {os.name}")
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"👤 Usuario: {os.getenv('USERNAME', 'Desconocido')}")
    
    # Variables de entorno relevantes
    path_var = os.getenv('PATH', '')
    mysql_paths = [p for p in path_var.split(';') if 'mysql' in p.lower()]
    postgres_paths = [p for p in path_var.split(';') if 'postgres' in p.lower()]
    
    if mysql_paths:
        print(f"🔧 MySQL en PATH: {mysql_paths}")
    if postgres_paths:
        print(f"🔧 PostgreSQL en PATH: {postgres_paths}")


def main():
    """Función principal del diagnóstico."""
    print("🔍 DIAGNÓSTICO DETALLADO DEL SISTEMA DE RESPALDOS")
    print("=" * 60)
    print("Este script ejecutará varias pruebas para identificar el problema específico.")
    
    show_system_info()
    
    # Ejecutar todas las pruebas
    tests = [
        ("Creación básica de archivos", test_basic_file_creation),
        ("Herramientas SQL Server", test_sql_server_tools),
        ("Herramientas MySQL", test_mysql_tools),
        ("Herramientas PostgreSQL", test_postgresql_tools),
        ("Validación de rutas", test_path_validation),
        ("Simulación de respaldos", test_backup_with_mock_db),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Error ejecutando prueba '{test_name}': {e}")
            results[test_name] = False
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status}: {test_name}")
    
    # Recomendaciones
    print("\n" + "=" * 60)
    print("💡 RECOMENDACIONES")
    print("=" * 60)
    
    if not results.get("Creación básica de archivos"):
        print("🚨 CRÍTICO: No se pueden crear archivos básicos. Verificar permisos del sistema.")
    
    if not results.get("Herramientas SQL Server"):
        print("⚠️ SQL Server: Instalar/configurar drivers ODBC de SQL Server.")
    
    if not results.get("Herramientas MySQL"):
        print("⚠️ MySQL: Instalar MySQL client tools y agregar al PATH.")
    
    if not results.get("Herramientas PostgreSQL"):
        print("⚠️ PostgreSQL: Instalar PostgreSQL client tools y agregar al PATH.")
    
    print("\n🔍 Para continuar el diagnóstico, revise los archivos creados en C:\\Respaldos_Test")


if __name__ == "__main__":
    main()
