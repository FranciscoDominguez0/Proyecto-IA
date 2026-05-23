import reflex as rx
import httpx

class Estado(rx.State):
    instruccion: str = ""
    contexto: str = ""
    salida: str = ""
    restricciones: str = ""
    modelo: str = "gemini"
    respuesta: str = ""
    cargando: bool = False

    def set_instruccion(self, value: str):
        self.instruccion = value

    def set_contexto(self, value: str):
        self.contexto = value

    def set_salida(self, value: str):
        self.salida = value

    def set_restricciones(self, value: str):
        self.restricciones = value

    def set_modelo(self, value: str):
        self.modelo = value

    def limpiar(self):
        self.respuesta = ""

    async def enviar(self):
        self.cargando = True
        self.respuesta = ""
        yield

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                "http://localhost:8001/generar",
                json={
                    "instruccion": self.instruccion,
                    "contexto": self.contexto,
                    "salida": self.salida,
                    "restricciones": self.restricciones,
                    "modelo": self.modelo,
                }
            )
            self.respuesta = r.json().get("respuesta", "Error.")

        self.cargando = False

def index():
    return rx.vstack(
        rx.heading("PromptForge"),

        rx.text("1. Instrucción"),
        rx.text_area(placeholder="¿Qué debe hacer la IA?",
                     on_change=Estado.set_instruccion, width="100%"),

        rx.text("2. Contexto"),
        rx.text_area(placeholder="Marco de referencia",
                     on_change=Estado.set_contexto, width="100%"),

        rx.text("3. Salida esperada"),
        rx.text_area(placeholder="Tipo de respuesta que quieres",
                     on_change=Estado.set_salida, width="100%"),

        rx.text("4. Restricciones"),
        rx.text_area(placeholder="Límites o condiciones",
                     on_change=Estado.set_restricciones, width="100%"),

        rx.select(["gemini", "deepseek"], default_value="gemini",
                  on_change=Estado.set_modelo),

        rx.hstack(
            rx.button("Generar respuesta", on_click=Estado.enviar,
                      loading=Estado.cargando),
            rx.button("Limpiar", on_click=Estado.limpiar,
                      color_scheme="red"),
        ),

        rx.cond(
            Estado.respuesta != "",
            rx.box(
                rx.markdown(Estado.respuesta),
                padding="1em",
                border="1px solid #ccc",
                border_radius="8px",
                width="100%",
            )
        ),

        spacing="4", max_width="680px", margin="auto", padding="2em"
    )

app = rx.App()
app.add_page(index)