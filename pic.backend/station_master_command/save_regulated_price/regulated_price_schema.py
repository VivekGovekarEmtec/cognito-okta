from typing import Optional
from aws_lambda_powertools.utilities.parser import BaseModel, Field
from decimal import Decimal


class RegulatePriceSchema(BaseModel):
    site_no: int
    zone_id: Optional[int]
    gas_full_serve_adjustment: Decimal = Field(default=0,max_digits=9,decimal_places=1)
    diesel_full_serve_adjustment: Decimal = Field(default=0,max_digits=9,decimal_places=1)
    gas_adjustment: Optional[Decimal] = Field(max_digits=9, decimal_places=1)
    diesel_adjustment: Optional[Decimal] = Field(max_digits=9, decimal_places=1)
    user_id: str = Field(max_length=50)
    id: Optional[int]

    class Config:
        from_attributes = True
