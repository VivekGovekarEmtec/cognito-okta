from decimal import Decimal
from typing import Optional
from aws_lambda_powertools.utilities.parser import BaseModel, Field
from datetime import datetime


class InsertPriceHeader(BaseModel):
    authorization_number: Optional[int] = None
    effective_date: datetime
    file_input: str
    zone1_regular_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone1_regular_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone1_diesel_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone1_diesel_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone2_regular_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone2_regular_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone2_diesel_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone2_diesel_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone3_regular_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone3_regular_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone3_diesel_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone3_diesel_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone4_regular_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone4_regular_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone4_diesel_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone4_diesel_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone5_regular_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone5_regular_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone5_diesel_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone5_diesel_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone6_regular_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone6_regular_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone6_diesel_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone6_diesel_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone1_plus_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone1_plus_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone1_supreme_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone1_supreme_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone2_plus_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone2_plus_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone2_supreme_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone2_supreme_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone3_plus_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone3_plus_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone3_supreme_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone3_supreme_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone4_plus_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone4_plus_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone4_supreme_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone4_supreme_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone5_plus_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone5_plus_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone5_supreme_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone5_supreme_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone6_plus_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone6_plus_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone6_supreme_min: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    zone6_supreme_max: Optional[Decimal] = Field(max_digits=9, decimal_places=3)
    inserted_user_id: str

    class config:
        from_attributes = True
