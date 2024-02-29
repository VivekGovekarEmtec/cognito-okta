from aws_lambda_powertools.utilities.parser import BaseModel


class MarkReview(BaseModel):
    site_id: int
    user_id: str
