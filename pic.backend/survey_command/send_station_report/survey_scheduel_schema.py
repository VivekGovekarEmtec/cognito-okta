from aws_lambda_powertools.utilities.parser import BaseModel, Field, validator
from datetime import datetime
from typing import List


class HierarchyBySiteId(BaseModel):
    id: int
    lang_desc: str
    hierarchy_type_id: int
    lang_id: int
    is_default: int

    class Config:
        from_attributes = True


class SendStationReportTemplate(BaseModel):
    outlet_id: int
    status: bool
    to: str
    message: str

    class Config:
        from_attributes = True


class StationReportList(BaseModel):
    request_date: datetime = Field(default=None)
    include_rows: bool
    language: str
    user_id: str
    station_report_list: List[SendStationReportTemplate]

    @validator("request_date")
    def set_timezone_to_none(cls, value):
        # Explicitly set the timezone to None
        return value.replace(tzinfo=None)

    class Config:
        from_attributes = True


class StationReportListResponse(BaseModel):
    success_site_id_list: List[int]
    error_site_id_list: List[int]
