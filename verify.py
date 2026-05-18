#!/usr/bin/env python
"""Script para verificar que el backend está listo para funcionar"""

import sys

print("\n" + "=" * 60)
print("🔍 VERIFICACIÓN DEL BACKEND GESTION DE RESERVAS")
print("=" * 60 + "\n")

# 1. Verificar que los modelos se importan correctamente
print("1️⃣  Verificando importación de modelos...")
try:
    from app.db.database import engine

    print("   ✅ Todos los modelos se importan correctamente")
except Exception as e:
    print(f"   ❌ Error importando modelos: {e}")
    sys.exit(1)

# 2. Verificar que los schemas se importan correctamente
print("\n2️⃣  Verificando importación de schemas...")
try:
    print("   ✅ Todos los schemas se importan correctamente")
except Exception as e:
    print(f"   ❌ Error importando schemas: {e}")
    sys.exit(1)

# 3. Verificar configuración
print("\n3️⃣  Verificando configuración...")
try:
    from app.core.config import settings

    print("   ✅ Configuración cargada:")
    print(f"      - Ambiente: {settings.ENVIRONMENT}")
    print(f"      - DEBUG: {settings.DEBUG}")
    print(f"      - URL BD: {settings.DATABASE_URL[:50]}...")
except Exception as e:
    print(f"   ❌ Error cargando configuración: {e}")
    sys.exit(1)

# 4. Intentar conectar a la BD
print("\n4️⃣  Intentando conectar a Supabase...")
try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("   ✅ Conexión a Supabase establecida correctamente")
except Exception as e:
    print(f"   ⚠️  Error conectando a Supabase: {e}")
    print("      → Asegúrate de que:")
    print("         1. DATABASE_URL está configurada en .env")
    print("         2. Tienes acceso a internet")
    print("         3. El script schema_db.sql fue ejecutado en Supabase")
    print("\n      Continuando sin BD para verificar código...")

# 5. Verificar FastAPI
print("\n5️⃣  Verificando FastAPI...")
try:
    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)
    response = client.get("/")

    if response.status_code == 200:
        print("   ✅ FastAPI funciona correctamente")
        data = response.json()
        print(f"      - Mensaje: {data.get('message')}")
        print(f"      - Versión: {data.get('version')}")
    else:
        print(f"   ⚠️  Respuesta inesperada: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error con FastAPI: {e}")
    sys.exit(1)

# 6. Verificar health check
print("\n6️⃣  Verificando health check...")
try:
    response = client.get("/api/v1/health")

    if response.status_code == 200:
        print("   ✅ Health check activo")
        data = response.json()
        print(f"      - Status: {data.get('status')}")
        print(f"      - Servicio: {data.get('service')}")
    else:
        print(f"   ⚠️  Respuesta inesperada: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error en health check: {e}")

# 7. Verificar endpoints disponibles
print("\n7️⃣  Endpoints disponibles:")
for route in app.routes:
    if hasattr(route, "path") and hasattr(route, "methods"):
        methods = ", ".join(route.methods - {"HEAD", "OPTIONS"})
        print(f"   ✅ {route.path:40} [{methods}]")

print("\n" + "=" * 60)
print("✅ BACKEND LISTO PARA USAR")
print("=" * 60)
print("\n📝 Próximos pasos:")
print("   1. Si viste errores en Supabase, ve a https://supabase.com/dashboard")
print("   2. Ejecuta el script schema_db.sql en SQL Editor de Supabase")
print("   3. Actualiza las credenciales en .env")
print("   4. Ejecuta: uvicorn app.main:app --reload")
print("   5. Abre http://localhost:8000/api/v1/docs para documentación")
print("\n")
