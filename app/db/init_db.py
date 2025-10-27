from app.db.database import base, engine


base.metadata.create_all(bind=engine)
