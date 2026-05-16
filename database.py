from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(autoflush=False, bind=engine)


if __name__ == '__main__':
    from models import Base

    Base.metadata.create_all(bind=engine)

