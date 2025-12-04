# 🐮 Cow App - Plataforma de Gestión Ganadera

**Cow App** es una aplicación web moderna diseñada para facilitar la gestión y comunicación entre ganaderos y veterinarios. Permite llevar un registro detallado de animales, tratamientos médicos y ofrece un canal de comunicación en tiempo real.

## 🌐 Acceso a la Aplicación
Puedes acceder a la versión desplegada de la aplicación aquí: [Cow App](https://cowapp-yafm.onrender.com/)

## 🚀 Características Principales

### 👨‍🌾 Para Ganaderos
- **Dashboard Interactivo**: Visualización rápida de estadísticas (nacimientos, animales enfermos, total activos).
- **Gestión de Animales**: Registro completo con fotos, raza, edad y estado.
- **Solicitud de Tratamientos**: Crear y gestionar tratamientos para animales enfermos.
- **Chat con Veterinarios**: Comunicación directa para consultas y seguimiento.

### 👨‍⚕️ Para Veterinarios
- **Gestión de Pacientes**: Vista centralizada de todos los tratamientos asignados.
- **Seguimiento Clínico**: Actualización de diagnósticos y estado de tratamientos.
- **Alertas y Notificaciones**: Identificación rápida de casos que requieren atención urgente.
- **Comunicación Directa**: Chat integrado para hablar con los propietarios.

### 🛠️ Funcionalidades Técnicas
- **Autenticación Segura**: Sistema de login y registro con roles diferenciados.
- **Chat en Tiempo Real**: Implementado con WebSockets para mensajería instantánea.
- **Subida de Imágenes**: Integración con Cloudinary para fotos de animales.
- **Diseño Responsivo**: Interfaz adaptada a móviles y escritorio (Bulma CSS).

## 💻 Tecnologías Utilizadas

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Base de Datos**: PostgreSQL / SQLite (vía [SQLAlchemy](https://www.sqlalchemy.org/) & [SQLModel](https://sqlmodel.tiangolo.com/))
- **Frontend**: Jinja2 Templates, HTML5, JavaScript
- **Estilos**: [Bulma CSS](https://bulma.io/) + CSS Personalizado
- **Tiempo Real**: WebSockets
- **Almacenamiento**: Cloudinary

## ⚙️ Instalación y Configuración

### Prerrequisitos
- Python 3.10 o superior
- PostgreSQL (recomendado) o SQLite
- Cuenta en Cloudinary (para imágenes)

### Pasos

1.  **Clonar el repositorio**
    ```bash
    git clone https://github.com/tu-usuario/cow-app.git
    cd cow-app
    ```

2.  **Crear y activar entorno virtual**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno**
    Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
    ```env
    DATABASE_URL=postgresql://user:password@localhost:5432/cow_db
    SECRET_KEY=tu_clave_secreta_super_segura
    CLOUDINARY_CLOUD_NAME=tu_cloud_name
    CLOUDINARY_API_KEY=tu_api_key
    CLOUDINARY_API_SECRET=tu_api_secret
    ```

5.  **Inicializar la Base de Datos**
    ```bash
    python create_db.py
    ```

## ▶️ Ejecución

Para iniciar el servidor de desarrollo:

```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en: `http://127.0.0.1:8000`

## 📂 Estructura del Proyecto

```
fastApiProject1/
├── app/
│   ├── crud/           # Operaciones de Base de Datos
│   ├── models/         # Modelos SQLModel
│   ├── routers/        # Endpoints de la API
│   ├── schemas/        # Esquemas Pydantic
│   ├── static/         # CSS, JS, Imágenes
│   ├── templates/      # Plantillas HTML (Jinja2)
│   ├── websocket/      # Gestor de conexiones WS
│   ├── db.py           # Configuración de DB
│   └── main.py         # Punto de entrada
├── requirements.txt
└── README.md
```

## 🤝 Contribución

1.  Haz un Fork del proyecto.
2.  Crea tu rama de funcionalidad (`git checkout -b feature/NuevaFuncionalidad`).
3.  Haz Commit de tus cambios (`git commit -m 'Agrega nueva funcionalidad'`).
4.  Haz Push a la rama (`git push origin feature/NuevaFuncionalidad`).
5.  Abre un Pull Request.

---
Desarrollado con ❤️ para el sector agropecuario.