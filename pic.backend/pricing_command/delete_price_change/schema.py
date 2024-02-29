from typing import List
from aws_lambda_powertools.utilities.parser import BaseModel


class PriceChangeDelete(BaseModel):
    site_product_price_change_id: int
    price_change_type: int

    class Config:
        from_attributes = True


class PriceChangeDeleteList(BaseModel):
    json_data: List[PriceChangeDelete]
    user_id: str

    class Config:
        from_attributes = True
