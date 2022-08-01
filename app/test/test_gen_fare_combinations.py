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

    # base_df_data = {
    #     "sort": [1, 2, 3],
    #     "dest": ["TPE", "TPE", "TPE"],
    #     "booking_class": ["J", "W", "V"],
    #     "season": ["L", "L", "L"],
    #     "base_fare": [8000, 4000, 2000],
    #     "direct": ["", "", ""],
    #     "cabin": ["Business", "Premium Economy", "Economy"],
    #     "rt_only": [False, False, True],
    #     "no_weekday_weekend": [True, False, False],
    #     "season_code": ["L", "L", "L"],
    # }
    base_df_data = {
        "sort": [1],
        "dest": ["TPE"],
        "booking_class": ["J"],
        "season": ["L"],
        "base_fare": [8000],
        "direct": [""],
        "cabin": ["Business"],
        "rt_only": [False],
        "no_weekday_weekend": [True],
        "season_code": ["L"],
    }
    base_df = pd.DataFrame(base_df_data)
    print(base_df)

    df = gen_fare_combinations(base_df, fare_combination_df)
    print(df)


def test_roundtrip_weekday():
    pass
