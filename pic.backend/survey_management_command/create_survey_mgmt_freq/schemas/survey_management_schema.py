from aws_lambda_powertools.utilities.parser import BaseModel, Field, validator
from datetime import datetime


class CreateSurveyManagement(BaseModel):
    site_id: int
    kent_id: str
    product_id: int
    new_frequency: str = Field(max_length=7, min_length=7)
    effective_date: datetime
    expiry_date: datetime
    from_1: str | None = Field(max_length=5, default=None, min_length=5)
    to_1: str | None = Field(max_length=5, default=None, min_length=5)
    from_2: str | None = Field(max_length=5, default=None, min_length=5)
    to_2: str | None = Field(max_length=5, default=None, min_length=5)
    from_3: str | None = Field(max_length=5, default=None, min_length=5)
    to_3: str | None = Field(max_length=5, default=None, min_length=5)
    from_4: str | None = Field(max_length=5, default=None, min_length=5)
    to_4: str | None = Field(max_length=5, default=None, min_length=5)
    from_5: str | None = Field(max_length=5, default=None, min_length=5)
    to_5: str | None = Field(max_length=5, default=None, min_length=5)
    user: str | None

    @validator("effective_date", "expiry_date")
    def set_timezone_to_none(cls, value):
        """
        This pydantic custom validator function is used to set time zone as none
        """
        # Explicitly set the timezone to None
        return value.replace(tzinfo=None)


    class Config:
        from_attributes = True
