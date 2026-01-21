from dataclasses import dataclass, asdict
from decouple import config

from .redis_app.api import app

@dataclass
class AppRunSettings:
    host: str = config("APP_HOST", cast=str, default="0.0.0.0")
    port: str = config("APP_PORT", cast=int, default=8080)
    debug: str = config("APP_HOST", cast=bool, default=True)

def start_app(settings: AppRunSettings) -> None:
    settings = asdict(settings)
    app.run(**settings)
