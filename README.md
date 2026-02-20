# Pay Wallet API

API REST para gestión de billeteras digitales (wallets) con soporte para múltiples monedas, transacciones (depósitos/retiros) y transferencias entre wallets.

## 📋 Descripción

Pay Wallet es una aplicación Django REST Framework que permite a los usuarios:
- Crear y gestionar múltiples billeteras digitales
- Realizar depósitos y retiros
- Transferir fondos entre wallets
- Gestionar su perfil de usuario
- Autenticación mediante JWT (JSON Web Tokens)

## 🛠️ Tecnologías

- **Django 6.0+**: Framework web de Python
- **Django REST Framework**: Framework para construir APIs REST
- **PostgreSQL**: Base de datos relacional
- **JWT (Simple JWT)**: Autenticación mediante tokens
- **Python-dotenv**: Gestión de variables de entorno

## 📦 Instalación

### Prerrequisitos

- Python 3.8+
- PostgreSQL 12+
- pip

### Pasos

1. **Clonar el repositorio** (o navegar al directorio del proyecto)

2. **Crear un entorno virtual**:
```bash
python -m venv venv
```

3. **Activar el entorno virtual**:
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

5. **Configurar la base de datos PostgreSQL**:
   - Crear una base de datos llamada `pay-wallet` (o el nombre que prefieras)
   - Asegúrate de tener un usuario PostgreSQL con permisos

6. **Configurar variables de entorno**:
   - Copia el archivo `.env` y configura las siguientes variables:
   ```env
   DEBUG=True
   SECRET_KEY=tu-clave-secreta-generada
   DATABASE_NAME=pay-wallet
   DATABASE_USER=postgres
   DATABASE_PASSWORD=tu-contraseña
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   ```

   Para generar una `SECRET_KEY`:
   ```bash
   python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

7. **Aplicar migraciones**:
```bash
python manage.py migrate
```

8. **Crear un superusuario** (opcional):
```bash
python manage.py createsuperuser
```

9. **Ejecutar el servidor de desarrollo**:
```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## 📁 Estructura del Proyecto

```
pay-wallet/
├── accounts/          # App de usuarios y autenticación
│   ├── models.py     # Modelo User personalizado
│   ├── serializers.py # Serializers para registro y perfil
│   ├── views.py      # Vistas de registro, login y perfil
│   └── urls.py       # URLs de autenticación
├── wallets/          # App de billeteras
│   ├── models.py     # Modelo Wallet
│   ├── serializers.py # Serializer de Wallet
│   ├── views.py      # ViewSet con acciones personalizadas
│   └── urls.py       # URLs de wallets
├── transactions/     # App de transacciones y transferencias
│   ├── models.py     # Modelos Transaction y Transfer
│   ├── serializers.py # Serializers con validaciones
│   ├── views.py      # ViewSets con lógica de negocio
│   └── urls.py       # URLs de transacciones
├── config/           # Configuración del proyecto
│   ├── settings.py   # Configuración Django
│   └── urls.py       # URLs principales
├── .env              # Variables de entorno (no versionar)
├── requirements.txt  # Dependencias Python
└── manage.py        # Script de gestión Django
```

## 🔐 Autenticación

La API utiliza **JWT (JSON Web Tokens)** para autenticación. Para acceder a los endpoints protegidos, incluye el token en el header:

```
Authorization: Bearer <access_token>
```

### Obtener tokens

1. **Registro de usuario**:
```http
POST /api/accounts/register/
Content-Type: application/json

{
  "email": "usuario@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "username": "Nombre Usuario"
}
```

2. **Login**:
```http
POST /api/accounts/login/
Content-Type: application/json

{
  "email": "usuario@example.com",
  "password": "password123"
}
```

Respuesta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

3. **Refrescar token**:
```http
POST /api/accounts/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 📡 Endpoints de la API

### Autenticación (`/api/accounts/`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/register/` | Registrar nuevo usuario | No |
| POST | `/login/` | Obtener tokens JWT | No |
| POST | `/token/refresh/` | Refrescar access token | No |
| GET | `/profile/` | Ver perfil del usuario | Sí |
| PUT | `/profile/` | Actualizar perfil completo | Sí |
| PATCH | `/profile/` | Actualizar perfil parcial | Sí |

### Wallets (`/api/wallets/`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/` | Listar wallets del usuario | Sí |
| POST | `/` | Crear nueva wallet | Sí |
| GET | `/{id}/` | Ver detalle de wallet | Sí |
| PUT | `/{id}/` | Actualizar wallet completa | Sí |
| PATCH | `/{id}/` | Actualizar wallet parcial | Sí |
| DELETE | `/{id}/` | Eliminar wallet | Sí |
| GET | `/{id}/balance/` | Consultar balance | Sí |
| POST | `/{id}/activate/` | Activar wallet | Sí |
| POST | `/{id}/deactivate/` | Desactivar wallet | Sí |

