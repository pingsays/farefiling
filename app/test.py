import unittest
import app
from src.modules.utilities import (
    excel_loader,
    gen_fare_combinations,
    merge_dfs,
    gen_fare_basis,
    gen_fare_price,
)
from pydantic import BaseModel
import pandas as pd


class InputRow(BaseModel):
    sort: int
    dest: str
    booking_class: str
    season: str
    base_fare: int
    direct: str


class TestFareFiling(unittest.TestCase):
    def test_excel_loader(self):
        required_sheets = (
            "input",
            "cabin_mapping",
            "season_mapping",
            "fare_combination",
        )

        dfs = excel_loader(app.input_file)
        keys = tuple(dfs.keys())

        for sheet in required_sheets:
            msg = f"sheet '{sheet}' is missing from Excel workbook"
            with self.subTest(msg):
                self.assertIn(sheet, keys)

    #         _input = dfs['input']
    #         print(_input)
    #         input_dtypes = {
    #             'sort': 'Int64',
    #             'dest': 'string',
    #             'booking_class': 'string',
    #             'season': 'string',
    #             'base_fare': 'Int64',
    #             'direct': 'string'
    #         }
    #         _input = _input.astype(input_dtypes)
    #         print(_input.dtypes)

    #         cabin_mapping = dfs['cabin_mapping']
    #         season_mapping = dfs['season_mapping']
    #         fare_combination = dfs['fare_combination']
    #         # print(cabin_mapping)
    # #         # print(cabin_mapping.dtypes)

    #         # print(season_mapping)
    #         # print(season_mapping.dtypes)

    #         # print(fare_combination)
    #         # print(fare_combination.dtypes)

    #         # df = fare_combination.convert_dtypes()
    #         # print(df)
    #         # print(df.dtypes)

    def test_gen_fare_combinations(self):
        input_data = [
            {
                "sort": 1,
                "dest": "TPE",
                "booking_class": "V",
                "season": "L",
                "base_fare": 400,
                "direct": "",
            },
            {
                "sort": 2,
                "dest": "TPE",
                "booking_class": "E",
                "season": "K1",
                "base_fare": 1400,
                "direct": "",
            },
            {
                "sort": 3,
                "dest": "TPE",
                "booking_class": "J",
                "season": "H2",
                "base_fare": 2400,
                "direct": "",
            },
        ]

        check_expect = [
            {
                "sort": 1,
                "dest": "TPE",
                "booking_class": "V",
                "season": "L",
                "base_fare": 400,
                "direct": "",
                "cabin": "Economy",
                "rt_only": True,
                "no_weekday_weekend": False,
                "season_code": "L",
            },
            {
                "sort": 2,
                "dest": "TPE",
                "booking_class": "E",
                "season": "K1",
                "base_fare": 1400,
                "direct": "",
                "cabin": "Premium Economy",
                "rt_only": False,
                "no_weekday_weekend": False,
                "season_code": "K",
            },
            {
                "sort": 3,
                "dest": "TPE",
                "booking_class": "J",
                "season": "H2",
                "base_fare": 2400,
                "direct": "",
                "cabin": "Business",
                "rt_only": False,
                "no_weekday_weekend": True,
                "season_code": "H",
            },
        ]

        input_df = pd.DataFrame(input_data)

        excel_sheets = excel_loader(app.input_file)
        cabin_df = excel_sheets["cabin_mapping"]
        season_df = excel_sheets["season_mapping"]
        fare_combination_df = excel_sheets["fare_combination"]

        merged_df = merge_dfs(
            input_df=input_df,
            cabin_df=cabin_df,
            season_df=season_df,
        )
        merged_df.sort_values("sort", inplace=True)
        y = merged_df.to_dict(orient="records")

        df = gen_fare_combinations(merged_df, fare_combination_df)

        # self.assertEqual(y, check_expect)

    def test_gen_fare_basis(self):
        excel_sheets = excel_loader(app.input_file)
        cabin_df = excel_sheets["cabin_mapping"]
        cabin_df = cabin_df.set_index("booking_class")
        cabin_dict = cabin_df.to_dict(orient="index")
        # print(cabin_df)
        # print(cabin_dict)
        # print()
        # print(cabin_dict['E'])

        check_expect1 = "EPWUS"
        check_expect2 = "BKXUS"
        check_expect3 = "RLWOUS"
        check_expect4 = "JLUS"
        check_expect5 = "DPOUS"
        wrong_check_expect6 = "CLWUS"
        wrong_check_expect7 = "VLXOUS"

        test1 = {
            "rbd": "E",
            "season": "P",
            "weekday": False,
            "ow": False,
        }
        self.assertEqual(gen_fare_basis(**test1), check_expect1)

    def test_gen_fare_price(self):
        # roundtrip + weekday
        check_expect = 1000 * 1 + 0
        self.assertEqual(gen_fare_price(1000, 1, 0), check_expect)

        # roundtrip + weekend
        check_expect = 1000 * 1 + 80
        self.assertEqual(gen_fare_price(1000, 1, 80), check_expect)

        # oneway + weekday
        check_expect = 1000 * 0.65 + 0
        self.assertEqual(gen_fare_price(1000, 0.65, 0), check_expect)

        # oneway + weekend
        check_expect = 1000 * 0.65 + 40
        self.assertEqual(gen_fare_price(1000, 0.65, 40), check_expect)


if __name__ == "__main__":
    unittest.main()
