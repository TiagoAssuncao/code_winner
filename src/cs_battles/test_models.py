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
def source_code(aditional=""):
    return "print('Oi');"+aditional

@pytest.fixture
def battle_fixture():
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
    battle = battle_fixture()
    b = BattleResponseFactory.create()
    battle.battle_winner = b
    battle.battles.add(battle.battle_winner)
    battle.save()
    return battle
@pytest.fixture
def battle_response_fix(battle):
    battle_response = BattleResponseFactory.create()
    battle_response.battle = battle
    battle_response.save()
    return battle_response

@pytest.fixture
def battle_without_winner():
    battle = battle_fixture()
    battle_response = battle_response_fix(battle)
    battle_response2 = battle_response_fix(battle)
    ri = register_item(battle_response,source_code())
    battle_response.update(ri)

    ri = register_item(battle_response2,source_code("a=1+1;"))
    battle_response2.update(ri)

    return battle
@pytest.fixture
def register_item(battle_response,source):
    response_item = battle_response.response.activity. \
        register_response_item(
            source=source,
            user=battle_response.response.user,
            context=battle_response.battle.battle_context,
            language=battle_response.battle.language,
        )
    response_item.autograde()
    return response_item

# Begin of tests

# TESTs to Battle
@pytest.mark.django_db
def test_determine_winner():
    battle = battle_without_winner()
    winner = battle.determine_winner()
    a = battle.battles.first()
    assert winner == a

@pytest.mark.django_db
def test_not_active_battle():
    b = battle_deactived()
    assert b.is_active is False

@pytest.mark.django_db
def test_active_battle():
    b = battle_with_invitations()
    assert b.is_active is True

@pytest.mark.django_db
def test_to_string_battle():
    b = battle_fixture()
    b.id = 1
    b.question.short_description = "test battle"
    assert "Battle (1): test battle" == str(b)

@pytest.mark.django_db
def test_battle_creation():
    b = BattleFactory.create()
    assert b is not None

@pytest.mark.django_db
def test_winner_time():
    battle = battle_without_winner()
    winner = battle.winner_time()
    assert battle.battles.last() == winner

@pytest.mark.django_db
def test_winner_length():
    battle = battle_without_winner()
    winner = battle.determine_winner()
    assert battle.battles.first() == winner

# TESTs to BattleResponse
@pytest.mark.django_db
def test_battle_response_creation():
    br = BattleResponseFactory.create()
    assert br is not None

@pytest.mark.django_db
def test_update_response():
    br = BattleResponseFactory.create()
    response_item = register_item(br,source_code())
    br.update(response_item)
    assert response_item == br.last_item

@pytest.mark.django_db
def test_stringfy_battle_response():
    br = BattleResponseFactory.create()
    name_user = br.response.user
    assert "Battle responses - User: %s" % name_user == str(br)
