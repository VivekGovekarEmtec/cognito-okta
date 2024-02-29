from aws_lambda_powertools.utilities.parser import BaseModel, Field
from typing import Optional

class Contact(BaseModel):
    id: Optional[int] = None
    site_id: Optional[int] = None
    contact_type_id: Optional[int] = None
    type_id: Optional[int] = None
    value: str
    user_id: str
    class Config:
        from_attributes = True