import logging
import sys
from pathlib import Path

import pandas as pd
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy


def excel_loader(path: Path) -> DataFrame:
    df = pd.read_excel(io=path, sheet_name=None, keep_default_na=False)
    return df


# def excel_loader(
#     path: Path,
# ) -> dict[str, Union[CabinMappings, FareCombinations, SeasonMappings, Inputs]]:
#     df = pd.read_excel(io=path, sheet_name=None, keep_default_na=False)
#     cabin_mappings = CabinMappings.model_validate(
#         {"data": df["cabin_mapping"].to_dict(orient="records")}
#     )

#     season_mappings = SeasonMappings.model_validate(
#         {"data": df["season_mapping"].to_dict(orient="records")}
#     )

#     fare_combinations = FareCombinations.model_validate(
#         {"data": df["fare_combination"].to_dict(orient="records")}
#     )

#     inputs = Inputs.model_validate({"data": df["input"].to_dict(orient="records")})

#     data = {
#         "cabin_mappings": cabin_mappings,
#         "season_mappings": season_mappings,
#         "fare_combinations": fare_combinations,
#         "inputs": inputs,
#     }

#     return data


def merge_dfs(
    input: DataFrame,
    cabin_mapping: DataFrame,
    season_mapping: DataFrame,
) -> DataFrame:
    """
    Takes in the input DataFrame, the cabin mapping DataFrame, and season mapping DataFrame and join them together.
    """
    # set up logger with function name for more granular debugging
    logger = _setup_logger()

    df = input.merge(cabin_mapping, on="booking_class")
    df = df.merge(season_mapping, on="season")

    # reapply sorting as pandas merge will mess it up
    # df = df.sort_values(by=["sort"])
    logger.debug(df)

    return df


def gen_fare_basis(
    rbd: str, season: str, weekday: bool, ow: bool, country: str = "US"
) -> str:
    """
    Takes in all the components needed to generate the fare basis and returns it.
    """
    # set up logger with function name for more granular debugging
    logger = _setup_logger()

    if weekday is None:
        weekday_code = ""
    elif weekday:
        weekday_code = "X"
    else:
        weekday_code = "W"

    if ow:
        ow_code = "O"
    else:
        ow_code = ""

    fare_basis = f"{rbd}{season}{weekday_code}{ow_code}{country}"
    return fare_basis


def gen_fare_price(
    base_fare: int, ow_multiplier: float, weekend_surcharge: int
) -> float:
    """
    Takes in the base fare, oneway multiplier, and weekend surcharge and return the calculated fare.
    """
    # set up logger with function name for more granular debugging
    logger = _setup_logger()

    fare = base_fare * ow_multiplier + weekend_surcharge
    return fare


def gen_fare_combinations(base: DataFrame, fare_combination: DataFrame) -> DataFrame:
    base = base.copy()
    fare_combination = fare_combination.copy()

    base["key"] = 1
    fare_combination["key"] = 1

    df = pd.merge(base, fare_combination, on="key", suffixes=[None, "_fc"])
    df.drop("key", axis=1, inplace=True)
    return df


def split_df(df: DataFrame, split_by: dict[str, str]) -> DataFrameGroupBy:
    """
    Takes in a DataFrame and a dictionary of {column_name: value} and split the DataFrame into groups.
    """
    # set up logger with function name for more granular debugging
    # logger = logging.getLogger(f"app.{__name__}.{sys._getframe().f_code.co_name}")
    logger = _setup_logger()
    for col, value in split_by.items():
        logger.debug(f"{col=}")
        logger.debug(f"{value=}")

        df_grouped = df.groupby(df[col] == value)
    return df_grouped


def output_to_excel(excel_file: Path, data: dict[str, DataFrame]) -> None:
    """
    Write each DataFrame into its own sheet of the Excel workbook.
    """
    # set up logger with function name for more granular debugging
    logger = _setup_logger()
    with pd.ExcelWriter(excel_file, engine="openpyxl", mode="w") as writer:
        for season, df in data.items():
            df.to_excel(writer, sheet_name=season, index=False)


def _setup_logger():
    """
    Function to create a logger with the function's name for more granular logging.
    """
    # set up logger with function name for more granular debugging
    # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch14s08.html
    return logging.getLogger(f"app.{__name__}.{sys._getframe(1).f_code.co_name}")
