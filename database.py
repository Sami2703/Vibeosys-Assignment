from sqlalchemy import create_engine, Column, Integer, String, Enum, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum
from datetime import datetime


# Database setup
URL_DATABASE = "mysql+pymysql://root:root@localhost:3306/product_db"

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Enums for product category and unit of measure
class ProductCategory(enum.Enum):
    finished = "finished"
    semi_finished = "semi-finished"
    raw = "raw"

class UnitMeasure(enum.Enum):
    mtr = "mtr"
    mm = "mm"
    ltr = "ltr"
    ml = "ml"
    cm = "cm"
    mg = "mg"
    gm = "gm"
    unit = "unit"
    pack = "pack"

# SQLAlchemy Product model
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category = Column(Enum(ProductCategory), nullable=False)
    description = Column(String(250))
    productimage_url = Column(Text)
    sku = Column(String(100), unique=True, nullable=False)
    unit_of_measure = Column(Enum(UnitMeasure), nullable=False)
    lead_time = Column(Integer, nullable=False)  #in days
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



# Create tables if they do not exist
Base.metadata.create_all(bind=engine)
