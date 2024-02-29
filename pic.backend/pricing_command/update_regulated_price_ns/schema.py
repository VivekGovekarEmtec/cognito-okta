from aws_lambda_powertools.utilities.parser import BaseModel


class UpdateRegulatedPrice(BaseModel):
    authorization_number: int
    user_id: str

    class Config:
        from_attributes = True
