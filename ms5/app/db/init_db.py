from app.db.database import Base
from app.db.database import engine

import app.db.models

Base.metadata.create_all(bind=engine)

logging.info("Таблицы успешно созданы.")