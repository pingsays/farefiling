from pathlib import Path

import numpy as np
import pandas as pd

from farefiling.helper import (
    excel_loader,
    gen_fare_combinations,
    merge_dfs,
    output_to_excel,
)

pd.set_option("display.max_columns", None)

INPUT_FILE = Path("gg_fare_proposal.xlsx")
OUTPUT_FILE = Path("gg_output.xlsx")


def main():
    dfs = excel_loader(path=INPUT_FILE)

    df_input = dfs["input"]
    df_cabin_mapping = dfs["cabin_mapping"]
    df_season_mapping = dfs["season_mapping"]
    df_fare_combination = dfs["fare_combination"]
    df_routing_number = dfs["routing_number"]

    # add metadata to input dataframe
    df_base = merge_dfs(
        input=df_input,
        cabin_mapping=df_cabin_mapping,
        season_mapping=df_season_mapping,
    )

    # generate business class fare combinations (no weekend - 2 types)
    df_business = df_base[df_base["cabin"] == "Business"]
    df_business_fare_combination = df_fare_combination[
        df_fare_combination["weekend"] == "X"
    ]
    df_business = gen_fare_combinations(
        base=df_business, fare_combination=df_business_fare_combination
    )
    print(df_business)

    # generate non business class fare combinations (all 4 types)
    df_non_business = df_base[df_base["cabin"] != "Business"]
    df_non_business = gen_fare_combinations(
        base=df_non_business, fare_combination=df_fare_combination
    )

    # merge business and non-business back together
    df_merged = pd.concat([df_business, df_non_business])

    # add routing number
    df_merged = df_merged.merge(df_routing_number, on="dest", how="left")
    df_merged = df_merged.sort_values(by=["sort", "sort_fc"])

    # calculate fare amount
    df_merged["fare_amount"] = (
        (df_merged["base_fare"] * df_merged["oneway_multiplier"])
        + df_merged["weekend_surcharge"]
        # .round()
    )

    # generate fare basis
    business_class_rbds = df_business["booking_class"].values
    df_merged["fare_basis"] = (
        df_merged["booking_class"]
        + df_merged["season_code"]
        + np.where(
            df_merged["booking_class"].isin(business_class_rbds),
            "",
            df_merged["weekend"],
        )
        + df_merged["oneway"]
        + "US"
    )

    # adding hardcoded values
    df_merged["origin"] = "NYC"
    df_merged["currency"] = "USD"

    columns_to_select = [
        "origin",
        "dest",
        "fare_basis",
        "currency",
        "fare_amount",
        "oneway_mapping",
        "routing_number",
        "season",
    ]
    output = df_merged[columns_to_select]

    grouped = output.groupby(output["season"])
    group_dfs = {name: group for name, group in grouped}

    output_to_excel(excel_file=OUTPUT_FILE, data=group_dfs)


if __name__ == "__main__":
    main()
