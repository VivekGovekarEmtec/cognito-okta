from aws_lambda_powertools.utilities.parser import BaseModel
from datetime import datetime as date_time


class PriceOnHoldUpdate(BaseModel):
    site_no: int
    product_id: int
    effective_date: date_time
    expiry_date: date_time
    user_id: str
    notes: str

    class Config:
        from_attributes = True
