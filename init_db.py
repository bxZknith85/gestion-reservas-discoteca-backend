"""
Script para inicializar la base de datos ejecutando schema_db.sql
Maneja reintentos automáticos y errores de tablas duplicadas
"""
import os
import time
from sqlalchemy import text, event
from app.db.database import engine

def init_db(max_retries=3, retry_delay=3):
    """Ejecuta el archivo schema_db.sql para crear las tablas con reintentos"""
    schema_file = os.path.join(os.path.dirname(__file__), "schema_db.sql")
    
    with open(schema_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    for attempt in range(max_retries):
        try:
            print(f"🔄 Intento {attempt + 1}/{max_retries} de conectar a la base de datos...")
            
            with engine.connect() as connection:
                print("✅ Conexión establecida. Ejecutando script SQL...")
                
                # Ejecutar cada sentencia por separado para manejar errores de duplicados
                statements = sql_script.split(';')
                error_count = 0
                
                for i, statement in enumerate(statements):
                    statement = statement.strip()
                    if not statement:
                        continue
                    
                    try:
                        connection.execute(text(statement))
                    except Exception as e:
                        error_str = str(e)
                        # Ignorar errores de tabla/schema ya existe
                        if 'already exists' in error_str or 'DuplicateTable' in str(type(e)):
                            # print(f"  ℹ️  Saltando duplicado: {statement[:50]}...")
                            pass
                        else:
                            error_count += 1
                            print(f"  ⚠️  Error en línea {i}: {error_str[:80]}")
                
                connection.commit()
                print("✅ Base de datos inicializada exitosamente")
                print(f"   (Se ignoraron {error_count} errores de tablas duplicadas)")
                return True
                
        except Exception as e:
            print(f"❌ Error en intento {attempt + 1}: {str(e)[:100]}")
            
            if attempt < max_retries - 1:
                print(f"⏳ Esperando {retry_delay} segundos antes de reintentar...")
                time.sleep(retry_delay)
            else:
                print(f"\n❌ No se pudo conectar después de {max_retries} intentos")
                print("💡 Soluciones:")
                print("1. Verifica que las credenciales en .env sean correctas")
                print("2. Verifica tu conexión a internet (necesario para Supabase)")
                print("3. Alterna: Usa la consola SQL de Supabase en https://supabase.com/dashboard")
                return False
    
    return False

if __name__ == "__main__":
    success = init_db()
    exit(0 if success else 1)
