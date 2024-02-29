from aws_lambda_powertools.utilities.parser import BaseModel, Field
from datetime import datetime


class CreatePriceOnHold(BaseModel):
    site_id: str
    product_id: int
    effective_date: datetime
    expiry_date: datetime
    user_id: str
    note: str = Field(default=None)
