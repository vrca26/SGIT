import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carga el .env solo en desarrollo local
load_dotenv()

# Usa variable de entorno DATABASE_URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    print("Error: DATABASE_URL no está definida en el entorno.")

# Crear engine y sesión
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
