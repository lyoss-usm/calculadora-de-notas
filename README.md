# Calculadora de Notas

Herramienta de línea de comandos (CLI) para gestionar, visualizar y simular calificaciones de cursos universitarios. Permite llevar un registro de notas, calcular la nota de presentación actual, visualizar curvas de nivel para alcanzar objetivos y realizar simulaciones de Monte Carlo para estimar probabilidades de aprobación.

## Características

- **Gestión de Notas**: Visualiza tus calificaciones actuales y ve qué evaluaciones faltan por rendir.
- **Gráficos de Curvas de Nivel**:
  - Si falta 1 evaluación: Grafica la Nota de Presentación (NP) en función de la nota que saques en esa evaluación.
  - Si faltan 2+ evaluaciones: Genera curvas de nivel interactivas (usando Plotly) que muestran las combinaciones de notas necesarias para alcanzar diferentes objetivos (55, 70, 80, 90, 100).
- **Simulación de Monte Carlo**: Estima la probabilidad de aprobar o alcanzar tu objetivo personal simulando miles de escenarios posibles para las evaluaciones restantes.
- **Configurable**: Define tus propios objetivos y parámetros de simulación.

## Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/lyoss-usm/calculadora-de-notas
    cd calculadora-de-notas
    ```

2.  **Crear y activar un entorno virtual (recomendado):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Linux/Mac
    # .venv\Scripts\activate   # En Windows
    ```

3.  **Instalar dependencias:**
    El proyecto cuenta con un archivo `requirements.txt` con las librerías necesarias.

    Puedes instalarlas ejecutando:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Para iniciar la aplicación, ejecuta el script `run.sh` (en Linux/Mac) o corre `main.py` directamente con Python:

```bash
./run.sh
# O
python main.py
```

### Navegación

1.  **Selección de Curso**: Al iniciar, verás una lista de cursos disponibles. Selecciona uno ingresando su número.
2.  **Menú del Curso**: Una vez dentro de un curso, tendrás las siguientes opciones:
    - **1. Ver notas**: Muestra tus notas actuales, evaluaciones pendientes y tu situación actual (Aprobado/Reprobado/Objetivo alcanzado).
    - **2. Gráfico de notas**: Genera y abre en tu navegador un gráfico interactivo para analizar qué notas necesitas.
    - **3. Simulación de notas**: Ejecuta una simulación de Monte Carlo y muestra un histograma con la distribución de posibles notas finales.
    - **4. Salir**: Vuelve al menú principal.

## Configuración

El archivo `config.py` contiene parámetros globales que puedes ajustar:
- `nota_aprobar`: Nota mínima para aprobar (por defecto 55).
- `n_samples`: Número de muestras para la simulación de Monte Carlo.
- `cortes`: Lista de notas objetivo para las curvas de nivel.

## Desarrollo: Cómo agregar un nuevo curso

Para agregar un curso nuevo a la calculadora, debes seguir estos 3 pasos:

### 1. Definir la estructura de datos (`data/data_cursos.json`)
Agrega una entrada en el archivo `data/data_cursos.json` con la sigla del curso como clave. Debe incluir:
- `nombre`: Nombre completo del curso.
- `objetivo`: Tu nota objetivo personal.
- `evaluaciones`: Una lista de listas, donde cada sub-lista representa una evaluación: `["Nombre", Nota, Rendida (true/false), Independiente (true/false)]`.
    - *Nota*: Si no se ha rendido, pon `0.0`.
    - *Rendida*: `true` si ya tienes la nota, `false` si no.
    - *Independiente*: Generalmente `false` (uso interno).

Ejemplo:
```json
"NUEVO_CURSO": {
  "nombre": "Nombre del Nuevo Curso",
  "objetivo": 80,
  "evaluaciones": [
    ["C1", 0.0, false, false],
    ["C2", 0.0, false, false],
    ["Examen", 0.0, false, false]
  ]
}
```

### 2. Definir la función de cálculo de nota (`cursos/funciones/`)
Crea un archivo Python en `cursos/funciones/` (por ejemplo `NUEVO_CURSO.py`) que implemente la lógica para calcular la nota final.
Debe exportar una función o lambda llamada `NP` (o como prefieras, pero consistente) que reciba un array de notas `x`.

El array `x` contiene las notas en el mismo orden que las definiste en el JSON.

Ejemplo (`cursos/funciones/NUEVO_CURSO.py`):
```python
import numpy as np

# x[0] es C1, x[1] es C2, x[2] es Examen
NP = lambda x: x[0] * 0.3 + x[1] * 0.3 + x[2] * 0.4
```

### 3. Registrar el curso (`main.py`)
Finalmente, importa la función de cálculo en `main.py` y agrega el curso a la lista `cursos`.

```python
# En main.py
from cursos.funciones import NUEVO_CURSO # Importa tu nuevo módulo

# ...

cursos = [
    # ... otros cursos
    Curso("NUEVO_CURSO", NUEVO_CURSO.NP), # Agrega esta línea
]
```

Ahora tu nuevo curso aparecerá en el menú.
