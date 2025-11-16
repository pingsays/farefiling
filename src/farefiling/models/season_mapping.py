from gg_fare_proposal.models.base import BaseModel


class SeasonMapping(BaseModel):
    season: str
    season_code: str


class SeasonMappings(BaseModel):
    data: list[SeasonMapping]
