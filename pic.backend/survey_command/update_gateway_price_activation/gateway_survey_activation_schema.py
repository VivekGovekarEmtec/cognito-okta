from aws_lambda_powertools.utilities.parser import BaseModel, Field


class PriceActivation(BaseModel):
    status: int = Field(default=0)
    user_id: str = Field(default=' ')


class PriceActivationStatus(BaseModel):
    is_active: bool = Field(default=False)


class PriceActivationStatusDict(BaseModel):
    gateway_price_activation: PriceActivationStatus