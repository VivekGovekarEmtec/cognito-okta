from aws_lambda_powertools.utilities.parser import BaseModel, validator
from datetime import datetime
from typing import List


class UpdateCompetitorSitesJsonData(BaseModel):
    id: int
    regular: float
    diesel: float

    class Config:
        from_attributes = True


class UpdateCompetitorSites(BaseModel):
    site_no: int
    survey_date: datetime
    reason_code: str
    json_data: List[UpdateCompetitorSitesJsonData]
    user_id: str

    class Config:
        from_attributes = True

    @validator("survey_date")
    def set_timezone_to_none(cls, value):
        # Explicitly set the timezone to None
        return value.replace(tzinfo=None)


class CompetitorSitesBySiteId(BaseModel):
    id: int
    kent_id: int
    brand_id: int
    brand: str
    address: str
    marketer_id: int
    municipality: str
    province_id: int
    province: str
    lat: float
    long: float
    restricted_dsl: str
    displayorder: int

    class Config:
        from_attributes = True