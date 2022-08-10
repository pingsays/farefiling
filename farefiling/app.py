# ============== #
# import modules #
# ============== #
# import public packages
import pandas as pd
import logging
import toml

# import utility functions
from modules.utilities import (
    excel_loader,
    apply_dtype_mapping,
    merge_dfs,
    gen_fare_combinations,
    split_df,
    output_to_excel,
)

# import local files
from datamodels import datatype_mapping


# ======================= #
# load application config #
# ======================= #
config = toml.load(r"./config.toml")


# ============= #
# set up logger #
# ============= #
logger = logging.getLogger("app")
logger.setLevel(config["logger"]["level"].upper())

# create handler
handler = logging.StreamHandler()

# create log format
fmt = "[{levelname}] {asctime} [{name}] {message}"
formatter = logging.Formatter(fmt=fmt, style="{")

# add formatter to handler
handler.setFormatter(formatter)

# add handler to logger
logger.addHandler(handler)


# ======== #
#   main   #
# ======== #
def main():

    # import Excel
    logger.info("Importing Excel input file..")
    excel_sheets = excel_loader(config["input"]["input_file"])

    # filter for config sheets only
    dfs = dict()
    for key, df in excel_sheets.items():
        if key in config["input"]["input_sheets"]:
            dfs[key] = df

    # choose excel or toml config
    if config["app"]["use_excel_config"]:
        excel_config = dfs["config"]
        separate_business_output = excel_config["separate_business_output"].values
    else:
        separate_business_output = config["app"]["separate_business_class_output"]

    # apply dtypes to dataframes
    logger.info("Applying datatype mapping to Excel input dataframes..")
    dfs = apply_dtype_mapping(dfs, datatype_mapping.dtype_mapping)
    # logger.debug(f"{[print(df.dtypes) for df in dfs.values()]}")
    # logger.debug(dfs)

    # merge input and some config to generate base df
    logger.info("Merging input, cabin_mapping, and season_mapping dfs..")
    base_df = merge_dfs(
        input_df=dfs["input"],
        cabin_df=dfs["cabin_mapping"],
        season_df=dfs["season_mapping"],
    )
    fare_combination_df = excel_sheets["fare_combination"]
    # logger.debug(f"{base_df=}")
    # logger.debug(f"{fare_combination_df=}")

    # generate all fare combinations
    logger.info("Generating fare combinations..")
    df = gen_fare_combinations(base_df=base_df, fare_combination_df=fare_combination_df)
    logger.debug(df)

    # if need separate business class output
    cabin_dfs = dict()
    if separate_business_output:
        split_by = {"cabin": "Business"}

        logger.info("Splitting DataFrame by Business Class vs Non-Business Class..")
        df_grouped = split_df(df=df, split_by=split_by)
        groups = list(df_grouped.groups.keys())

        # store business class fares
        if True in groups:
            cabin_dfs["business"] = df_grouped.get_group(True)

        # store non-business class fares
        if False in groups:
            cabin_dfs["non-business"] = df_grouped.get_group(False)
    else:
        # if not separating business class, store everything in one category
        cabin_dfs["all"] = df

    # loop though each cabin split (business and non-business)
    logger.info("Splitting DataFrame by Seasonality..")
    output_dfs = dict()
    for key, df in cabin_dfs.items():
        categories = list()
        season_dfs = list()

        # create a list of seasons
        seasons = df["season"].unique()

        logger.info(f"List of seasons in [{key}] fares: {seasons}")
        [categories.append({"season": season}) for season in seasons]
        logger.debug(f"{key} categories: {categories}")

        # loop through each category (season)
        for category in categories:
            # set season as category_name
            category_name = list(category.values())[0]

            # perform split on df
            df_grouped = split_df(df, split_by=category)
            groups = list(df_grouped.groups.keys())

            # save True group to season_dfs
            s = df_grouped.get_group(True)
            s = s.drop(columns=["season", "season_code"])
            season_dfs.append({category_name: s})

            if False not in groups:
                break

        output_dfs[key] = season_dfs
        # logger.debug(output_dfs)

    if config["app"]["output_to_excel"]:
        for key, data_list in output_dfs.items():
            output_file = config["output"][key]["output_file"]
            logger.info(f"Writing output to Excel file [{output_file}]..")
            output_to_excel(filename=output_file, data_list=data_list)

    logger.info("Run complete! :) xoxo <3")


if __name__ == "__main__":
    main()
