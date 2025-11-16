from pathlib import Path

import pandas as pd

from gg_fare_proposal.helper import excel_loader
from gg_fare_proposal.models.cabin_mapping import CabinMappings
from gg_fare_proposal.models.fare_combination import FareCombinations
from gg_fare_proposal.models.input import Inputs
from gg_fare_proposal.models.season_mapping import SeasonMappings

# def test_excel_loader():
#     path = Path("gg_fare_proposal.xlsx")
#     df = excel_loader(path=path)
#     cabin_mappings = CabinMappings.model_validate(
#         {"data": df["cabin_mapping"].to_dict(orient="records")}
#     )
#     print(cabin_mappings.json())

#     season_mappings = SeasonMappings.model_validate(
#         {"data": df["season_mapping"].to_dict(orient="records")}
#     )
#     print(season_mappings.json())

#     fare_combinations = FareCombinations.model_validate(
#         {"data": df["fare_combination"].to_dict(orient="records")}
#     )
#     print(fare_combinations.json())

#     inputs = Inputs.model_validate({"data": df["input"].to_dict(orient="records")})
#     print(inputs.json())
