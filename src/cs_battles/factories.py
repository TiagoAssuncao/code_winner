from django.utils import timezone
from codeschool.factories import *
from cs_battles.models import Battle, BattleResponse
from cs_questions.factories import CodingIoQuestionFactory

class BattleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Battle
    battle_owner = factory.SubFactory(UserFactory)
    question = factory.SubFactory(CodingIoQuestionFactory)
    language_id = 1
    """name = factory.LazyAttribute(lambda x: fake.word())
    short_description = factory.LazyAttribute(lambda x: fake.sentence())
    long_description = factory.LazyAttribute(lambda x: fake.text())
    """
    

class BattleResponseFactory(factory.DjangoModelFactory):
    class Meta:
        model = BattleResponse
    battle = factory.SubFactory(BattleFactory)
    time_end = timezone.now()
    response = factory.LazyAttribute(lambda x: x.battle.question.get_response(user=factory.SubFactory(UserFactory)))
