import reflex as rx
import httpx

BG, CARD, SURFACE = "#0c0c0e", "#131316", "#1a1a1f"
BORDER, TEXT, MUTED = "#26262e", "#e8e4dc", "#6b6b7e"
GREEN, VIOLET = "#4ade80", "#a78bfa"

class Estado(rx.State):
    instruccion: str = ""
    contexto: str = ""
    salida: str = ""
    restricciones: str = ""
    modelo: str = "gemini"
    respuesta: str = ""
    cargando: bool = False

    def set_instruccion(self, value: str): self.instruccion = value
    def set_contexto(self, value: str):    self.contexto = value
    def set_salida(self, value: str):      self.salida = value
    def set_restricciones(self, value: str): self.restricciones = value
    def set_modelo(self, value: str):      self.modelo = value
    def limpiar(self):                     self.respuesta = ""

    async def enviar(self):
        self.cargando = True
        self.respuesta = ""
        yield
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post("http://localhost:8001/generar", json={
                "instruccion": self.instruccion,
                "contexto": self.contexto,
                "salida": self.salida,
                "restricciones": self.restricciones,
                "modelo": self.modelo,
            })
            self.respuesta = r.json().get("respuesta", "Error.")
        self.cargando = False


def campo(num, label, ph, handler):
    return rx.vstack(
        rx.text(f"{num}  {label}", font_size="11px", color=MUTED, font_weight="600", letter_spacing="0.08em"),
        rx.text_area(placeholder=ph, on_change=handler, rows="3", width="100%",
            padding="12px 14px", font_size="14px", background=SURFACE, color=TEXT,
            border=f"1px solid {BORDER}", border_radius="10px", resize="none",
            _focus={"border_color": GREEN, "outline": "none", "box_shadow": f"0 0 0 3px {GREEN}20"},
            _placeholder={"color": "#3a3a48"}),
        spacing="2", width="100%",
    )

def chip(label, val, color):
    on = Estado.modelo == val
    return rx.box(
        rx.text(label, font_size="11px", font_weight="600", color=rx.cond(on, "#0c0c0e", MUTED)),
        padding="6px 18px", border_radius="999px", cursor="pointer",
        background=rx.cond(on, color, "transparent"),
        border="1px solid", border_color=rx.cond(on, color, BORDER),
        on_click=Estado.set_modelo(val), transition="all 0.2s",
        _hover={"border_color": color, "color": color},
    )

def index():
    return rx.box(
        rx.hstack(
            rx.text("Prompt ", font_size="20px", font_weight="700", color=TEXT),
            rx.text("Api", font_size="20px", font_weight="300", color=MUTED),
            rx.spacer(),
            rx.hstack(
                rx.box(width="7px", height="7px", border_radius="50%", background=GREEN, box_shadow=f"0 0 8px {GREEN}"),
                rx.text("activo", font_size="11px", color=GREEN),
                spacing="2", align="center",
            ),
            width="100%", align="center", padding="18px 32px",
            background=CARD, border_bottom=f"1px solid {BORDER}",
        ),
        rx.hstack(
            rx.vstack(
                campo("01", "INSTRUCCIÓN",   "¿Qué debe hacer el modelo?", Estado.set_instruccion),
                campo("02", "CONTEXTO",      "¿Qué información necesita?", Estado.set_contexto),
                campo("03", "SALIDA",        "¿Qué formato de respuesta?", Estado.set_salida),
                campo("04", "RESTRICCIONES", "¿Qué debe evitar?",          Estado.set_restricciones),
                rx.hstack(
                    rx.button("Ejecutar", on_click=Estado.enviar, loading=Estado.cargando,
                        flex="1", padding="12px", border_radius="10px", border="none",
                        background=f"linear-gradient(135deg, {GREEN}, #22c55e)", color=BG,
                        font_size="13px", font_weight="600", cursor="pointer",
                        _hover={"opacity": "0.85"}, transition="all 0.2s"),
                    rx.button("Limpiar", on_click=Estado.limpiar,
                        padding="12px 20px", border_radius="10px", cursor="pointer",
                        background="transparent", color=MUTED, border=f"1px solid {BORDER}",
                        font_size="13px", transition="all 0.2s"),
                    width="100%", spacing="3",
                ),
                spacing="4", width="42%", padding="28px 24px",
                background=CARD, border_right=f"1px solid {BORDER}",
                min_height="calc(100vh - 61px)",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text("Respuesta", font_size="14px", font_weight="600", color=TEXT),
                    rx.spacer(),
                    chip("Gemini", "gemini", GREEN),
                    chip("DeepSeek", "deepseek", VIOLET),
                    width="100%", align="center", spacing="2",
                ),
                rx.box(height="1px", width="100%", background=BORDER),
                rx.cond(Estado.cargando,
                    rx.vstack(rx.spinner(size="3", color=VIOLET),
                        rx.text("Generando…", font_size="12px", color=VIOLET),
                        align="center", justify="center", height="360px", width="100%", spacing="3"),
                    rx.cond(Estado.respuesta != "",
                        rx.box(rx.markdown(Estado.respuesta), width="100%",
                            overflow_y="auto", max_height="calc(100vh - 180px)",
                            font_size="14px", line_height="1.85", color=TEXT),
                        rx.vstack(
                            rx.icon("message-square-dashed", size=32, color="#3a3a48"),
                            rx.text("Aquí aparecerá la respuesta", font_size="12px", color=MUTED),
                            align="center", justify="center", height="360px", width="100%", spacing="3"),
                    ),
                ),
                spacing="4", width="58%", padding="28px 32px",
                background=BG, min_height="calc(100vh - 61px)",
            ),
            spacing="0", width="100%", align="start",
        ),
        background=BG, min_height="100vh", font_family="'DM Sans', sans-serif",
    )

app = rx.App(stylesheets=[
    "https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap"
])
app.add_page(index)