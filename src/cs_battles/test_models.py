from codeschool.tests import *
from codeschool.models import User
from codeschool.factories import UserFactory
from cs_battles.factories import *
from cs_battles.models import Battle, BattleResponse
from cs_core.models import ProgrammingLanguage
from django.utils import timezone
from cs_questions.models import CodingIoQuestion
from codeschool.factories import UserFactory

#  Fixtures
register(BattleFactory)
register(BattleResponseFactory)
register(UserFactory)

"""
@pytest.fixture
def user():
    user = User(password="1234",username="tester")
    #user.save()
    return user
@pytest.fixture
def question():
    question = CodingIoQuestion(iospec_source="Oi",depth=7,short_description="abcd",long_description="Faca um teste usando print para mostrar Oi",slug="abcdef",title="Test question",path="000100010000")
    return question

@pytest.fixture
def language():
    language = ProgrammingLanguage(ref="py",name="python2")
    return language

@pytest.fixture
def battle_response():
    return BattleResponse(
                        time_end=timezone.now(),
                        battle=battle(),
                        )
@pytest.fixture
def battle():
    return Battle(
                battle_owner=user(),
                question=question(),
                language=language(),
                )

"""

@pytest.fixture
def battle():
    battle = BattleFactory.create()
    return battle

@pytest.fixture
def battle_with_invitations():
    battle = BattleFactory.create()
    battle.invitations_user.add(UserFactory.create())
    battle.save()
    return battle
@pytest.fixture
def battle_deactived():
    battle = BattleFactory.create()
    b = BattleResponse(battle=battle,response=battle.question.get_response(user=battle.battle_owner))    
    b.save()
    battle.battle_winner = b
    battle.battles.add(battle.battle_winner)
    battle.save()
    return battle


@pytest.mark.django_db
def test_determine_winner():
    battle = battle_deactived()
    winner = battle.determine_winner()
    assert winner is battle.battle_owner

@pytest.mark.django_db
def test_not_active_battle():
    b = battle_deactived()
    assert b.is_active is False

@pytest.mark.django_db
def test_active_battle():
    b = battle_with_invitations()
    assert b.is_active is True

@pytest.mark.django_db
def test_battle_creation():
    b = BattleFactory.create()
    assert b is not None

"""@pytest.mark.django_db
def test_battle_response_creation():
    br = BattleResponseFactory.create()
    assert br is not None
    """
