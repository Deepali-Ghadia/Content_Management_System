from database import Base, engine
import models

print("Creating database...")
# metadata.create_all creates a table for all the classes that we have provided in the models.py file. These classes are inherited from Base class and Base class is an instance of declarative_base()
Base.metadata.create_all(engine)

print("Database created successfully")