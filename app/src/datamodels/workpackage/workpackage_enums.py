from enum import Enum


class OriginEnum(Enum):
    nyc = "NYC"
    lax = "LAX"
    sfo = "SFO"


class CabinEnum(Enum):
    c = "Business"
    py = "Premium Economy"
    y = "Economy"


class OwRtEnum(Enum):
    ow = "OO"
    rt = "RT"


class CurrencyEnum(Enum):
    usd = "USD"


class BlankEnum(Enum):
    blank = ""


class SeasonEnum(Enum):
    l = "L"
    k = "K"
    k1 = "K1"
    k2 = "K2"
    h = "H"
    h1 = "H1"
    h2 = "H2"
    p = "P"
    o = "O"
