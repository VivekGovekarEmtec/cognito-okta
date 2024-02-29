from aws_lambda_powertools.utilities.parser import BaseModel, validator
from datetime import datetime as date_time


class TemporaryClose(BaseModel):
    site_no: int
    effective_date: date_time
    expiry_date: date_time

    @validator("effective_date", "expiry_date")
    def set_timezone_to_none(cls, value):
        # Explicitly set the timezone to None
        return value.replace(tzinfo=None)

    class Config:
        from_attributes = True