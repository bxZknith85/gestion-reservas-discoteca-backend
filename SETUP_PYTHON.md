# 🐍 Setup de Python - Gestion Reservas Discoteca

## ⚠️ Problema Actual
Tu sistema tiene **Python 3.14.4**, que es demasiado reciente y no tiene wheels precompilados disponibles para algunas dependencias críticas como `psycopg2-binary` y `pydantic-core`.

## ✅ Solución: Instalar Python 3.11 o 3.12

### Opción 1: Descargar Python 3.12 (Recomendado)
1. Ve a https://www.python.org/downloads/
2. Descarga **Python 3.12.0** (o la última versión 3.12.x)
3. Al instalar:
   - ☑️ **Marca: "Add Python to PATH"**
   - ☑️ **Marca: "Install pip"**
   - ☑️ **Marca: "Install for all users"** (si puedes)
4. Haz clic en **Install Now**

### Opción 2: Descargar Python 3.11 (También funciona)
1. Ve a https://www.python.org/downloads/
2. Descarga **Python 3.11.x** (versión estable)
3. Sigue los mismos pasos que Opción 1

## 🔧 Después de Instalar Python 3.12/3.11

### Paso 1: Verificar Instalación
```powershell
python --version
# Debe mostrar: Python 3.12.x o Python 3.11.x
```

### Paso 2: Crear Virtual Environment
```powershell
cd c:\Users\USUARIO\Documents\Github\bxZknith85\gestion-reservas-discoteca-backend
python -m venv venv
```

### Paso 3: Activar Virtual Environment
```powershell
# En PowerShell:
.\venv\Scripts\Activate.ps1

# En CMD:
venv\Scripts\activate.bat
```

Deberías ver `(venv)` al inicio de tu línea de comando.

### Paso 4: Instalar Dependencias
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 5: Verificar Instalación
```powershell
python verify.py
```

Deberías ver todos los checks en ✅ verde.

## 📋 Checklist Final

- [ ] Descargué e instalé Python 3.12 (o 3.11)
- [ ] Verifiqué que `python --version` muestra 3.12.x o 3.11.x
- [ ] Creé virtual environment con `python -m venv venv`
- [ ] Activé venv con `.\venv\Scripts\Activate.ps1`
- [ ] Ejecuté `pip install -r requirements.txt` exitosamente
- [ ] Ejecuté `python verify.py` y pasaron todos los checks

## ❓ Problemas Comunes

**"python no se reconoce"**
- Python no está en PATH. Reinstala con "Add Python to PATH" marcado

**"pip: command not found"**
- Asegúrate que venv está activado (deberías ver `(venv)` en tu terminal)

**Error al activar venv en PowerShell**
- Ejecuta primero: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## 🚀 Una Vez Instalado

```powershell
# Terminal 1: Activar venv e iniciar servidor
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

# Terminal 2: Ejecutar tests
.\venv\Scripts\Activate.ps1
pytest tests/
```

Luego:
- API Swagger: http://localhost:8000/api/v1/docs
- Health Check: http://localhost:8000/api/v1/health
