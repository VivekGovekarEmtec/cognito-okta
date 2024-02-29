from aws_lambda_powertools.utilities.parser import BaseModel, Field, validator
from datetime import datetime as date_time
from typing import Optional, Literal
from decimal import Decimal


class ProductConfiguration(BaseModel):
    site_id: int
    product_id: int
    base_difference_price: Decimal = Field(..., max_digits=9, decimal_places=4)
    fs_difference_price: Decimal = Field(..., max_digits=9, decimal_places=4)
    notification_type_code: int
    is_temp_not_available: Literal[0, 1]
    effective_date: date_time
    expiry_date: date_time = Field(default=date_time(9999, 12, 31, 23, 59, 59, 999999))
    updated_by_user_id: str
    pos_product_grade: Optional[str]
    run_out_product_id: Optional[int]
    regulated_prices_reference_value_id: Optional[int]

    @validator("effective_date", "expiry_date")
    def set_timezone_to_none(cls, value):
        # Explicitly set the timezone to None
        return value.replace(tzinfo=None)

    class Config:
        from_attributes = True


class UpdateSiteProductConfig(BaseModel):
    site_id: int
    product_id: int
    base_difference_price: Decimal = Field(..., max_digits=9, decimal_places=4)
    fs_difference_price: Decimal = Field(..., max_digits=9, decimal_places=4)
    notification_type_code: int
    is_temp_not_available: int
    effective_date: date_time
    expiry_date: date_time = Field(default=date_time(9999, 12, 31, 23, 59, 59, 999999))
    updated_by_user_id: str
    pos_product_grade: Optional[str]
    run_out_product_id: Optional[int]
    regulated_prices_reference_value_id: Optional[int]

    @validator("effective_date", "expiry_date")
    def set_timezone_to_none(cls, value):
        # Explicitly set the timezone to None
        return value.replace(tzinfo=None)

    class Config:
        from_attributes = True
