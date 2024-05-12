from gg_fare_proposal.models.base import BaseModel


class OutputRow(BaseModel):
    origin_city_code: str = "NYC"
    destination_city_code: str
    fare_class_code: str
    currency_code: str = "USD"
    fare_amount: int
    ow_rt: int
    routing_number: int


class Output(BaseModel):
    data: list[OutputRow]
