from src.modules.utilities import gen_fare_combinations
import pandas as pd


fare_combination_data = [
    {
        "weekday": True,
        "oneway": False,
        "oneway_multiplier": 1.0,
        "weekend_surcharge": 0,
        "oneway_mapping": "RT",
    },
    {
        "weekday": False,
        "oneway": False,
        "oneway_multiplier": 1.0,
        "weekend_surcharge": 80,
        "oneway_mapping": "RT",
    },
    {
        "weekday": True,
        "oneway": True,
        "oneway_multiplier": 0.65,
        "weekend_surcharge": 0,
        "oneway_mapping": "OO",
    },
    {
        "weekday": False,
        "oneway": True,
        "oneway_multiplier": 0.65,
        "weekend_surcharge": 40,
        "oneway_mapping": "OO",
    },
]
fare_combination_df = pd.DataFrame(fare_combination_data)


def test_default():
    """
    Default has no restrictions on Roundtrip/Oneway and Weekend/Weekday. Should have 4 fare combinations.
    """
    import pprint

    pp = pprint.PrettyPrinter(indent=2, compact=True)

    check_expect = [
        {
            "origin": "NYC",
            "destination": "TPE",
            "fare_basis": "WHXUS",
            "booking_class": "W",
            "cabin": "Premium Economy",
            "ow_rt": "RT",
            "blank1": "",
            "blank2": "",
            "blank3": "",
            "currency": "USD",
            "fare_price": 5000.0,
            "season": "H1",
            "season_code": "H",
        },
        {
            "origin": "NYC",
            "destination": "TPE",
            "fare_basis": "WHWUS",
            "booking_class": "W",
            "cabin": "Premium Economy",
            "ow_rt": "RT",
            "blank1": "",
            "blank2": "",
            "blank3": "",
            "currency": "USD",
            "fare_price": (5000.0 + 80),
            "season": "H1",
            "season_code": "H",
        },
        {
            "origin": "NYC",
            "destination": "TPE",
            "fare_basis": "WHXOUS",
            "booking_class": "W",
            "cabin": "Premium Economy",
            "ow_rt": "OO",
            "blank1": "",
            "blank2": "",
            "blank3": "",
            "currency": "USD",
            "fare_price": (5000.0 * 0.65),
            "season": "H1",
            "season_code": "H",
        },
        {
            "origin": "NYC",
            "destination": "TPE",
            "fare_basis": "WHWOUS",
            "booking_class": "W",
            "cabin": "Premium Economy",
            "ow_rt": "OO",
            "blank1": "",
            "blank2": "",
            "blank3": "",
            "currency": "USD",
            "fare_price": (5000.0 * 0.65 + 40),
            "season": "H1",
            "season_code": "H",
        },
    ]

    base_df_data = {
        "sort": [1],
        "dest": ["TPE"],
        "booking_class": ["W"],
        "season": ["H1"],
        "base_fare": [5000],
        "direct": [""],
        "cabin": ["Premium Economy"],
        "rt_only": [False],
        "no_weekday_weekend": [False],
        "season_code": ["H"],
    }
    base_df = pd.DataFrame(base_df_data)

    df = gen_fare_combinations(base_df, fare_combination_df)
    df = df.to_dict(orient="records")

    assert df == check_expect


def test_roundtrip_only():
    """
    Restrictions on Roundtrip fares only. Should have 2 fare combinations of 1) Roundtrip + Weekday, 2) Roundtrip + Weekend
    """
    check_expect = [
        {
            "origin": "NYC",
            "destination": "TPE",
            "fare_basis": "VLXUS",
            "booking_class": "V",
            "cabin": "Economy",
            "ow_rt": "RT",
            "blank1": "",
            "blank2": "",
            "blank3": "",
            "currency": "USD",
            "fare_price": 1500.0,
            "season": "L",
            "season_code": "L",
        },
        {
            "origin": "NYC",
            "destination": "TPE",
            "fare_basis": "VLWUS",
            "booking_class": "V",
            "cabin": "Economy",
            "ow_rt": "RT",
            "blank1": "",
            "blank2": "",
            "blank3": "",
            "currency": "USD",
            "fare_price": 1580.0,
            "season": "L",
            "season_code": "L",
        },
    ]

    base_df_data = {
        "sort": [1],
        "dest": ["TPE"],
        "booking_class": ["V"],
        "season": ["L"],
        "base_fare": [1500],
        "direct": [""],
        "cabin": ["Economy"],
        "rt_only": [True],
        "no_weekday_weekend": [False],
        "season_code": ["L"],
    }
    base_df = pd.DataFrame(base_df_data)

    df = gen_fare_combinations(base_df, fare_combination_df)
    df = df.to_dict(orient="records")

    assert df == check_expect


def test_no_weekend_fare_types():
    """
    No Weekend/Weekday fare types. Should have 2 fare combinations of 1) Roundtrip, 2) Oneway. Weekend/Weekday fare basis slot should be blank.
    """
    check_expect = [
        {
            "origin": "NYC",
            "destination": "TPE",
            "fare_basis": "JKUS",
            "booking_class": "J",
            "cabin": "Business",
            "ow_rt": "RT",
            "blank1": "",
            "blank2": "",
            "blank3": "",
            "currency": "USD",
            "fare_price": 8000.0,
            "season": "K1",
            "season_code": "K",
        },
        {
            "origin": "NYC",
            "destination": "TPE",
            "fare_basis": "JKOUS",
            "booking_class": "J",
            "cabin": "Business",
            "ow_rt": "OO",
            "blank1": "",
            "blank2": "",
            "blank3": "",
            "currency": "USD",
            "fare_price": (8000.0 * 0.65),
            "season": "K1",
            "season_code": "K",
        },
    ]

    base_df_data = {
        "sort": [1],
        "dest": ["TPE"],
        "booking_class": ["J"],
        "season": ["K1"],
        "base_fare": [8000],
        "direct": [""],
        "cabin": ["Business"],
        "rt_only": [False],
        "no_weekday_weekend": [True],
        "season_code": ["K"],
    }
    base_df = pd.DataFrame(base_df_data)

    df = gen_fare_combinations(base_df, fare_combination_df)
    df = df.to_dict(orient="records")

    assert df == check_expect


def test_roundtrip_only_and_no_weekend_fare_types():
    """
    Roundtrip only and no Weekend/Weekday fare types. Should have 1 fare combination of 1) Roundtrip. Weekend/Weekday fare basis slot should be blank.
    """
    check_expect = [
        {
            "origin": "NYC",
            "destination": "TPE",
            "fare_basis": "GPUS",
            "booking_class": "G",
            "cabin": "Business",
            "ow_rt": "RT",
            "blank1": "",
            "blank2": "",
            "blank3": "",
            "currency": "USD",
            "fare_price": 1_000_000.0,
            "season": "P",
            "season_code": "P",
        },
    ]

    base_df_data = {
        "sort": [1],
        "dest": ["TPE"],
        "booking_class": ["G"],
        "season": ["P"],
        "base_fare": [1_000_000],
        "direct": [""],
        "cabin": ["Business"],
        "rt_only": [True],
        "no_weekday_weekend": [True],
        "season_code": ["P"],
    }
    base_df = pd.DataFrame(base_df_data)

    df = gen_fare_combinations(base_df, fare_combination_df)
    df = df.to_dict(orient="records")

    assert df == check_expect
