# Proyecto de Microservicio ECG con FastAPI

Este proyecto implementa un microservicio basado en FastAPI que permite el procesamiento de electrocardiogramas (ECG) y proporciona insights sobre estos, como el conteo de cruces de cero en la señal.

## Características

- API RESTful construida con **FastAPI**.
- Gestión de datos de ECG con **SQLAlchemy** y **SQLite**.
- **Autenticación con JWT** para proteger los endpoints.
- **CRUD** de datos de ECG con endpoints protegidos.
- Generación de insights (cruces de cero) para cada señal de ECG.

## Requisitos

- Python 3.8 o superior
- Paquetes especificados en `requirements.txt`

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/antonioruizm/prueba-idoven.git
   cd prueba-idoven

2. Crea y activa un entorno virtual:

    python3 -m venv entorno
    source entorno/bin/activate  # En Windows usa `entorno\Scripts\activate`

3. Instala las dependencias:

  pip install -r requirements.txt


## Uso
Ejecutar el Servidor

Para iniciar el servidor de desarrollo de FastAPI, ejecuta:

uvicorn main:app --reload

El servidor estará disponible en http://127.0.0.1:8000


## Documentación de la API

La documentación interactiva de la API está disponible en:

    Swagger UI: http://127.0.0.1:8000/docs
    ReDoc: http://127.0.0.1:8000/redoc

## Endpoints Principales

    POST /register/ - Registra un nuevo usuario.
    POST /token - Genera un token JWT para autenticarse.
    POST /ecgs/ - Crea un nuevo registro de ECG (requiere autenticación).
    GET /ecgs/{ecg_id}/insights - Obtiene los insights de un ECG específico (requiere autenticación).

## Ejemplos de Uso

Para probar los endpoints protegidos, primero registra un usuario y luego genera un token usando /token. Usa este token para autenticar las solicitudes a los endpoints protegidos.
Ejemplo de Registro de Usuario

POST /register/
{
  "username": "testuser",
  "password": "testpassword"
}

Ejemplo de Creación de un ECG

POST /ecgs/
{
  "id": 1,
  "date": "2024-01-01T00:00:00Z",
  "leads": [
      {"name": "I", "signal": [1, -1, 2, -2, 3]},
      {"name": "II", "signal": [-1, 1, -2, 2, -3]}
  ]
}

Ejemplo de Obtención de Insights de ECG

GET /ecgs/1/insights

Este endpoint devuelve el conteo de cruces de cero para cada lead.
