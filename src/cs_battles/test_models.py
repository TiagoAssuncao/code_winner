from codeschool.testing import *
from cs_battles.factories import *
from cs_battles.models import Battle, BattleResponse
from cs_core.factories import ProgrammingLanguageFactory
#  Fixtures
register(BattleFactory)
register(BattleResponseFactory)


@pytest.mark.django_db
def test_battle_creation():
    b = BattleFactory.create()
    assert b != None