### Transacciones (`/api/transactions/`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/` | Listar transacciones del usuario | Sí |
| POST | `/` | Crear transacción (depósito/retiro) | Sí |
| GET | `/{id}/` | Ver detalle de transacción | Sí |
| PUT | `/{id}/` | Actualizar transacción | Sí |
| PATCH | `/{id}/` | Actualizar transacción parcial | Sí |
| DELETE | `/{id}/` | Eliminar transacción | Sí |

### Transferencias (`/api/transactions/transfers/`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/` | Listar transferencias del usuario | Sí |
| POST | `/` | Crear transferencia entre wallets | Sí |
| GET | `/{id}/` | Ver detalle de transferencia | Sí |
| PUT | `/{id}/` | Actualizar transferencia | Sí |
| PATCH | `/{id}/` | Actualizar transferencia parcial | Sí |
| DELETE | `/{id}/` | Eliminar transferencia | Sí |

## 📊 Modelos de Datos

### User (Cuentas)
- `email` (único, usado para login)
- `first_name`, `last_name`
- `phone_number` (opcional)
- `date_of_birth` (opcional)
- `is_verified` (boolean)
- `date_joined`, `last_login`

### Wallet (Billeteras)
- `user` (ForeignKey a User)
- `balance` (DecimalField, max_digits=10, decimal_places=2)
- `currency` (USD, EUR, GBP)
- `is_active` (boolean)
- `created_at`, `updated_at`

### Transaction (Transacciones)
- `wallet` (ForeignKey a Wallet)
- `amount` (DecimalField)
- `transaction_type` (DEPOSIT, WITHDRAWAL)
- `status` (PENDING, COMPLETED, FAILED)
- `description` (opcional)
- `created_at`, `updated_at`

### Transfer (Transferencias)
- `from_wallet` (ForeignKey a Wallet)
- `to_wallet` (ForeignKey a Wallet)
- `amount` (DecimalField)
- `status` (PENDING, COMPLETED, FAILED)
- `created_at`, `updated_at`

## 💡 Ejemplos de Uso

### Crear una Wallet

```http
POST /api/wallets/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "balance": "0.00",
  "currency": "USD",
  "is_active": true
}
```

### Realizar un Depósito

```http
POST /api/transactions/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "wallet": 1,
  "amount": "100.50",
  "transaction_type": "DEPOSIT",
  "description": "Depósito inicial"
}
```

### Realizar un Retiro

```http
POST /api/transactions/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "wallet": 1,
  "amount": "50.00",
  "transaction_type": "WITHDRAWAL",
  "description": "Retiro de fondos"
}
```

**Nota**: El sistema valida automáticamente que haya balance suficiente antes de procesar el retiro.

### Transferir entre Wallets

```http
POST /api/transactions/transfers/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "from_wallet": 1,
  "to_wallet": 2,
  "amount": "25.00"
}
```

**Nota**: El sistema valida que:
- Las wallets sean distintas
- La wallet de origen tenga balance suficiente
- La wallet de origen pertenezca al usuario autenticado

### Consultar Balance

```http
GET /api/wallets/1/balance/
Authorization: Bearer <access_token>
```

Respuesta:
```json
{
  "wallet_id": 1,
  "balance": "100.50",
  "currency": "USD"
}
```

## 🔒 Validaciones y Reglas de Negocio

### Wallets
- El balance no puede ser negativo
- Solo puedes crear/modificar tus propias wallets
- Solo puedes ver tus propias wallets

### Transacciones
- El monto debe ser mayor que cero
- Para retiros: se valida balance suficiente antes de procesar
- Las transacciones se procesan automáticamente y actualizan el balance de la wallet
- Solo puedes crear transacciones en tus propias wallets

### Transferencias
- El monto debe ser mayor que cero
- Las wallets de origen y destino deben ser distintas
- Se valida balance suficiente en la wallet de origen
- Solo puedes enviar desde tus propias wallets
- Las transferencias se procesan automáticamente (resta origen, suma destino)

## 🗄️ Base de Datos

El proyecto utiliza **PostgreSQL**. Las migraciones se aplican con:

```bash
python manage.py makemigrations
python manage.py migrate
```

**Importante**: Si cambias el modelo de User después de crear migraciones iniciales, necesitarás recrear la base de datos o hacer migraciones manuales.

## 🧪 Testing

Para ejecutar los tests (si existen):

```bash
python manage.py test
```

## 📝 Notas Importantes

1. **Seguridad**: En producción, asegúrate de:
   - Cambiar `DEBUG=False`
   - Usar una `SECRET_KEY` segura y única
   - Configurar `ALLOWED_HOSTS`
   - Usar HTTPS
   - No versionar el archivo `.env`

2. **Base de Datos**: Si cambias el modelo User después de crear migraciones, puede ser necesario recrear la base de datos.

3. **Tokens JWT**: Los tokens tienen una duración limitada:
   - Access token: 15 minutos
   - Refresh token: 1 día

## 📄 Licencia

Este proyecto es de uso educativo/demostrativo.

## 👤 Autor

Desarrollado como proyecto de gestión de billeteras digitales.

---

Para más información sobre Django REST Framework, visita: https://www.django-rest-framework.org/
