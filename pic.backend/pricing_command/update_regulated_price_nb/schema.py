from aws_lambda_powertools.utilities.parser import BaseModel, Field
from decimal import Decimal
from typing import List


class JsonData(BaseModel):
    site_id: int
    regular_pump_price: Decimal = Field(max_digits=9, decimal_places=1)
    plus_pump_price: Decimal = Field(max_digits=9, decimal_places=1)
    supreme_pump_price: Decimal = Field(max_digits=9, decimal_places=1)
    diesel_pump_price: Decimal = Field(max_digits=9, decimal_places=1)


class UpdateRegulatedPrice(BaseModel):
    authorization_number: int
    json_data: List[JsonData]
    user_id: str
