import pandas as pd
from pandas import DataFrame
from ..datamodels.workpackage.workpackage import WorkPackageRecord


def excel_loader(excel_file: str) -> dict[str, DataFrame]:
    dfs = pd.read_excel(excel_file, sheet_name=None)
    return dfs


def apply_dtype_mapping(
    dfs: dict[str, DataFrame], mapping: dict[str, dict]
) -> dict[str, DataFrame]:
    for sheet_name, dtypes in mapping.items():
        dfs[sheet_name] = dfs[sheet_name].astype(dtypes)
    return dfs


def merge_dfs(
    input_df: DataFrame, cabin_df: DataFrame, season_df: DataFrame
) -> DataFrame:
    df = input_df.merge(cabin_df, on="booking_class")
    df = df.merge(season_df, on="season")
    return df


def gen_fare_basis(
    rbd: str, season: str, weekday: bool, ow: bool, country: str = "US"
) -> str:
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
    fare = base_fare * ow_multiplier + weekend_surcharge
    return fare


def gen_fare_combinations(
    base_df: DataFrame, fare_combination_df: DataFrame
) -> DataFrame:

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
                ow_multiplier,
                weekend_surcharge,
                ow,
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

    return records


def split_df(df: DataFrame, split_by: dict[str, list]) -> dict:
    dfs = {}
    for col, values in split_by.items():
        for value in values:
            s = df[df[col] == value]
            s = s.drop(columns=["season", "season_code"])
            s = s.reset_index(drop=True)
            dfs[value] = s

    return dfs


def output_to_excel(dfs: dict[str, DataFrame], filename) -> None:
    with pd.ExcelWriter(filename, engine="openpyxl", mode="w") as writer:
        for season, df in dfs.items():
            df.to_excel(writer, sheet_name=season, index=False)
