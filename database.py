from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgres://plxhwoqjoonrmr:243ffc530c3060e6892fe03b38a851daae7b21949a1d4444a88e5c8296bc3a61@ec2-3-213-106-122.compute-1.amazonaws.com:5432/dc1hgrgjvsg0bf"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()