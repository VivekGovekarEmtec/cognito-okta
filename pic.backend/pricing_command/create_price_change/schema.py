from decimal import Decimal
from aws_lambda_powertools.utilities.parser import BaseModel, Field
from datetime import datetime


class CreatePriceChange(BaseModel):
    site_id: int
    product_id: int = Field(gt=0)
    request_date: datetime
    request_price: Decimal = Field(..., max_digits=9, decimal_places=4, ge=0)
    comment: str = Field(max_length=1000)
    move_with: str
    hierarchy_header_id: int = Field(ge=0)
    site_list: str | None
    over_write_notification_type_with: int
    user_id: str = Field(max_length=200)
    is_auto_authorization: bool = Field(default=False)
    is_request_now: int = Field(default=0, ge=0)


class PriceChangeValidation(BaseModel):
    is_valid: bool