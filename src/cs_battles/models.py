from django.db import models
from django.contrib.auth import models as auth_model
from django.core.urlresolvers import reverse
from cs_questions.models import Question
from cs_core.models import ProgrammingLanguage
from cs_questions.models import CodingIoQuestion, CodingIoResponse

class Battle(models.Model):
    """The model to associate many battles"""
    TYPE_BATTLES = ( ("length","length"),("time","time") )
    date = models.DateField(auto_now_add=True)
    invitations_user = models.ManyToManyField(auth_model.User)
    battle_owner = models.ForeignKey(auth_model.User,related_name="battle_owner")
    battle_winner = models.OneToOneField('BattleResponse',blank=True,null=True,related_name="winner")
    question = models.ForeignKey(CodingIoQuestion,related_name="battle_question")
    type = models.TextField(default=0,choices=TYPE_BATTLES)
    language = models.ForeignKey(ProgrammingLanguage, related_name="battle_language")
    short_description = property(lambda x: x.question.short_description)
    long_description = property(lambda x: x.question.long_description)
    
    def determine_winner(self):
        if (self.battles.first() and not self.battle_winner 
            and not self.invitations_user.all() ):
            self.battle_winner = getattr(self,'winner_'+self.type)()
            self.save()
        return self.battle_winner

    def winner_length(self):
        def source_length(battle):
            return len(battle.source)
        return min(self.battles.all(), key=source_length)
    
    def winner_time(self):
        def source_time(battle):
            return battle.time_end - battle.time_end
        return min(self.battles.all(),key=source_time)

    def __str__(self):
        if self.battle_winner:
            return "(%s) %s Winner: %s" % (self.id,self.battle_winner.user,self.short_description)
        else:
            return "(%s) %s" % (self.id,self.short_description)


class BattleResponse(CodingIoResponse):
    """BattleResponse class with attributes necessary to one participation for one challenger"""

    time_begin = models.DateTimeField()
    time_end = models.DateTimeField()
    battle = models.ForeignKey(Battle,related_name='battles')
    
    def __str__(self):
        return "%s - BattleResponse - User:  %s" % (self.id,self.user)
