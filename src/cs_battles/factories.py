from django.utils import timezone
from codeschool.factories import *
from cs_battles.models import Battle, BattleResponse
from cs_questions.factories import CodingIoQuestionFactory
from cs_core.factories import ProgrammingLanguageFactory
from cs_core.models import ResponseContext

class BattleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Battle
    battle_owner = factory.SubFactory(UserFactory)
    question = factory.SubFactory(CodingIoQuestionFactory)
    language = 'python'
    battle_context = factory.LazyAttribute(
            lambda x: ResponseContext.objects
                                    .get_or_create(
                                            activity=x.question,
                                            name=fake.word()
                                        )[0]
                    )
    """name = factory.LazyAttribute(lambda x: fake.word())
    short_description = factory.LazyAttribute(lambda x: fake.sentence())
    long_description = factory.LazyAttribute(lambda x: fake.text())
    """
    

class BattleResponseFactory(factory.DjangoModelFactory):
    class Meta:
        model = BattleResponse
    battle = factory.SubFactory(BattleFactory)
    time_end = timezone.now()
    response = factory.LazyAttribute(lambda x: x.battle.question.get_response(user=UserFactory.create()))
