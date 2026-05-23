# Prompt AI App

Aplicación web de prompts con **FastAPI** y **Reflex**. El backend expone una API para generar respuestas con Gemini o DeepSeek y la interfaz permite enviar prompts desde la web.

## Estructura del proyecto

```text
prompt-ai-app/
│
├── .env                    ← una única variable de entorno
├── main.py                 ← FastAPI (del profe, extendido)
├── rxconfig.py             ← configuración de Reflex
├── requirements.txt        ← todas las librerías
├── venv/                   ← un solo entorno virtual
│
└── prompt_app/
    ├── __init__.py
    └── prompt_app.py       ← la UI en Reflex
```

## Requisitos previos

- Python 3.10 o superior
- `pip`
- Una clave API de Gemini y, si la vas a usar, una clave de DeepSeek

## 1) Crear y activar el entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

> Si usas PowerShell y te aparece un error por ejecución de scripts, ejecuta primero:
>
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```

## 2) Instalar dependencias

```bash
pip install -r requirements.txt
```

## 3) Crear el archivo `.env`

En la raíz del proyecto crea un archivo `.env` con estas variables:

```env
GEMINI_API_KEY=TU_API_KEY_DE_GEMINI
DEEPSEEK_API_KEY=TU_API_KEY_DE_DEEPSEEK
```

Si solo vas a usar Gemini, puedes dejar `DEEPSEEK_API_KEY` vacío o eliminarla.

## 4) Ejecutar la aplicación

### Backend (FastAPI)

```bash
uvicorn main:app --reload --port 8001
```

### Frontend (Reflex)

```bash
reflex run
```

## 5) Abrir la app

- Backend: `http://localhost:8001`
- Frontend: la URL que te muestra Reflex al iniciar

## 6) Solución de problemas comunes

### Error: `ModuleNotFoundError`

Asegúrate de haber activado el entorno virtual antes de instalar o ejecutar:

```bash
venv\Scripts\activate
```

### Error: `No module named dotenv` o `No module named reflex`

Vuelve a instalar dependencias:

```bash
pip install -r requirements.txt
```

### No se detecta `.env`

Verifica que el archivo se llame exactamente `.env` y que esté en la raíz del proyecto.

## Variables usadas en la app

- `GEMINI_API_KEY`: necesaria para el modelo Gemini.
- `DEEPSEEK_API_KEY`: opcional, solo si vas a usar DeepSeek.

## Notas

- El backend se inicia con `uvicorn` y el frontend con `reflex run`.
- La app ya incluye la estructura base para trabajar en una sola carpeta y un único entorno virtual.
