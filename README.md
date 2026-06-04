Kache Backend API
Comparador de precios de supermercados — Backend Django REST Framework.
Autor: Juan Jiménez  
Universidad: UTE — Programación 4  
Proyecto: kache1.1_jimenez
---
Tecnologías
·	Python 3.11+
·	Django 5.x
·	Django REST Framework 3.15+
·	PostgreSQL
·	SimpleJWT (autenticación)
·	django-filter (filtros avanzados)
---
Instalación y ejecución local
1. Clonar el repositorio
```bash
git clone <URL\\\\\\\_DEL\\\\\\\_REPO>
cd kache1.1\\\\\\\_jimenez
```
2. Crear entorno virtual e instalar dependencias
```bash
python -m venv .venv
.venv\\\\\\\\Scripts\\\\\\\\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

pip install django djangorestframework djangorestframework-simplejwt django-cors-headers django-filter python-decouple psycopg2-binary
```
3. Configurar variables de entorno
Copiar `.env.example` a `.env` y completar:
```
SECRET\\\\\\\_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED\\\\\\\_HOSTS=localhost,127.0.0.1
DB\\\\\\\_NAME=kache\\\\\\\_db
DB\\\\\\\_USER=postgres
DB\\\\\\\_PASSWORD=tu\\\\\\\_password
DB\\\\\\\_HOST=localhost
DB\\\\\\\_PORT=5432
CORS\\\\\\\_ALLOW\\\\\\\_ALL\\\\\\\_ORIGINS=True
```
4. Aplicar migraciones y crear superusuario
```bash
python manage.py migrate
python manage.py createsuperuser
```
5. Ejecutar servidor
```bash
python manage.py runserver
```
API disponible en: `http://127.0.0.1:8000/api/v1/`
---
Autenticación JWT
Obtener token (Login)
```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "tu\\\\\\\_password"
}
```
Respuesta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
Usar el token en requests protegidos
Incluir en el header:
```
Authorization: Bearer <access\\\\\\\_token>
```
Renovar token
```http
POST /api/v1/auth/refresh/
Content-Type: application/json

{
  "refresh": "<refresh\\\\\\\_token>"
}
```
---
Permisos
Rol	GET (listar/detalle)	POST / PUT / PATCH	DELETE
Anónimo	✅	❌	❌
Usuario autenticado	✅	❌	❌
Staff (is_staff=True)	✅	✅	✅
Superusuario	✅	✅	✅
---
Endpoints de la API
Base URL: `/api/v1/`
Autenticación
Método	Endpoint	Descripción
POST	`/api/v1/auth/login/`	Obtener access + refresh token
POST	`/api/v1/auth/refresh/`	Renovar access token
POST	`/api/v1/auth/verify/`	Verificar token
Categorías
Método	Endpoint	Descripción	Auth requerida
GET	`/api/v1/categorias/`	Listar todas	No
GET	`/api/v1/categorias/{id}/`	Detalle	No
POST	`/api/v1/categorias/`	Crear	Sí (staff)
PUT	`/api/v1/categorias/{id}/`	Actualizar	Sí (staff)
PATCH	`/api/v1/categorias/{id}/`	Actualizar parcial	Sí (staff)
DELETE	`/api/v1/categorias/{id}/`	Eliminar	Sí (staff)
Filtros disponibles:
·	`?search=lacteos` — búsqueda por nombre/descripción
·	`?categoria\\\\\\\_padre=1` — filtrar por categoría padre
·	`?ordering=nombre` — ordenar
Productos
Método	Endpoint	Descripción	Auth requerida
GET	`/api/v1/productos/`	Listar todos	No
GET	`/api/v1/productos/{id}/`	Detalle	No
GET	`/api/v1/productos/{id}/mejor-precio/`	Mejor precio del producto	No
POST	`/api/v1/productos/`	Crear	Sí (staff)
PUT	`/api/v1/productos/{id}/`	Actualizar	Sí (staff)
PATCH	`/api/v1/productos/{id}/`	Actualizar parcial	Sí (staff)
DELETE	`/api/v1/productos/{id}/`	Eliminar	Sí (staff)
Filtros disponibles:
·	`?search=arroz` — búsqueda por nombre/marca/código de barras
·	`?id\\\\\\\_categoria=2` — filtrar por categoría
·	`?unidad\\\\\\\_medida=kg` — filtrar por unidad
·	`?ordering=nombre` — ordenar
Supermercados
Método	Endpoint	Descripción	Auth requerida
GET	`/api/v1/supermercados/`	Listar todos	No
GET	`/api/v1/supermercados/{id}/`	Detalle	No
POST	`/api/v1/supermercados/`	Crear	Sí (staff)
PUT	`/api/v1/supermercados/{id}/`	Actualizar	Sí (staff)
PATCH	`/api/v1/supermercados/{id}/`	Actualizar parcial	Sí (staff)
DELETE	`/api/v1/supermercados/{id}/`	Eliminar	Sí (staff)
Filtros disponibles:
·	`?search=supermaxi` — búsqueda por nombre
·	`?activo=true` — filtrar activos/inactivos
·	`?ordering=nombre`
Sucursales
Método	Endpoint	Descripción	Auth requerida
GET	`/api/v1/sucursales/`	Listar todas	No
GET	`/api/v1/sucursales/{id}/`	Detalle	No
GET	`/api/v1/sucursales/{id}/productos-en-oferta/`	Productos en oferta de la sucursal	No
POST	`/api/v1/sucursales/`	Crear	Sí (staff)
PUT	`/api/v1/sucursales/{id}/`	Actualizar	Sí (staff)
PATCH	`/api/v1/sucursales/{id}/`	Actualizar parcial	Sí (staff)
DELETE	`/api/v1/sucursales/{id}/`	Eliminar	Sí (staff)
Filtros disponibles:
·	`?search=norte` — búsqueda por nombre/ciudad/dirección
·	`?ciudad=Quito` — filtrar por ciudad
·	`?id\\\\\\\_supermercado=1` — filtrar por supermercado
·	`?activo=true`
Precios
Método	Endpoint	Descripción	Auth requerida
GET	`/api/v1/precios/`	Listar todos	No
GET	`/api/v1/precios/{id}/`	Detalle	No
GET	`/api/v1/precios/comparar-precios/?id\\\\\\\_producto=5`	Comparar precios de un producto	No
POST	`/api/v1/precios/`	Crear	Sí (staff)
PUT	`/api/v1/precios/{id}/`	Actualizar	Sí (staff)
PATCH	`/api/v1/precios/{id}/`	Actualizar parcial	Sí (staff)
DELETE	`/api/v1/precios/{id}/`	Eliminar	Sí (staff)
Filtros disponibles:
·	`?search=leche` — búsqueda por nombre de producto/sucursal
·	`?en\\\\\\\_oferta=true` — solo ofertas
·	`?ordering=precio\\\\\\\_actual`
Historial de Precios
Método	Endpoint	Descripción	Auth requerida
GET	`/api/v1/historial-precios/`	Listar historial	No
GET	`/api/v1/historial-precios/{id}/`	Detalle	No
Filtros disponibles:
·	`?search=leche` — búsqueda por producto/sucursal
·	`?ordering=-fecha\\\\\\\_registro`
---
Paginación
Todos los endpoints de lista están paginados. Respuesta estándar:
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/v1/productos/?page=2",
  "previous": null,
  "results": \\\\\\\[...]
}
```
Tamaño de página: 20 resultados. Cambiar con `?page\\\\\\\_size=10` (máx. 100).
---
Ejemplos de uso con token
Crear un supermercado (requiere staff)
```bash
curl -X POST http://localhost:8000/api/v1/supermercados/ \\\\\\\\
  -H "Authorization: Bearer <access\\\\\\\_token>" \\\\\\\\
  -H "Content-Type: application/json" \\\\\\\\
  -d '{"nombre": "Supermaxi", "sitio\\\\\\\_web": "https://supermaxi.com", "activo": true}'
