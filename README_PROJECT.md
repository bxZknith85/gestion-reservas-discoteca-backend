# Gestión de Reservas de Discoteca - Backend

Sistema backend para la gestión de reservas en discotecas, desarrollado con **FastAPI** y **PostgreSQL**.

## 🚀 Características

- ✅ API RESTful con FastAPI
- ✅ Autenticación con JWT
- ✅ Base de datos PostgreSQL
- ✅ Modelos para: Usuarios, Salas, Eventos, Reservas
- ✅ CRUD completo para cada entidad
- ✅ Dockerizado
- ✅ Tests unitarios
- ✅ Validación de datos con Pydantic

## 📋 Requisitos Previos

- Python 3.11+
- PostgreSQL 12+
- Docker y Docker Compose (opcional)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/bxZknith85/gestion-reservas-discoteca-backend.git
cd gestion-reservas-discoteca-backend
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus configuraciones:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/gestion_reservas
SECRET_KEY=your-secret-key-here
DEBUG=True
ENVIRONMENT=development
```

### 5. Crear base de datos

```bash
# Usando PostgreSQL
createdb -U postgres gestion_reservas
```

## 🚀 Uso

### Ejecutar servidor de desarrollo

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

### Documentación interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 Docker

### Ejecutar con Docker Compose

```bash
docker-compose up -d
```

Esto iniciará:
- PostgreSQL en puerto 5432
- Backend en puerto 8000

### Detener servicios

```bash
docker-compose down
```

## 📁 Estructura del Proyecto

```
gestion-reservas-discoteca-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── usuarios.py
│   │           ├── salas.py
│   │           ├── eventos.py
│   │           └── reservas.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── constants.py
│   ├── models/
│   │   ├── usuario.py (contiene todos los modelos)
│   │   └── base.py
│   ├── schemas/
│   │   ├── usuario.py
│   │   ├── sala.py
│   │   ├── evento.py
│   │   └── reserva.py
│   ├── crud/
│   │   ├── usuario.py
│   │   ├── sala.py
│   │   ├── evento.py
│   │   └── reserva.py
│   ├── db/
│   │   └── database.py
│   ├── services/
│   └── main.py
├── tests/
│   ├── conftest.py
│   └── test_health.py
├── migrations/
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## 🔌 Endpoints Principales

### Usuarios
- `POST /api/v1/usuarios/` - Crear usuario
- `GET /api/v1/usuarios/` - Listar usuarios
- `GET /api/v1/usuarios/{id}` - Obtener usuario
- `PUT /api/v1/usuarios/{id}` - Actualizar usuario
- `DELETE /api/v1/usuarios/{id}` - Eliminar usuario

### Salas
- `POST /api/v1/salas/` - Crear sala
- `GET /api/v1/salas/` - Listar salas
- `GET /api/v1/salas/{id}` - Obtener sala
- `PUT /api/v1/salas/{id}` - Actualizar sala
- `DELETE /api/v1/salas/{id}` - Eliminar sala

### Eventos
- `POST /api/v1/eventos/` - Crear evento
- `GET /api/v1/eventos/` - Listar eventos
- `GET /api/v1/eventos/{id}` - Obtener evento
- `PUT /api/v1/eventos/{id}` - Actualizar evento
- `DELETE /api/v1/eventos/{id}` - Eliminar evento

### Reservas
- `POST /api/v1/reservas/` - Crear reserva
- `GET /api/v1/reservas/` - Listar reservas
- `GET /api/v1/reservas/{id}` - Obtener reserva
- `GET /api/v1/reservas/usuario/{usuario_id}` - Listar reservas de usuario
- `PUT /api/v1/reservas/{id}` - Actualizar reserva
- `DELETE /api/v1/reservas/{id}` - Eliminar reserva

## 🧪 Tests

Ejecutar tests:

```bash
pytest
```

Con cobertura:

```bash
pytest --cov=app
```

## 📝 Próximos Pasos

- [ ] Implementar autenticación con JWT
- [ ] Agregar endpoints de login/logout
- [ ] Implementar roles y permisos
- [ ] Agregar validaciones de negocio
- [ ] Implementar notificaciones por email
- [ ] Agregar paginación mejorada
- [ ] Implementar filtros avanzados
- [ ] Agregar logging
- [ ] Implementar caché
- [ ] Agregar rate limiting

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE`.

## 👤 Autor

**Tu Nombre**

- GitHub: [@bxZknith85](https://github.com/bxZknith85)

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para cambios importantes, por favor abre un issue primero para discutir los cambios propuestos.

## 📞 Contacto

Si tienes preguntas o sugerencias, no dudes en contactarme.

---

Hecho con ❤️ por [bxZknith85](https://github.com/bxZknith85)
