from codeschool import models as auth_model
from cs_core.models import ProgrammingLanguage,ResponseContext,ResponseItem,programming_language
from cs_questions.models import CodingIoQuestion, CodingIoResponseItem
from cs_questions.models import Question
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cs_core.models import Response

class Battle(models.Model):
    """The model to associate many battles"""
    TYPE_BATTLES = (
                    (_("length"),"length"),
                    (_("time"),"time")
                    )
    date = models.DateField(auto_now_add=True)

    invitations_user = models.ManyToManyField(auth_model.User)

    battle_owner = models.ForeignKey(
                auth_model.User,
                related_name="battle_owner"
            )

    battle_winner = models.OneToOneField(
                    'BattleResponse',
                    blank=True,
                    null=True,
                    related_name="winner"
                )

    question = models.ForeignKey(
                    CodingIoQuestion,
                    related_name="battle_question"
                )

    challenge_type = models.CharField(
                _('challenge_type'),
                default=TYPE_BATTLES[0][0],
                choices=TYPE_BATTLES,
                max_length=20,
                help_text=_('Choose a battle challenge type.')
            )
    language = models.ForeignKey(
                ProgrammingLanguage,
                related_name="battle_language"
            )
 
    short_description = property(lambda x: x.question.short_description)

    long_description = property(lambda x: x.question.long_description)
    
    battle_context = models.ForeignKey(ResponseContext)
    @property
    def is_active(self):
        return (len(self.invitations_user.all()) is not 0
                or self.battle_winner is None)

    def __init__(self, *args, **kwargs):
        if 'language' in kwargs and isinstance(kwargs['language'], str):
            kwargs['language'] = programming_language(kwargs['language'])
        super().__init__(*args, **kwargs)
    
    def determine_winner(self):
        if self.is_active:
            self.battle_winner = getattr(self,'winner_'+str(self.challenge_type))()
            self.save()
        return self.battle_winner

    def winner_length(self):
        def source_length(battle):
            if battle.last_item.source is not None:
                return len(battle.last_item.source)
            else:
                return -1
        return min(self.battles.all(), key=source_length)

    def winner_time(self):
        def source_time(battle):
            return battle.time_end - battle.time_begin
        return min(self.battles.all(),key=source_time)

    def __str__(self):
            return "Battle (%s): %s" % (self.id,self.short_description)



class BattleResponse(models.Model):
    """
    BattleResponse class with attributes necessary to one participation for one
    challenger.
    """

    class Meta:
        unique_together = [('response', 'battle')]

    response = models.OneToOneField(Response)
    time_begin = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(
        blank=True,
        null=True,
    )
    battle = models.ForeignKey(Battle,related_name='battles')
 
    last_item = models.ForeignKey(ResponseItem,blank=True,null=True)
    def update(self, response_item):
        self.time_end = response_item.created
        self.last_item = response_item
        self.save()

    def __str__(self):
        return "Battle responses - User: %s" % self.response.user
