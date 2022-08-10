# ============== #
# import modules #
# ============== #
# import public packages
import pandas as pd
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy
import logging
import sys

# import data models
from ..datamodels.workpackage.workpackage import WorkPackageRecord


# ============= #
# set up logger #
# ============= #
logger = logging.getLogger(f"app.{__name__}")


# ========= #
# functions #
# ========= #
def excel_loader(excel_file: str) -> dict[str, DataFrame]:
    """
    Takes in an Excel file and load all sheets into a dictionary of DataFrames.
    """
    # set up logger with function name for more granular debugging
    logger = _setup_logger()

    dfs = pd.read_excel(excel_file, sheet_name=None)
    return dfs


def apply_dtype_mapping(
    dfs: dict[str, DataFrame], mapping: dict[str, dict]
) -> dict[str, DataFrame]:
    """
    Takes in the dictionary of DataFrames and a dictionary of data type mapping and change the dtypes of each DataFrame.
    """
    # set up logger with function name for more granular debugging
    logger = _setup_logger()

    for sheet_name, dtypes in mapping.items():
        dfs[sheet_name] = dfs[sheet_name].astype(dtypes)
    return dfs


def merge_dfs(
    input_df: DataFrame, cabin_df: DataFrame, season_df: DataFrame
) -> DataFrame:
    """
    Takes in the input DataFrame, the cabin mapping DataFrame, and season mapping DataFrame and join them together.
    """
    # set up logger with function name for more granular debugging
    logger = _setup_logger()

    df = input_df.merge(cabin_df, on="booking_class")
    df = df.merge(season_df, on="season")

    # reapply sorting as pandas merge will mess it up
    df = df.sort_values(by=["sort"])
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


def gen_fare_combinations(
    base_df: DataFrame, fare_combination_df: DataFrame
) -> DataFrame:
    """
    Takes in the base DataFrame and fare combination DataFrame and generate all the different possible fare combinations.
    """
    # set up logger with function name for more granular debugging
    logger = _setup_logger()

    records = list()

    # loop though each row (input) of base df
    for _, base_row in base_df.iterrows():

        # unpack base_row data into variables
        (
            _,
            dest,
            booking_class,
            season,
            base_fare,
            _,
            cabin,
            rt_only,
            no_weekday_weekend,
            season_code,
        ) = base_row.to_list()

        # loop through each row (fare combination) of fare combination df
        for _, combination_row in fare_combination_df.iterrows():

            # unpack combination_row data into variables
            (
                weekday,
                ow,
                ow_multiplier,
                weekend_surcharge,
                ow_mapping,
            ) = combination_row.to_list()

            # if input rbd allows for rt fares only, then skip ow fare combination
            if rt_only and ow:
                continue

            # if input rbd has no weekday/weekend distinction, then skip weekend fare combination
            if no_weekday_weekend and not weekday:
                continue

            # for input rbd w/o weekday/weekend distinction, leave farebasis blank for weekday/weekend
            if no_weekday_weekend:
                weekday = None

            # generate fare basis
            fare_basis = gen_fare_basis(
                rbd=booking_class, season=season_code, weekday=weekday, ow=ow
            )

            # generate fare price
            fare_price = gen_fare_price(
                base_fare=base_fare,
                ow_multiplier=ow_multiplier,
                weekend_surcharge=weekend_surcharge,
            )

            # create WorkPackageRecord
            record = WorkPackageRecord(
                destination=dest,
                fare_basis=fare_basis,
                booking_class=booking_class,
                cabin=cabin,
                ow_rt=ow_mapping,
                fare_price=fare_price,
                season=season,
                season_code=season_code,
            )
            records.append(record.dict())

    df = pd.DataFrame(data=records)
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


def output_to_excel(filename: str, data_list: list[dict[str, DataFrame]]) -> None:
    """
    Write each DataFrame into its own sheet of the Excel workbook.
    """
    # set up logger with function name for more granular debugging
    logger = _setup_logger()
    with pd.ExcelWriter(filename, engine="openpyxl", mode="w") as writer:
        for data in data_list:
            for season, df in data.items():
                df.to_excel(writer, sheet_name=season, index=False)


def _setup_logger():
    """
    Function to create a logger with the function's name for more granular logging.
    """
    # set up logger with function name for more granular debugging
    # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch14s08.html
    return logging.getLogger(f"app.{__name__}.{sys._getframe(1).f_code.co_name}")
