from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)

# Base.metadata.create_all(bind=engine)
Session = sessionmaker(autoflush=False, bind=engine)
