# Gestión de Reservas de Discoteca - Backend (Supabase)

Sistema backend para la gestión de reservas en discotecas, desarrollado con **FastAPI**, **PostgreSQL** y **Supabase**.

## 🚀 Características

- ✅ API RESTful con FastAPI v0.104+
- ✅ Base de datos PostgreSQL en Supabase
- ✅ Autenticación con JWT
- ✅ Múltiples schemas: `catalog`, `core`, `transactions`, `audit`, `system`
- ✅ Modelos completos para: Usuarios, Eventos, Mesas, Reservas, Tickets, Órdenes, Pagos
- ✅ CRUD completo para cada entidad
- ✅ Auditoría automática con triggers SQL
- ✅ Triggers para `updated_at` automático
- ✅ Vistas SQL para consultas complejas
- ✅ Dockerizado
- ✅ Tests unitarios
- ✅ Validación de datos con Pydantic v2
- ✅ CORS configurado

## 📋 Requisitos Previos

- **Python 3.11 o 3.12** (⚠️ NO usar Python 3.14, ver [SETUP_PYTHON.md](SETUP_PYTHON.md))
- PostgreSQL 16+ (via Supabase)
- Docker y Docker Compose (opcional)
- Cuenta en Supabase (https://supabase.com)

## 🔧 Configuración

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

### 4. Obtener credenciales de Supabase

1. Ve a https://supabase.com/dashboard
2. Crea un nuevo proyecto o usa uno existente
3. En `Settings > Database`, obtén:
   - **Host**: `[project].supabase.co`
   - **Port**: `5432`
   - **Database**: `postgres`
   - **User**: `postgres` (o tu usuario)
   - **Password**: La contraseña que configuraste

4. En `Settings > API`, obtén:
   - **Project URL**: `https://[project].supabase.co`
   - **Anon Key**: Tu clave pública

### 5. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales de Supabase:

```env
# DATABASE_URL format: postgresql://[user]:[password]@[project].supabase.co:5432/postgres
DATABASE_URL=postgresql://postgres:your_password@abc123.supabase.co:5432/postgres
SUPABASE_URL=https://abc123.supabase.co
SUPABASE_KEY=your-anon-key

SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DEBUG=False
ENVIRONMENT=production
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

### 6. Ejecutar script SQL en Supabase

1. En Supabase Dashboard, ve a `SQL Editor`
2. Crea una nueva query
3. Copia el contenido de `schema_db.sql` y ejecútalo
4. Esto creará todos los schemas, tablas, índices, triggers y datos semilla

### 7. Verificar la conexión

```bash
python -c "from app.db.database import engine; engine.connect(); print('✅ Conexión exitosa a Supabase')"
```

## 🚀 Uso

### Ejecutar servidor de desarrollo

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

### Documentación interactiva

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

## 🐳 Docker

### Ejecutar con Docker Compose

```bash
# Crear archivo .env con credenciales de Supabase
docker-compose up -d
```

El backend estará disponible en `http://localhost:8000`

### Ver logs

```bash
docker-compose logs -f backend
```

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
│   │           ├── users.py          # Gestión de usuarios
│   │           ├── events.py         # Gestión de eventos
│   │           ├── tables.py         # Gestión de mesas
│   │           ├── reservations.py   # Gestión de reservas
│   │           └── orders.py         # Gestión de órdenes y pagos
│   ├── core/
│   │   ├── config.py       # Configuración (Supabase)
│   │   ├── security.py     # JWT y hashing
│   │   └── constants.py    # Constantes
│   ├── models/
│   │   ├── catalog.py      # Catálogos (tipos, estados)
│   │   ├── core.py         # Entidades principales
│   │   ├── transactions.py # Transacciones (órdenes, pagos)
│   │   ├── audit.py        # Auditoría
│   │   ├── system.py       # Sistema (config, logs admin)
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── event.py
│   │   ├── table.py
│   │   ├── reservation.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   └── ...
│   ├── crud/               # Lógica CRUD (migrar a SQLAlchemy ORM)
│   ├── db/
│   │   └── database.py     # Configuración de BD (Supabase)
│   ├── services/           # Lógica de negocio
│   └── main.py             # Punto de entrada
├── tests/
├── schema_db.sql           # Script SQL de BD
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## 🔌 Endpoints Principales

### Usuarios (`/api/v1/users/`)
- `POST /` - Crear usuario
- `GET /` - Listar usuarios
- `GET /{id}` - Obtener usuario
- `PUT /{id}` - Actualizar usuario
- `DELETE /{id}` - Eliminar usuario

### Eventos (`/api/v1/events/`)
- `POST /` - Crear evento
- `GET /` - Listar eventos
- `GET /{id}` - Obtener evento
- `PUT /{id}` - Actualizar evento
- `DELETE /{id}` - Eliminar evento

### Mesas (`/api/v1/tables/`)
- `POST /` - Crear mesa
- `GET /` - Listar mesas
- `GET /{id}` - Obtener mesa
- `PUT /{id}` - Actualizar mesa
- `DELETE /{id}` - Eliminar mesa

### Reservas (`/api/v1/reservations/`)
- `POST /` - Crear reserva
- `GET /` - Listar reservas
- `GET /{id}` - Obtener reserva
- `GET /user/{user_id}` - Listar reservas de usuario
- `PUT /{id}` - Actualizar reserva
- `DELETE /{id}` - Cancelar reserva

### Órdenes (`/api/v1/orders/`)
- `POST /` - Crear orden
- `GET /` - Listar órdenes
- `GET /{id}` - Obtener orden
- `PUT /{id}` - Actualizar orden
- `DELETE /{id}` - Eliminar orden

### Pagos (`/api/v1/orders/{order_id}/payments/`)
- `POST /` - Crear pago
- `GET /` - Listar pagos de orden
- `PUT /{id}` - Confirmar/rechazar pago

## 🔐 Seguridad

- ✅ Contraseñas hasheadas con bcrypt
- ✅ Tokens JWT con vencimiento configurable
- ✅ Validación de email con regex
- ✅ Índices para queries eficientes
- ✅ Constraints de integridad referencial
- ✅ Auditoría automática de cambios críticos

## 🧪 Tests

Ejecutar tests:

```bash
pytest
```

Con cobertura:

```bash
pytest --cov=app
```

Con detalle:

```bash
pytest -v
```

## 📊 Base de Datos

### Schemas

- **catalog**: Tablas de referencia (roles, estados, tipos)
- **core**: Entidades principales (usuarios, eventos, mesas)
- **transactions**: Flujo de compra (órdenes, reservas, tickets, pagos)
- **audit**: Auditoría automática de cambios
- **system**: Configuración y logs administrativos

### Características SQL

- ✅ Triggers para auditoría automática
- ✅ Triggers para `updated_at` automático
- ✅ Vistas para consultas complejas
- ✅ Índices para rendimiento
- ✅ Constraints de integridad
- ✅ Enums para estados

## 📝 Próximos Pasos

- [ ] Implementar endpoints de órdenes y pagos
- [ ] Agregar endpoints de categorías de tickets
- [ ] Agregar endpoints de precios de mesas
- [ ] Implementar autenticación con JWT
- [ ] Agregar endpoints de login/logout
- [ ] Implementar roles y permisos
- [ ] Agregar validaciones de negocio avanzadas
- [ ] Implementar notificaciones por email
- [ ] Agregar paginación mejorada
- [ ] Implementar filtros y búsqueda
- [ ] Agregar logging centralizado
- [ ] Implementar caché (Redis)
- [ ] Agregar rate limiting
- [ ] Implementar WebSockets para actualizaciones en tiempo real

## 🚨 Troubleshooting

### Error: "could not translate host name to address"

**Causa**: La DATABASE_URL está incorrecta o Supabase no es accesible.

**Solución**: 
1. Verifica que el formato sea: `postgresql://[user]:[password]@[project].supabase.co:5432/postgres`
2. Verifica que tengas internet
3. Verifica las credenciales en Supabase Dashboard

### Error: "password authentication failed"

**Causa**: La contraseña de Supabase es incorrecta.

**Solución**: 
1. Ve a Supabase > Settings > Database
2. Reset la contraseña si es necesario
3. Actualiza el `.env`

### Error: "relation does not exist"

**Causa**: El script SQL no se ejecutó en Supabase.

**Solución**: 
1. Ve a Supabase > SQL Editor
2. Ejecuta el contenido de `schema_db.sql`
3. Verifica que los schemas se crearon correctamente

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE`.

## 👤 Autor

**bxZknith85**

- GitHub: [@bxZknith85](https://github.com/bxZknith85)

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para cambios importantes:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

Hecho con ❤️ para la industria de discotecas | Powered by Supabase
