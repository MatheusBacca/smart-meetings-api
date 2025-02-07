import database.models as models
from database.database import engine
from util.utils import create_app

app = create_app()

models.Base.metadata.create_all(bind=engine)
