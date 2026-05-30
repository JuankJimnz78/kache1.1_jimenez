# Comparador de Precios de Supermercados

API REST construida con Django REST Framework para comparar precios entre supermercados.

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) instalado
- PostgreSQL (recomendado) o SQLite para desarrollo rápido

## Configuración PostgreSQL

### 1. Crear la base de datos

```bash
psql -U postgres
CREATE DATABASE precios_db;
\q
```

### 2. Configurar `.env`

```env
USE_POSTGRES=True
DATABASE_URL=postgres://postgres:tu_password@localhost:5432/precios_db
```

### 3. Comandos

```bash
uv sync
uv run manage.py migrate
uv run manage.py createsuperuser
uv run manage.py runserver
uv run pytest
```

## Inicio rápido (SQLite)

```bash
uv sync
cp .env.example .env
# Editar .env: USE_POSTGRES=False
uv run manage.py migrate
uv run manage.py createsuperuser
uv run manage.py runserver
```

## Endpoints

| Recurso           | Endpoint                     |
|-------------------|------------------------------|
| Supermercados     | `/api/v1/supermercados/`     |
| Categorías        | `/api/v1/categorias/`        |
| Productos         | `/api/v1/productos/`         |
| Sucursales        | `/api/v1/sucursales/`        |
| Precios           | `/api/v1/precios/`           |
| Historial precios | `/api/v1/historial-precios/` |
| Admin             | `/admin/`                    |

## Acciones especiales

| Endpoint                                               | Descripción                                    |
|--------------------------------------------------------|------------------------------------------------|
| `GET /api/v1/precios/comparar-precios/?id_producto=X`  | Todos los precios de un producto (menor→mayor) |
| `GET /api/v1/productos/{id}/mejor-precio/`             | Precio más bajo con su sucursal                |
| `GET /api/v1/sucursales/{id}/productos-en-oferta/`     | Productos en oferta de una sucursal            |

## Filtros

### Productos
`nombre`, `marca`, `codigo_barras` → `icontains`
`id_categoria`, `unidad_medida` → exacto

### Precios
`id_producto`, `id_sucursal`, `en_oferta` → exacto
`precio_min`, `precio_max` → rango de `precio_actual`
`id_supermercado` → filtrar por supermercado (a través de sucursal)

### Historial de Precios
`id_producto`, `id_sucursal` → exacto
`fecha_desde`, `fecha_hasta` → rango de `fecha_registro`

## Paginación

| Clase                   | page_size | max_page_size |
|-------------------------|-----------|---------------|
| StandardResultsPagination | 20      | 100           |
| SmallResultsPagination  | 10        | 50            |

Parámetro de query: `?page_size=N`

## Señales automáticas

- **Creación de Precio** → se registra en `HistorialPrecios` como primer registro
- **Actualización de Precio** → si `precio_actual` cambia, el valor anterior se guarda en `HistorialPrecios`

## Grupos de permisos

| Clase               | Comportamiento                                  |
|---------------------|-------------------------------------------------|
| EsSoloLectura       | Solo GET/HEAD/OPTIONS                           |
| EsAdminOSoloLectura | Admin escribe, el resto solo lee (default)      |
| EsAdminOEditor      | Grupo "Editor" o `is_staff` pueden escribir     |
| EsSuperusuario      | Solo superusuarios pueden DELETE                |

## Estructura del proyecto

```
precios_project/
├── config/          # Configuración Django (settings, urls, wsgi, asgi)
├── store/           # Aplicación principal
│   ├── models/      # Modelos de base de datos
│   ├── serializers/ # Serializers DRF
│   ├── views/       # ViewSets
│   ├── tests/       # Tests con pytest-django y factory-boy
│   ├── filters.py   # Filtros django-filter
│   ├── pagination.py
│   ├── permissions.py
│   └── signals.py   # Señales para HistorialPrecios
├── manage.py
└── pyproject.toml
```
