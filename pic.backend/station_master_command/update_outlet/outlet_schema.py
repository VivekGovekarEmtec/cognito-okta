from aws_lambda_powertools.utilities.parser import BaseModel, Field, validator
from datetime import datetime
from decimal import Decimal

class UpdateSite(BaseModel):
    site_no: int = Field(...)
    alternative_site_no: str = Field(max_length=10, default=None)
    name: str = Field(max_length=100, default=None)
    retailer_name: str = Field(max_length=100, default=None)
    brand_id: int
    address: str = Field(max_length=100, default=None)
    cross_street: str = Field(max_length=100, default=None)
    city_id: int
    facility_type_id: int
    status_id: int
    language_id: int
    timezone_id: int
    territory_manager_id: int
    hierarchy_id: int
    pin: str = Field(max_length=20, default=None)
    is_regie_energy: Decimal = Field(max_digits=1, decimal_places=0, default=0)
    is_daily_reset_applicable: Decimal = Field(max_digits=1, decimal_places=0, default=0)
    reset_time: str = Field(..., max_length=5)
    reset_next_day: Decimal = Field(max_digits=1, decimal_places=0, default=None)
    pump_configuration_template: int
    latitude: Decimal = Field(max_digits=12, decimal_places=8)
    longitude: Decimal = Field(max_digits=12, decimal_places=8)
    radius_for_tableau: int = Field(default=5)
    user_id: str = Field(..., max_length=50)
    survey_submission_count: int = Field(default=None)
    confidence_score: Decimal = Field(max_digits=6, decimal_places=3, default=None)
    auto_clear_start_time: str = Field(min_length=5, max_length=5, default=None)
    auto_clear_end_time: str = Field(min_length=5, max_length=5, default=None)
    is_gas_buddy_active: Decimal = Field(..., max_digits=1, decimal_places=0)
    tactic_regular_pricing_zoneId: int = Field(default=None)
    tactic_regular_price_differential: Decimal = Field(max_digits=9, decimal_places=4, default=None)
    tactic_diesel_pricing_zone_id: int
    tactic_diesel_price_differential: Decimal = Field(max_digits=9, decimal_places=4, default=None)
    is_rounding_9: Decimal = Field(max_digits=1, decimal_places=0)
    is_rounding_0: Decimal = Field(max_digits=1, decimal_places=0)
    rack_fwd_missing_time: str = Field(max_length=5, default=None)
    rack_fwd_missing_time_active: Decimal = Field(max_digits=1, decimal_places=0, default=None)
    effective_date: datetime = Field(default=None)
    expiry_date: datetime = Field(default=None)

    @validator("effective_date", "expiry_date")
    def set_timezone_to_none(cls, value):
        # Explicitly set the timezone to None
        return value.replace(tzinfo=None)

    class Config:
        from_attributes = True