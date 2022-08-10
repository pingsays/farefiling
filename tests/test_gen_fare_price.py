from src.farefiling.modules.utilities import gen_fare_price


def test_roundtrip_weekday():
    check_expect = 1000 * 1.0 + 0
    assert (
        gen_fare_price(base_fare=1000, ow_multiplier=1.0, weekend_surcharge=0)
        == check_expect
    )


def test_roundtrip_weekend():
    check_expect = 1000 * 1.0 + 80
    assert (
        gen_fare_price(base_fare=1000, ow_multiplier=1.0, weekend_surcharge=80)
        == check_expect
    )


def test_oneway_weekday():
    check_expect = 1000 * 0.65 + 0
    assert (
        gen_fare_price(base_fare=1000, ow_multiplier=0.65, weekend_surcharge=0)
        == check_expect
    )


def test_oneway_weekend():
    check_expect = 1000 * 0.65 + 40
    assert (
        gen_fare_price(base_fare=1000, ow_multiplier=0.65, weekend_surcharge=40)
        == check_expect
    )
