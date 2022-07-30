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


# ============================== #
# define global variables/config #
# ============================== #
input_file = r"gg_fare_filing.xlsx"
output_file = r"output.xlsx"
config_sheets = {"input", "cabin_mapping", "season_mapping", "fare_combination"}


# ======== #
#   main   #
# ======== #
def main():
    # import Excel
    logger.info("Importing Excel input file..")
    excel_sheets = excel_loader(input_file)

    # filter for config sheets only
    dfs = dict()
    for key, df in excel_sheets.items():
        if key in config_sheets:
            dfs[key] = df

    # apply dtypes to dataframes
    logger.info("Applying datatype mapping to Excel input dataframes..")
    dfs = apply_dtype_mapping(dfs, datatype_mapping.dtype_mapping)
    logger.debug(f"{[print(df.dtypes) for df in dfs.values()]}")

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

    # create new dataframe of output for further processing
    logger.info("Creating new dataframe for further processing..")
    df = pd.DataFrame(data=records)

    # split dataframe by seasonality
    logger.info("Splitting dataframe by seasonality..")
    seasons = df["season"].unique()
    split_by = {"season": seasons}
    output_dfs = split_df(df, split_by=split_by)

    logger.info(f"Writing output to Excel file [{output_file}]..")
    try:
        output_to_excel(dfs=output_dfs, filename=output_file)
    except Exception as e:
        logger.error(e)
        raise e

    logger.info("Run complete! :)")


if __name__ == "__main__":
    main()
