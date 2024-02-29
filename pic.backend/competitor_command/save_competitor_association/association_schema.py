from typing import List
from aws_lambda_powertools.utilities.parser import BaseModel

class SaveCompetitorAssociationDataList(BaseModel):
    kent_id: int
    m_id: int
    device_type_id: int
    order_no: int

    class Config:
        from_attributes = True


class SaveCompetitorsAssociation(BaseModel):
    outlet_id: int
    json_data: List[SaveCompetitorAssociationDataList]
    push_to_pos: int
    user_id: str

    class Config:
        from_attributes = True


