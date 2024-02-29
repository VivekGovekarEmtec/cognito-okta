from aws_lambda_powertools.utilities.parser import BaseModel, Field

class UpdateCompetitor(BaseModel):
    id: int
    kent_id: int
    brand_id: int
    address: str = Field(..., max_length=100)
    muni_name: str = Field(..., max_length=100)
    lat: float
    long: float
    marketer_id: int
    province_id: int
    restricted_dsl: str
    last_user_id: str
    lsd_sign: int
    site_rating: int
    ml: float
    gas_buddy: str
    wd_open: str
    wd_close: str
    status_code: int
    language: str

    class Config:
        from_attributes = True