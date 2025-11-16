from gg_fare_proposal.models.base import BaseModel


class CabinMapping(BaseModel):
    booking_class: str
    cabin: str
    rt_only: str


class CabinMappings(BaseModel):
    data: list[CabinMapping]
