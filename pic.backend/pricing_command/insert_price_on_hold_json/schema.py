from aws_lambda_powertools.utilities.parser import BaseModel
from datetime import datetime as date_time
from typing import List


class PriceOnHoldInsert(BaseModel):
    site_no: int
    product_id: int
    effective_date: date_time
    expiry_date: date_time

    class Config:
        from_attributes = True


class PriceOnHoldInsertList(BaseModel):
    json_data: List[PriceOnHoldInsert]
    user_id: str
    notes: str
