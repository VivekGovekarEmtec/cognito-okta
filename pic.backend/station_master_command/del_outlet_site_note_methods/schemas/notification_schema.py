from aws_lambda_powertools.utilities.parser import BaseModel, Field

class SiteNotification(BaseModel):
    id: int = Field(default=None)
    site_id: int = Field(default=None)
    notification_id: int = Field(default=None)
    status_id: int = Field(default=None)
    email: str = Field(max_length=500)
    user_name: str = Field(max_length=200)
    user_id: str = Field(default=None)

    class Config:
        from_attributes = True

