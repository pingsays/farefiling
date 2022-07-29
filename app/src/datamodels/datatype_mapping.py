dtype_mapping = {
    "input": {
        "sort": "Int64",
        "dest": "string",
        "booking_class": "string",
        "season": "string",
        "base_fare": "Int64",
        "direct": "string",
    },
    "cabin_mapping": {
        "booking_class": "string",
        "cabin": "string",
        "rt_only": "bool",
        "no_weekday_weekend": "bool",
    },
    "season_mapping": {
        "season": "string",
        "season_code": "string",
    },
    "fare_combination": {
        "weekday": "bool",
        "oneway_multiplier": "Float64",
        "weekend_surcharge": "Int64",
        "oneway": "bool",
        "oneway_mapping": "string",
    },
}
