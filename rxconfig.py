import reflex as rx
from reflex_base.plugins.sitemap import SitemapPlugin

config = rx.Config(
    app_name="prompt_app",
    frontend_port=3003,
    backend_port=8001,
    disable_plugins=[SitemapPlugin],
)