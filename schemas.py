from pydantic import BaseModel
from enum import Enum
from typing import Optional

class ProductCategory(str, Enum):
    finished = "finished"
    semi_finished = "semi-finished"
    raw = "raw"

class UnitMeasure(str, Enum):
    mtr = "mtr"
    mm = "mm"
    ltr = "ltr"
    ml = "ml"
    cm = "cm"
    mg = "mg"
    gm = "gm"
    unit = "unit"
    pack = "pack"

class ProductBase(BaseModel):
    name: str
    category: ProductCategory
    description: Optional[str] = None
    productimage_url: Optional[str] = None
    sku: str
    unit_of_measure: UnitMeasure
    lead_time: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_date: str
    updated_date: str

    class Config:
        orm_mode = True
