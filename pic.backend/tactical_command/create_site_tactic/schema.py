from aws_lambda_powertools.utilities.parser import BaseModel, Field


class SiteTacticInsert(BaseModel):
    site_id: int
    follow_action_id: int
    follow_movement_id: int
    movement_option_id: int
    cpl_tolerance: float
    rack_fwd_tolerance: float
    follow_options: str
    last_updated_user_id: str
    comments: str
    start_time: str
    end_time: str
    follow_sites: str = Field(default=None)


    class Config:
        from_attributes = True
