# 🚀 Users API - CRUD con FastAPI y SQLAlchemy

Esta es una API REST simple construida con **FastAPI** que permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre una tabla de usuarios. Utiliza **SQLAlchemy** para la persistencia de datos (usando SQLite) y requiere una **API Key** para operaciones de escritura.

---

## 🛠️ Instalación y Configuración

Sigue estos pasos para configurar tu entorno de desarrollo y obtener todas las dependencias necesarias.

### 1. Crear Entorno Virtual e Instalar Dependencias

Usaremos **`uv`** para gestionar las dependencias.

```bash
# 1. Instalar uv si no lo tienes: pip install uv
# 2. Crear un entorno virtual llamado 'venv'
uv init

# 3. Activar el entorno virtual
source venv/bin/activate  # En Linux/macOS
# .\venv\Scripts\activate  # En Windows

# 4. Instalar las dependencias
uv add fastapi --extra standard 

uv add sqlalchemy 

uv add pydantic 

uv add python-dotenv

# 5. Ejecutar la app
uv run fastaoi dev main.py