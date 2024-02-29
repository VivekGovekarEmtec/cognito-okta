from aws_lambda_powertools.utilities.parser import BaseModel
from datetime import datetime as date_time


class SiteProductPriceChangeUpdate(BaseModel):
    product_price_change_id: int
    site_id: int
    product_id: int
    is_request_now: int
    request_date: date_time
    request_prices: float
    autho_no: str
    comment: str
    kent_id: int
    hierarchy_header_id: int
    site_list: str
    over_write_notification_type_with: int
    user_id: str
    price_change_status: int

    class Config:
        from_attributes = True
