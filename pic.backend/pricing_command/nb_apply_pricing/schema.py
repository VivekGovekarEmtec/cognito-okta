from aws_lambda_powertools.utilities.parser import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class NBApplyPricing(BaseModel):
    effective_date: datetime
    ref_date_1: datetime
    ref_date_2: datetime
    regular_retail_price: Decimal = Field(max_digits=9, decimal_places=3)
    regular_retail_with_delivery_price: Decimal = Field(max_digits=9, decimal_places=3)
    regular_full_serve_with_delivery_price: Decimal = Field(max_digits=9, decimal_places=3)
    regular_to_plus_diff: Decimal = Field(max_digits=9, decimal_places=3)
    plus_retail_price: Decimal = Field(max_digits=9, decimal_places=3)
    plus_retail_with_delivery_price: Decimal = Field(max_digits=9, decimal_places=3)
    plus_full_serve_with_delivery_price: Decimal = Field(max_digits=9, decimal_places=3)
    regular_to_supreme_diff: Decimal = Field(max_digits=9, decimal_places=3)
    supreme_retail_price: Decimal = Field(max_digits=9, decimal_places=3)
    supreme_retail_with_delivery_price: Decimal = Field(max_digits=9, decimal_places=3)
    supreme_full_serve_with_delivery_price: Decimal = Field(max_digits=9, decimal_places=3)
    diesel_retail_price: Decimal = Field(max_digits=9, decimal_places=3)
    diesel_retail_with_delivery_price: Decimal = Field(max_digits=9, decimal_places=3)
    diesel_full_serve_with_delivery_price: Decimal = Field(max_digits=9, decimal_places=3)
    inserted_user_id: str
    auth_number: int = Field(default=None)
