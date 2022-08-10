from src.farefiling.modules.utilities import gen_fare_basis


def test_business_class_roundtrip():
    check_expect = "JLUS"
    assert gen_fare_basis(rbd="J", season="L", weekday=None, ow=False) == check_expect


def test_business_class_oneway():
    check_expect = "JLOUS"
    assert gen_fare_basis(rbd="J", season="L", weekday=None, ow=True) == check_expect


def test_roundtrip_weekday():
    check_expect = "BLXUS"
    assert gen_fare_basis(rbd="B", season="L", weekday=True, ow=False) == check_expect


def test_roundtrip_weekend():
    check_expect = "BLWUS"
    assert gen_fare_basis(rbd="B", season="L", weekday=False, ow=False) == check_expect


def test_oneway_weekday():
    check_expect = "BLXOUS"
    assert gen_fare_basis(rbd="B", season="L", weekday=True, ow=True) == check_expect


def test_oneway_weekend():
    check_expect = "BLWOUS"
    assert gen_fare_basis(rbd="B", season="L", weekday=False, ow=True) == check_expect
