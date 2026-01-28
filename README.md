# Calculadora de Notas

Aplicación web para gestionar y visualizar calificaciones de cursos universitarios. Desarrollada con Flask para proporcionar una interfaz moderna y accesible a los estudiantes de la Universidad Técnica Federico Santa María.

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/lyoss-usm/calculadora-de-notas.git
cd calculadora-de-notas
```

### 2. Crear entorno virtual

Se recomienda usar un entorno virtual para aislar las dependencias del proyecto:

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

**Linux/macOS:**

```bash
source .venv/bin/activate
```

**Windows (CMD):**

```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar base de datos

Este proyecto utiliza **MongoDB** como base de datos para almacenar información de los cursos. Asegúrate de tener MongoDB instalado y en ejecución en tu máquina local o utiliza un servicio de MongoDB en la nube.

#### Configuración de la URI de MongoDB

Por defecto, la aplicación se conecta a `mongodb://localhost:27017/calculadora_notas`. Si necesitas una configuración personalizada, establece la variable de entorno:

```bash
export MONGO_URI="mongodb://usuario:contraseña@host:puerto/calculadora_notas"
```

#### Poblar la base de datos

Para descargar cursos y crear los índices necesarios:

```bash
python -m core.cursos.repository
```

El script te guiará en el proceso de descarga y configuración inicial. Este proceso:

1. Descarga información de cursos desde la fuente
2. Almacena los datos en MongoDB
3. Crea índices de texto optimizados para búsquedas en español

## Ejecución

### Modo Desarrollo

Para iniciar el servidor de desarrollo:

```bash
python run.py
```

El servidor estará disponible en:

- URL local: `http://127.0.0.1:5000`
- URL de red: `http://<tu-ip>:5000`

### Variables de Entorno

Puedes configurar el entorno mediante variables:

```bash
# Cambiar entorno (development, production, testing)
export FLASK_ENV=development

# Cambiar puerto
export PORT=8000

python run.py
```

### Detener el Servidor

Presiona `Ctrl+C` en la terminal donde está ejecutándose el servidor.

## Estructura del Proyecto

```
calculadora-de-notas/
├── app/                          # aplicación flask
│   ├── __init__.py              # application factory
│   ├── routes.py                # rutas web
│   ├── static/                  # archivos estáticos
│   │   ├── css/
│   │   │   └── style.css        # estilos principales
│   │   ├── img/
│   │   │   └── lyoss-banner.png # banner lyoss
│   │   └── js/
│   │       └── main.js          # javaScript principal
│   └── templates/               # templates Jinja2
│       ├── layouts/             # layouts base
│       │   ├── base.html
│       │   ├── navbar.html
│       │   └── footer.html
│       ├── components/          # componentes reutilizables
│       │   └── course_card.html
│       └── index.html           # página principal
├── core/                        # lógica de negocio
│   ├── analisis/               # módulos de análisis
│   ├── cursos/                 # modelos de cursos
│   ├── data/                   # datos JSON
│   └── utils.py                # utilidades
├── config.py                   # configuración Flask
├── run.py                      # entry point
└── requirements.txt            # dependencias Python
```
