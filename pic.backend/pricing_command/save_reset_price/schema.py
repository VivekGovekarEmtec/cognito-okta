from typing import List
from aws_lambda_powertools.utilities.parser import BaseModel
from datetime import datetime as date_time


class SiteProductPrice(BaseModel):
    site_id: int
    effective_date: date_time

    class Config:
        from_attributes = True


class SiteProductPriceChange(BaseModel):
    outlet_data: List[SiteProductPrice]
    product_id: int
    price: float
    user_id: str

    class Config:
        from_attributes = True
