from ast import Or
from pydantic import BaseModel, validator
from .workpackage_enums import (
    OriginEnum,
    CabinEnum,
    OwRtEnum,
    CurrencyEnum,
    BlankEnum,
    SeasonEnum,
)


class WorkPackageRecord(BaseModel):
    origin: OriginEnum = OriginEnum.nyc
    destination: str
    fare_basis: str
    booking_class: str
    cabin: CabinEnum
    ow_rt: OwRtEnum
    blank1: BlankEnum = BlankEnum.blank
    blank2: BlankEnum = BlankEnum.blank
    blank3: BlankEnum = BlankEnum.blank
    currency: CurrencyEnum = CurrencyEnum.usd
    fare_price: float
    season: SeasonEnum
    season_code: SeasonEnum

    class Config:
        use_enum_values = True

    @validator("booking_class")
    def booking_class_must_have_len_one(cls, value):
        if len(value) != 1:
            raise ValueError("booking_class must have length of 1")
        return value

    @validator("booking_class")
    def booking_class_must_be_alphabetic(cls, value):
        assert value.isalpha(), "booking_class must be alphabetic"
        return value
