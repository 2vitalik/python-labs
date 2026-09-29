from core.app import create_app
from db import MODELS
from routes import media

app = create_app(models=MODELS, routers=[media.router])
