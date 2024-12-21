from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definir la base para crear las tablas
Base = declarative_base()

# Definir el modelo de la base de datos
class Task(Base):
    __tablename__ = 'tasks'  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True)  # ID de la tarea
    title = Column(String)  # Título de la tarea
    description = Column(String)  # Descripción de la tarea

# Crear una instancia del motor de SQLAlchemy usando Windows Authentication
DATABASE_URL = 'mssql+pyodbc://@ALEJANDRO\MSSQLSERVER01/TaskManager?driver=ODBC+Driver+17+for+SQL+Server;Trusted_Connection=yes'
engine = create_engine(DATABASE_URL)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()
    
