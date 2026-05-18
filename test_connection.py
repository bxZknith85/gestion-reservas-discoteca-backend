#!/usr/bin/env python
"""Script para verificar conexión a Supabase"""

import os

from dotenv import load_dotenv

print("=" * 60)
print("🔗 VERIFICANDO CONEXIÓN A SUPABASE")
print("=" * 60)

load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url or "[" in db_url:
    print("\n❌ .env no está configurado con credenciales")
    print("   Por favor, edita el archivo .env con tus datos reales")
    exit(1)

print("\n✅ .env tiene credenciales configuradas")

try:
    from sqlalchemy import create_engine, text

    print("\n⏳ Intentando conectar a Supabase...")
    engine = create_engine(db_url, echo=False)

    with engine.connect() as conn:
        # Test 1: Version
        result = conn.execute(text("SELECT version()"))
        version = result.scalar()
        print("\n✅ CONEXIÓN EXITOSA A SUPABASE")
        print(f"   Base de datos: {version[:60]}...")

        # Test 2: Contar tablas
        result = conn.execute(
            text(
                "SELECT COUNT(table_name) FROM information_schema.tables "
                "WHERE table_schema NOT IN ('pg_catalog', 'information_schema')"
            )
        )
        table_count = result.scalar()
        print(f"   Tablas existentes: {table_count}")

        # Test 3: Listar schemas
        result = conn.execute(
            text(
                "SELECT schema_name FROM information_schema.schemata "
                "WHERE schema_name NOT IN "
                "('pg_catalog', 'information_schema', 'pg_toast', 'pg_temp_1', 'pg_toast_temp_1')"
            )
        )
        schemas = [row[0] for row in result.fetchall()]
        print(f"   Schemas: {', '.join(schemas)}")

except Exception as e:
    print("\n❌ ERROR DE CONEXIÓN:")
    print(f"   {str(e)[:150]}")
    print("\n   Verifica que el .env tenga:")
    print("   - DATABASE_URL correcta")
    print("   - Contraseña de postgres correcta")
    exit(1)

print("\n" + "=" * 60)
print("🎉 ¡Backend listo para iniciar!")
print("=" * 60)
print("\nPróximo paso: ejecuta")
print("  uvicorn app.main:app --reload")
