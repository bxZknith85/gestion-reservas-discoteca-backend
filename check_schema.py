"""
Diagnóstico: Ver qué tablas existen en la BD
"""
from sqlalchemy import inspect, text
from app.db.database import engine

def check_tables():
    inspector = inspect(engine)
    
    print("=" * 60)
    print("ESQUEMAS EN LA BD:")
    print("=" * 60)
    
    schemas = inspector.get_schema_names()
    print(f"Esquemas encontrados: {schemas}\n")
    
    for schema in schemas:
        if schema in ['public', 'core', 'catalog', 'transactions']:
            print(f"\n📋 ESQUEMA: {schema}")
            print("-" * 60)
            tables = inspector.get_table_names(schema=schema)
            
            for table in tables:
                columns = inspector.get_columns(table, schema=schema)
                print(f"\n  🗂️  Tabla: {schema}.{table}")
                for col in columns:
                    print(f"      - {col['name']}: {col['type']}")

if __name__ == "__main__":
    try:
        check_tables()
    except Exception as e:
        print(f"❌ Error: {e}")
