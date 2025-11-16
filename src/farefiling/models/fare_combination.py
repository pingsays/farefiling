from gg_fare_proposal.models.base import BaseModel


class FareCombination(BaseModel):
    weekend: str
    oneway_multiplier: float
    weekend_surcharge: int
    oneway: str
    oneway_mapping: int


class FareCombinations(BaseModel):
    data: list[FareCombination]
