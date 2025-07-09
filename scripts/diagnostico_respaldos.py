"""
Script de diagnóstico para el sistema de respaldos.
Verifica paso a paso qué está ocurriendo durante el proceso de respaldo.
"""

import sys
import os
import tempfile
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def diagnóstico_respaldos():
    """Diagnóstica el proceso de respaldos paso a paso."""
    
    print("🔍 DIAGNÓSTICO DEL SISTEMA DE RESPALDOS")
    print("=" * 60)
    
    try:
        from src.services.database_service import DatabaseService
        
        # Crear carpeta de prueba
        carpeta_prueba = os.path.join(os.getcwd(), "diagnostico_respaldos")
        os.makedirs(carpeta_prueba, exist_ok=True)
        print(f"📁 Carpeta de prueba creada: {carpeta_prueba}")
        
        # Simular el proceso para SQL Server
        print(f"\n🗄️ Simulando respaldo SQL Server...")
        
        # Crear servicio simulado
        service = DatabaseService('sql_server', 'localhost', 'sa', 'password', 1433)
        
        # Replicar la lógica de create_backup
        database = "TestDB"
        backup_path = carpeta_prueba
        
        print(f"📋 Parámetros:")
        print(f"   - Base de datos: {database}")
        print(f"   - Ruta base: {backup_path}")
        print(f"   - Tipo BD: {service.db_type}")
        
        # Paso 1: Crear subcarpeta
        db_type_folder = {
            'sql_server': 'SQL_Server',
            'mysql': 'MySQL', 
            'postgresql': 'PostgreSQL'
        }.get(service.db_type, 'Unknown')
        
        full_backup_path = os.path.join(backup_path, db_type_folder)
        print(f"📂 Subcarpeta calculada: {full_backup_path}")
        
        # Crear la carpeta
        os.makedirs(full_backup_path, exist_ok=True)
        print(f"✅ Subcarpeta creada: {os.path.exists(full_backup_path)}")
        
        # Paso 2: Generar nombre de archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_extension = service.config.get('file_extension', '.bak')
        filename = f"{database}_{timestamp}{file_extension}"
        fullpath = os.path.join(full_backup_path, filename)
        
        print(f"📄 Archivo calculado:")
        print(f"   - Timestamp: {timestamp}")
        print(f"   - Extensión: {file_extension}")
        print(f"   - Nombre: {filename}")
        print(f"   - Ruta completa: {fullpath}")
        
        # Paso 3: Simular creación de archivo (sin conexión real)
        print(f"\n🔧 Simulando creación de archivo...")
        
        try:
            # Crear archivo de prueba
            with open(fullpath, 'w') as f:
                f.write(f"-- Respaldo simulado de {database}\n")
                f.write(f"-- Creado el {datetime.now()}\n")
                f.write(f"-- Ruta: {fullpath}\n")
                f.write("-- Este es un archivo de prueba\n")
            
            print(f"✅ Archivo creado exitosamente")
            print(f"📊 Tamaño: {os.path.getsize(fullpath)} bytes")
            print(f"📁 Existe: {os.path.exists(fullpath)}")
            
        except Exception as e:
            print(f"❌ Error creando archivo: {e}")
            return False
        
        # Verificar estructura final
        print(f"\n📁 ESTRUCTURA FINAL:")
        for root, dirs, files in os.walk(carpeta_prueba):
            level = root.replace(carpeta_prueba, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                print(f"{subindent}{file} ({size} bytes)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en diagnóstico: {e}")
        import traceback
        traceback.print_exc()
        return False

def diagnóstico_conexión_real():
    """Diagnóstica una conexión real (si el usuario proporciona datos)."""
    
    print(f"\n🔗 DIAGNÓSTICO DE CONEXIÓN REAL")
    print("=" * 40)
    
    # Solicitar datos de conexión
    print("Para probar con conexión real, proporciona:")
    servidor = input("Servidor (Enter para omitir): ").strip()
    
    if not servidor:
        print("⏭️ Omitiendo prueba de conexión real")
        return True
    
    usuario = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()
    
    try:
        from src.services.database_service import DatabaseService
        
        # Crear servicio real
        service = DatabaseService('sql_server', servidor, usuario, password, 1433)
        
        print(f"🔄 Probando conexión...")
        
        # Probar conexión
        if service.test_connection():
            print(f"✅ Conexión exitosa")
            
            # Obtener bases de datos
            databases = service.get_databases()
            print(f"📊 Bases de datos encontradas: {len(databases)}")
            for db in databases[:5]:  # Mostrar solo las primeras 5
                print(f"   - {db}")
            
            if databases:
                # Probar respaldo de la primera BD
                test_db = databases[0]
                carpeta_respaldo = os.path.join(os.getcwd(), "respaldo_real_test")
                
                print(f"\n📦 Probando respaldo real de: {test_db}")
                print(f"📁 Carpeta destino: {carpeta_respaldo}")
                
                try:
                    resultado = service.create_backup(test_db, carpeta_respaldo)
                    print(f"✅ Respaldo exitoso: {resultado}")
                    print(f"📊 Tamaño: {os.path.getsize(resultado)} bytes")
                    
                except Exception as e:
                    print(f"❌ Error en respaldo: {e}")
            
        else:
            print(f"❌ Error de conexión")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Diagnóstico básico (simulado)
    exito1 = diagnóstico_respaldos()
    
    if exito1:
        print(f"\n" + "=" * 60)
        print("🎯 DIAGNÓSTICO COMPLETADO")
        print("✅ La lógica de creación de carpetas y archivos funciona")
        print("📋 El problema podría estar en:")
        print("   1. Conexión a la base de datos")
        print("   2. Permisos en la carpeta destino")
        print("   3. Validación de rutas")
        print("   4. Comandos de respaldo específicos")
        
        # Ofrecer diagnóstico de conexión real
        respuesta = input("\n¿Quieres probar con conexión real? (s/n): ").lower()
        if respuesta == 's':
            diagnóstico_conexión_real()
    
    input("\nPresiona Enter para finalizar...")
