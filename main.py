from logging import Logger
from configobj import ConfigObj
import uvicorn
import database.models as models
from database.database import engine
from util.logger import setup_logger
from util.utils import create_app

app = create_app()

models.Base.metadata.create_all(bind=engine)

logger: Logger = setup_logger(__name__)
if __name__ == "__main__":
    config = ConfigObj("config.cfg")
    host: str = config["SERVICE"].get("HOST")
    if not host:
        host: str = "127.0.0.1"

    port: int = int(config["SERVICE"].get("PORT"))
    if not port:
        port: int = 8000

    app_server = uvicorn.run(app, host=host, port=port)
