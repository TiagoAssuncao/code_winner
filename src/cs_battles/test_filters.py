from codeschool.tests import *
from django.utils import timezone
from cs_battles import filters

@pytest.fixture
def timezone_date(year=2016,day=15,minute=30):
    return timezone.datetime(
        year=year,
        month=6,
        day=day,
        minute=minute,
        hour=12
    )

@pytest.fixture
def date_delta_time():
    first = timezone_date()
    last = timezone_date(year=2017,day=17,minute=55)
    return last-first


def test_date_format_short():
    date = timezone_date()
    assert "15/06/16" == filters.date_format(date,"short")

def test_date_format_long():
    date = timezone_date()
    assert "15/06/16 12:30" == filters.date_format(date,"long")

def test_deltatime_format():
    delta_time = date_delta_time()
    assert "1 anos, 2 dias, 00:25:00:0000" == filters.delta_time(delta_time)

