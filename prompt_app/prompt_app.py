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


def campo(numero: str, label: str, placeholder: str, handler):
    return rx.vstack(
        rx.hstack(
            rx.box(
                rx.text(numero, font_size="10px", color="#00ff88",
                        font_weight="700", letter_spacing="0.1em"),
                background="#00ff8815",
                padding="2px 8px",
                border_radius="3px",
                border="1px solid #00ff8830",
            ),
            rx.text(label, font_size="11px", color="#aaa",
                    font_weight="700", letter_spacing="0.12em"),
            spacing="2", align="center",
        ),
        rx.text_area(
            placeholder=placeholder,
            on_change=handler,
            width="100%", min_height="72px",
            padding="10px 12px", font_size="13px",
            background="#0a0a0a", color="#e0e0e0",
            border="1px solid #222", border_radius="6px",
            _focus={
                "border_color": "#00ff88",
                "outline": "none",
                "box_shadow": "0 0 0 1px #00ff8818",
            },
            _placeholder={"color": "#333"},
            resize="none",
        ),
        spacing="2", width="100%",
    )


def boton_modelo(label: str, valor: str):
    activo = Estado.modelo == valor
    return rx.box(
        rx.text(label, font_size="10px", font_weight="700",
                color=rx.cond(activo, "#0a0a0a", "#777"),
                letter_spacing="0.08em"),
        padding="5px 16px", border_radius="4px",
        background=rx.cond(activo, "#00ff88", "transparent"),
        border="1px solid",
        border_color=rx.cond(activo, "#00ff88", "#252525"),
        cursor="pointer",
        on_click=Estado.set_modelo(valor),
        transition="all 0.15s ease",
        _hover={"border_color": "#00ff88", "color": "#00ff88"},
    )


def pensando():
    return rx.vstack(
        rx.spinner(size="3", color="#00ff88"),
        rx.text("PENSANDO", font_size="11px", color="#00ff88",
                font_weight="700", letter_spacing="0.2em"),
        align="center",
        justify="center",
        height="320px",
        width="100%",
    )


def index():
    return rx.box(

        # Header
        rx.hstack(
            rx.hstack(
                rx.box(
                    rx.text("PROYECTO", font_size="9px", font_weight="700",
                            color="#00ff88", letter_spacing="0.2em"),
                    background="#00ff8812",
                    padding="3px 10px",
                    border_radius="3px",
                    border="1px solid #00ff8825",
                ),
                rx.text("/", font_size="16px", color="#252525",
                        font_weight="300"),
                rx.text("APIS", font_size="20px", font_weight="800",
                        color="white", letter_spacing="0.06em"),
                spacing="3", align="center",
            ),
            rx.spacer(),
            rx.hstack(
                rx.box(width="7px", height="7px", border_radius="50%",
                       background="#00ff88",
                       box_shadow="0 0 8px #00ff8870"),
                rx.text("Sistema activo", font_size="11px", color="#00ff88",
                        font_weight="600", letter_spacing="0.08em"),
                spacing="2", align="center",
            ),
            width="100%", align="center",
            padding="16px 32px",
            background="#0f0f0f",
            border_bottom="1px solid #1a1a1a",
        ),

        # Cuerpo
        rx.hstack(

            # Panel izquierdo — formulario
            rx.vstack(
                rx.hstack(
                    rx.box(width="3px", height="14px",
                           background="#00ff88", border_radius="2px"),
                    rx.text("Constructor de Prompt", font_size="11px",
                            color="#777", letter_spacing="0.08em",
                            font_weight="600"),
                    spacing="2", align="center",
                ),
                campo("01", "INSTRUCCION",
                      "Define la tarea principal...",
                      Estado.set_instruccion),
                campo("02", "CONTEXTO",
                      "Marco de referencia...",
                      Estado.set_contexto),
                campo("03", "SALIDA",
                      "Formato de respuesta esperado...",
                      Estado.set_salida),
                campo("04", "RESTRICCIONES",
                      "Limites y condiciones...",
                      Estado.set_restricciones),

                rx.hstack(
                    rx.button(
                        "Ejecutar",
                        on_click=Estado.enviar,
                        loading=Estado.cargando,
                        flex="1", padding="12px",
                        background="#00ff88", color="#0a0a0a",
                        font_size="12px", font_weight="800",
                        border_radius="6px", letter_spacing="0.1em",
                        cursor="pointer",
                        _hover={"background": "#00e07a"},
                        transition="all 0.15s ease",
                    ),
                    rx.button(
                        "Limpiar",
                        on_click=Estado.limpiar,
                        padding="12px 20px",
                        background="transparent", color="#555",
                        font_size="12px", font_weight="600",
                        border_radius="6px", border="1px solid #222",
                        cursor="pointer",
                        _hover={"border_color": "#555", "color": "#888"},
                        transition="all 0.15s ease",
                    ),
                    width="100%", spacing="3",
                ),

                spacing="4", width="42%",
                padding="24px 28px",
                background="#111",
                border_right="1px solid #1a1a1a",
                min_height="calc(100vh - 69px)",
            ),

            # Panel derecho — output
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.box(width="3px", height="14px",
                               background="#00ff88", border_radius="2px"),
                        rx.text("Output", font_size="11px", color="#777",
                                letter_spacing="0.08em", font_weight="600"),
                        spacing="2", align="center",
                    ),
                    rx.spacer(),
                    rx.hstack(
                        boton_modelo("GEMINI", "gemini"),
                        boton_modelo("DEEPSEEK", "deepseek"),
                        spacing="2",
                    ),
                    width="100%", align="center",
                ),

                rx.box(
                    height="1px", width="100%",
                    background="linear-gradient(90deg, #00ff88, transparent)",
                ),

                rx.cond(
                    Estado.cargando,
                    pensando(),
                    rx.cond(
                        Estado.respuesta != "",
                        rx.box(
                            rx.markdown(Estado.respuesta),
                            width="100%",
                            overflow_y="auto",
                            max_height="calc(100vh - 160px)",
                            font_size="14px", color="#ccc",
                            line_height="1.9",
                        ),
                        rx.vstack(
                            rx.text("_", font_size="40px",
                                    color="#1c1c1c", font_weight="800"),
                            rx.text("esperando prompt",
                                    font_size="10px", color="#252525",
                                    letter_spacing="0.18em"),
                            align="center", justify="center",
                            height="320px", width="100%",
                        ),
                    ),
                ),

                spacing="4", width="58%",
                padding="24px 28px",
                background="#0d0d0d",
                min_height="calc(100vh - 69px)",
            ),

            spacing="0", width="100%", align="start",
        ),

        background="#0a0a0a",
        min_height="100vh",
        font_family="'JetBrains Mono', monospace",
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&display=swap"
    ]
)
app.add_page(index)