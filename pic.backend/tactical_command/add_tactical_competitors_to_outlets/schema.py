from typing import List
from aws_lambda_powertools.utilities.parser import BaseModel


class CompetitorDetail(BaseModel):
    kent_id: int

    class Config:
        from_attributes = True


class TacticalCompetitorDetail(BaseModel):
    competitors: List[CompetitorDetail]
    site_id: int

    class Config:
        from_attributes = True


class AddTacticCompetitorsForOutlets(BaseModel):
    json_data: TacticalCompetitorDetail
    user_id: str

    class Config:
        from_attributes = True