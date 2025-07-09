"""
Sistema mejorado de validación de herramientas de base de datos.
Detecta automáticamente qué herramientas están disponibles y proporciona información clara.
"""

import subprocess
import os
import sys
from typing import Dict, List, Tuple


class DatabaseToolsValidator:
    """Validador de herramientas de base de datos disponibles en el sistema."""
    
    def __init__(self):
        self.available_tools = {}
        self.missing_tools = {}
        self.scan_results = {}
        
    def scan_all_tools(self) -> Dict[str, Dict]:
        """Escanea todas las herramientas de base de datos disponibles."""
        tools_config = {
            'sql_server': {
                'name': 'SQL Server',
                'requirements': ['pyodbc', 'driver'],
                'client_tool': None,
                'description': 'Microsoft SQL Server con drivers ODBC'
            },
            'mysql': {
                'name': 'MySQL',
                'requirements': ['mysqldump'],
                'client_tool': 'mysqldump',
                'description': 'MySQL con herramientas cliente'
            },
            'postgresql': {
                'name': 'PostgreSQL', 
                'requirements': ['pg_dump'],
                'client_tool': 'pg_dump',
                'description': 'PostgreSQL con herramientas cliente'
            }
        }
        
        for db_type, config in tools_config.items():
            result = self._check_database_tools(db_type, config)
            self.scan_results[db_type] = result
            
            if result['available']:
                self.available_tools[db_type] = result
            else:
                self.missing_tools[db_type] = result
        
        return self.scan_results
    
    def _check_database_tools(self, db_type: str, config: Dict) -> Dict:
        """Verifica las herramientas para un tipo específico de base de datos."""
        result = {
            'db_type': db_type,
            'name': config['name'],
            'description': config['description'],
            'available': False,
            'details': [],
            'missing': [],
            'install_instructions': ''
        }
        
        if db_type == 'sql_server':
            return self._check_sql_server_tools(result)
        elif db_type == 'mysql':
            return self._check_mysql_tools(result)
        elif db_type == 'postgresql':
            return self._check_postgresql_tools(result)
        
        return result
    
    def _check_sql_server_tools(self, result: Dict) -> Dict:
        """Verifica herramientas específicas de SQL Server."""
        try:
            # Verificar pyodbc
            import pyodbc
            result['details'].append("✅ pyodbc disponible")
            
            # Verificar drivers
            drivers = pyodbc.drivers()
            sql_drivers = [d for d in drivers if 'SQL Server' in d]
            
            if sql_drivers:
                result['details'].append(f"✅ Driver SQL Server: {sql_drivers[0]}")
                result['available'] = True
            else:
                result['missing'].append("❌ Driver SQL Server no encontrado")
                result['install_instructions'] = """
Instalar Microsoft ODBC Driver for SQL Server:
1. Descargar desde: https://aka.ms/odbc17
2. Ejecutar el instalador
3. Reiniciar la aplicación
"""
                
        except ImportError:
            result['missing'].append("❌ pyodbc no está instalado")
            result['install_instructions'] = """
Instalar pyodbc:
1. pip install pyodbc
2. Instalar Microsoft ODBC Driver for SQL Server
"""
        
        return result
    
    def _check_mysql_tools(self, result: Dict) -> Dict:
        """Verifica herramientas específicas de MySQL."""
        try:
            # Verificar mysqldump
            output = subprocess.run(['mysqldump', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if output.returncode == 0:
                version_info = output.stdout.strip()
                result['details'].append(f"✅ mysqldump: {version_info}")
                result['available'] = True
            else:
                result['missing'].append("❌ mysqldump no funciona correctamente")
                
        except FileNotFoundError:
            result['missing'].append("❌ mysqldump no encontrado en PATH")
            result['install_instructions'] = """
Instalar MySQL Client Tools:

OPCIÓN 1 - MySQL Installer (Recomendado):
1. Descargar MySQL Installer desde: https://dev.mysql.com/downloads/installer/
2. Ejecutar e instalar "MySQL Client Tools"
3. Agregar C:\\Program Files\\MySQL\\MySQL Server X.X\\bin al PATH del sistema

OPCIÓN 2 - Chocolatey:
1. choco install mysql.utilities

OPCIÓN 3 - Scoop:
1. scoop install mysql

Después de instalar, reiniciar PowerShell/CMD.
"""
        except Exception as e:
            result['missing'].append(f"❌ Error verificando mysqldump: {e}")
        
        return result
    
    def _check_postgresql_tools(self, result: Dict) -> Dict:
        """Verifica herramientas específicas de PostgreSQL."""
        try:
            # Verificar pg_dump
            output = subprocess.run(['pg_dump', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if output.returncode == 0:
                version_info = output.stdout.strip()
                result['details'].append(f"✅ pg_dump: {version_info}")
                result['available'] = True
            else:
                result['missing'].append("❌ pg_dump no funciona correctamente")
                
        except FileNotFoundError:
            result['missing'].append("❌ pg_dump no encontrado en PATH")
            result['install_instructions'] = """
Instalar PostgreSQL Client Tools:

OPCIÓN 1 - PostgreSQL Official Installer:
1. Descargar desde: https://www.postgresql.org/download/windows/
2. Ejecutar instalador y seleccionar "Command Line Tools"
3. Agregar C:\\Program Files\\PostgreSQL\\XX\\bin al PATH del sistema

OPCIÓN 2 - Chocolatey:
1. choco install postgresql

OPCIÓN 3 - Scoop:
1. scoop install postgresql

Después de instalar, reiniciar PowerShell/CMD.
"""
        except Exception as e:
            result['missing'].append(f"❌ Error verificando pg_dump: {e}")
        
        return result
    
    def get_available_databases(self) -> List[str]:
        """Retorna lista de tipos de base de datos disponibles."""
        return list(self.available_tools.keys())
    
    def get_missing_databases(self) -> List[str]:
        """Retorna lista de tipos de base de datos no disponibles."""
        return list(self.missing_tools.keys())
    
    def print_report(self):
        """Imprime un reporte detallado del estado de las herramientas."""
        print("🔧 REPORTE DE HERRAMIENTAS DE BASE DE DATOS")
        print("=" * 60)
        
        if self.available_tools:
            print("✅ HERRAMIENTAS DISPONIBLES:")
            for db_type, info in self.available_tools.items():
                print(f"\\n🎯 {info['name']} ({db_type})")
                for detail in info['details']:
                    print(f"   {detail}")
        
        if self.missing_tools:
            print("\\n❌ HERRAMIENTAS FALTANTES:")
            for db_type, info in self.missing_tools.items():
                print(f"\\n⚠️ {info['name']} ({db_type})")
                for missing in info['missing']:
                    print(f"   {missing}")
                if info['install_instructions']:
                    print(f"\\n💡 INSTRUCCIONES DE INSTALACIÓN:")
                    print(info['install_instructions'])
        
        # Resumen
        total = len(self.available_tools) + len(self.missing_tools)
        available_count = len(self.available_tools)
        
        print("\\n" + "=" * 60)
        print("📊 RESUMEN:")
        print(f"   Total de motores: {total}")
        print(f"   Disponibles: {available_count}")
        print(f"   Faltantes: {len(self.missing_tools)}")
        
        if available_count > 0:
            print(f"\\n🚀 PUEDE USAR: {', '.join([info['name'] for info in self.available_tools.values()])}")
        
        if self.missing_tools:
            print(f"⚠️ PARA HABILITAR: {', '.join([info['name'] for info in self.missing_tools.values()])}")
            print("   Siga las instrucciones de instalación mostradas arriba")


def main():
    """Función principal para ejecutar el validador."""
    print("🔍 VALIDADOR DE HERRAMIENTAS DE BASE DE DATOS")
    print("=" * 60)
    print("Escaneando herramientas disponibles en el sistema...")
    print()
    
    validator = DatabaseToolsValidator()
    results = validator.scan_all_tools()
    
    validator.print_report()
    
    # Información adicional
    print("\\n" + "=" * 60)
    print("📝 NOTAS IMPORTANTES:")
    print("• Este sistema funcionará con cualquier motor que esté disponible")
    print("• SQL Server usa drivers ODBC nativos de Windows") 
    print("• MySQL y PostgreSQL requieren herramientas cliente específicas")
    print("• Después de instalar herramientas, reinicie la aplicación")
    print("• Para soporte completo, instale todos los client tools")


if __name__ == "__main__":
    main()
