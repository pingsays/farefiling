from gg_fare_proposal.models.base import BaseModel


class Input(BaseModel):
    dest: str
    booking_class: str
    season: str
    base_fare: int
    direct: str


class Inputs(BaseModel):
    data: list[Input]
