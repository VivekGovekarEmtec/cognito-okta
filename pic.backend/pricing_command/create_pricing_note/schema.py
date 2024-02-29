from typing import Optional
from aws_lambda_powertools.utilities.parser import BaseModel, Field, validator
from datetime import datetime


class CreatePricingNote(BaseModel):
    site_id: int
    gaz_note: str | None = Field(default=None)
    gaz_note_last_user: str | None = Field(default=None)
    gaz_note_last_change_date: Optional[datetime] = None
    dsl_note: str | None = Field(default=None)
    dsl_note_last_user: str | None = Field(default=None)
    dsl_note_last_change_date: Optional[datetime] = None
    promo_note: str | None = Field(default=None)
    promo_note_last_user: str | None = Field(default=None)
    promo_note_last_change_date: Optional[datetime] = None
    temporary_note: str | None = Field(default=None)
    temporary_note_last_user: str | None = Field(default=None)
    temporary_note_last_change_date: Optional[datetime] = None
    user_id: str

    class Config:
        from_attributes = True

    @validator("gaz_note_last_change_date", "dsl_note_last_change_date", "promo_note_last_change_date",
               "temporary_note_last_change_date")
    def set_timezone_to_none(cls, value):
        if value:
            return value.replace(tzinfo=None)
        return None
