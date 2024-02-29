from typing import List
from aws_lambda_powertools.utilities.parser import BaseModel

class AttachCompetitorAssociationDataList(BaseModel):
    kent_id: int

    class Config:
        from_attributes = True

class AttachCompetitorsAssociation(BaseModel):
    competitors: List[AttachCompetitorAssociationDataList]
    site_id: int

    class Config:
        from_attributes = True

class AttachCompetitorsAssociationList(BaseModel):
    json_data: AttachCompetitorsAssociation
    user_id: str

    class Config:
        from_attributes = True