# ============== #
# import modules #
# ============== #
# import public packages
import pandas as pd
import logging
import toml

# import utility functions
from src.modules.utilities import (
    excel_loader,
    apply_dtype_mapping,
    merge_dfs,
    gen_fare_combinations,
    split_df,
    output_to_excel,
)

# import local files
from src.datamodels import datatype_mapping


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

    # apply dtypes to dataframes
    logger.info("Applying datatype mapping to Excel input dataframes..")
    dfs = apply_dtype_mapping(dfs, datatype_mapping.dtype_mapping)
    # logger.debug(f"{[print(df.dtypes) for df in dfs.values()]}")

    # merge input and some config to generate base df
    logger.info("Merging input, cabin_mapping, and season_mapping dfs..")
    base_df = merge_dfs(
        input_df=dfs["input"],
        cabin_df=dfs["cabin_mapping"],
        season_df=dfs["season_mapping"],
    )
    fare_combination_df = excel_sheets["fare_combination"]

    # generate all fare combinations
    logger.info("Generating fare combinations..")
    records = gen_fare_combinations(
        base_df=base_df, fare_combination_df=fare_combination_df
    )
    df = pd.DataFrame(data=records)

    # if need separate business class output
    cabin_dfs = dict()
    if config["app"]["separate_business_class_output"]:
        split_by = {"cabin": "Business"}
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

    output_dfs = dict()
    # loop though each cabin split (business vs non-business)
    for key, df in cabin_dfs.items():
        categories = list()
        season_dfs = list()

        # create a list of seasons
        seasons = df["season"].unique()
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

    if config["app"]["output_to_excel"]:
        logger.info(f"Writing output to Excel file(s)..")
        for key, data_list in output_dfs.items():
            output_file = config["output"][key]["output_file"]
            output_to_excel(filename=output_file, data_list=data_list)

    logger.info("Run complete! :)")


if __name__ == "__main__":
    main()