```
Listar productos (público)
```bash
curl http://localhost:8000/api/v1/productos/?search=arroz
```
Comparar precios de un producto
```bash
curl http://localhost:8000/api/v1/precios/comparar-precios/?id\\\\\\\_producto=1
```
---
Despliegue
La API está desplegada en: `http://<IP\\\\\\\_DEL\\\\\\\_SERVIDOR>/api/v1/`
> Para desplegar en un VPS Ubuntu:
> ```bash
> pip install gunicorn
> gunicorn config.wsgi:application --bind 0.0.0.0:8000
> ```
---
Archivos del proyecto
```
kache1.1\\\\\\\_jimenez/
├── config/
│   ├── settings.py       # Configuración principal
│   ├── urls.py           # URLs raíz + JWT endpoints
│   └── wsgi.py
├── store/
│   ├── models/           # 6 modelos: Categoria, Producto, Supermercado, Sucursal, Precio, HistorialPrecio
│   ├── serializers/      # 6 serializers
│   ├── views/            # 6 viewsets con CRUD completo
│   ├── filters.py        # Filtros avanzados
│   ├── pagination.py     # Paginación estándar
│   ├── permissions.py    # Permisos: EsAdminOSoloLectura, EsAdminOEditor, EsSuperusuario
│   ├── signals.py        # Señales (historial automático de precios)
│   └── urls.py           # Router DRF
├── pyproject.toml        # Dependencias
├── .env.example          # Variables de entorno de ejemplo
└── README.md
```
---
requirements.txt
```
django>=5.0,<6.0
djangorestframework>=3.15
djangorestframework-simplejwt>=5.3
django-cors-headers>=4.3
django-filter>=24.0
python-decouple>=3.8
psycopg2-binary>=2.9
gunicorn>=21.0
```

