from typing import List
from aws_lambda_powertools.utilities.parser import BaseModel


class CompetitorDetailList(BaseModel):
    kent_id: int
    reg_auto_clear_adjustment: float
    dsl_auto_clear_adjustment: float
    observe_type_id: int

    class Config:
        from_attributes = True


class UpdateTacticCompetitorsForOutlets(BaseModel):
    site_id: int
    user_id: str
    comp_list_json: List[CompetitorDetailList]

    class Config:
        from_attributes = True
