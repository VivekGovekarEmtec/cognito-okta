from aws_lambda_powertools.utilities.parser import BaseModel


class UpdateTacticFollowActionStatus(BaseModel):
    site_id: int
    follow_action_id: int
    status_id: int

    class Config:
        from_attributes = True