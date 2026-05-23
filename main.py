from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(
    title="PromptForge API",
    description="API que recibe un prompt estructurado y llama a Gemini o Grok",
    version="1.0"
)

class PromptData(BaseModel):
    instruccion: str
    contexto: str
    salida: str
    restricciones: str
    modelo: str

@app.post("/generar")
def generar(datos: PromptData):
    prompt = f"""Instrucción: {datos.instruccion}
Contexto: {datos.contexto}
Salida esperada: {datos.salida}
Restricciones: {datos.restricciones}

IMPORTANTE: Responde en texto claro y bien estructurado."""

    if datos.modelo == "gemini":
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            return {"respuesta": response.text}
        except Exception as e:
            return {"respuesta": f"Error con Gemini: {str(e)}"}

    elif datos.modelo == "grok":
        try:
            r = requests.post(
                "https://api.x.ai/v1/responses",
                headers={
                    "Authorization": f"Bearer {os.getenv('GROK_API_KEY')}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-4.20-reasoning",
                    "input": prompt
                }
            )

            print("Status code:", r.status_code)
            print("Respuesta Grok:", r.text)

            if r.status_code != 200:
                return {"respuesta": f"Error de Grok ({r.status_code}): {r.text}"}

            data = r.json()
            return {"respuesta": data["output"][0]["content"][0]["text"]}

        except Exception as e:
            return {"respuesta": f"Error con Grok: {str(e)}"}

    return {"respuesta": "Modelo no reconocido. Usa 'gemini' o 'grok'."}