from codeschool.factories import *
from cs_battles.models import Battle, BattleResponse
from cs_questions.factories import CodingIoQuestionFactory

class BattleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Battle
    battle_owner = factory.SubFactory(UserFactory)
    question = factory.SubFactory(CodingIoQuestionFactory)
    language_id = 'python'
    """name = factory.LazyAttribute(lambda x: fake.word())
    short_description = factory.LazyAttribute(lambda x: fake.sentence())
    long_description = factory.LazyAttribute(lambda x: fake.text())
    """
    

class BattleResponseFactory(factory.DjangoModelFactory):
    class Meta:
        model = BattleResponse
    battle_id = 1
    """discipline = factory.SubFactory(DisciplineFactory)
    teacher = factory.SubFactory(UserFactory)
    is_active = True
    @factory.post_generation
    def num_students(self, create, extracted, **kwargs):
        if create and extracted:
            num_students = extracted
            for _ in range(num_students):
                user = UserFactory.create()
                self.register_student(user)
    """
