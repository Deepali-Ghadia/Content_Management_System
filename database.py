from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# creating an instance of create_engine so that we can interact with the database through a database session
engine = create_engine('postgresql://postgres:admin@localhost/content_management_system', echo = True)

# declarative base provides a catalog of classes and their relational mappings
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)