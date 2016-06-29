from django.utils import timezone
from codeschool.factories import *
from cs_battles.models import Battle, BattleResponse
from cs_questions.factories import CodingIoQuestionFactory

class BattleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Battle
    battle_owner = factory.SubFactory(UserFactory)
    question_id = factory.SubFactory(CodingIoQuestionFactory)
    language_id = 'python'
    """name = factory.LazyAttribute(lambda x: fake.word())
    short_description = factory.LazyAttribute(lambda x: fake.sentence())
    long_description = factory.LazyAttribute(lambda x: fake.text())
    """
    

class BattleResponseFactory(factory.DjangoModelFactory):
    class Meta:
        model = BattleResponse
    battle_id = 1
    question = factory.SubFactory(CodingIoQuestionFactory)
    user = factory.SubFactory(UserFactory)
    language_id = 'python'
    time_begin = timezone.now()
    time_end = timezone.now()
