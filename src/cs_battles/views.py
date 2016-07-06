from django.shortcuts import render,redirect
from django.http import Http404,HttpResponse
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from cs_questions.models.coding_io import CodingIoQuestion
from cs_core.models import ProgrammingLanguage, ResponseContext
from .models import BattleResponse, Battle
from datetime import datetime
from viewpack import CRUDViewPack
from django.views.generic.edit import ModelFormMixin
import json
#from .forms import  BattleForm

MAXIMUM_POINT = 100
AC = 0
WA = 1
LIMIT = 2
MESSAGES = {
                AC: "Sua questão está certa",
                WA: "Está errada",
                LIMIT: "Atingiu limite de submissões",
            }
def battle(request,battle_pk):
    battle = Battle.objects.get(id=battle_pk)
    if request.method == "POST":
        status_code = 0
        given_grade = 0.0
        post = request.POST
        if post:
            # Obtain attributes from post
            battle_code = post.get("code")
            try:
                battle_response = battle.battles \
                                .get(response__user_id=request.user.id)
                response_item = battle_response.submit_code(battle_code)
                given_grade = response_item.given_grade
                battle_is_correct = (response_item.given_grade == MAXIMUM_POINT)
                if battle_is_correct:
                    status_code = AC
                else:
                    status_code = WA
                    MESSAGES[WA]="Está errada: %.2f%%"%float(given_grade)
            except Exception as e:
                print(e)
                status_code = LIMIT
        context = {
            'status_code':status_code,
            'messages':MESSAGES
        }
        return HttpResponse(json.dumps(context),content_type="application/json")
#        return render(request, 'battles/result.jinja2', context)
    else:
        return render(request, 'battles/battle.jinja2',{'battle':battle})

def battle_give_up(request,battle_pk):
    if request.method == "POST":
        post = request.POST
        if post:
            # Make the submition to prevent errors
            battle = Battle.objects.get(id=battle_pk)
            battle_response = battle.battles \
                              .get(response__user_id=request.user.id)
            battle_response.submit_code(post.get("code"))
            battle_response.give_up_battle()
    return HttpResponse('')

def battle_user(request):
    """Define the battles of a user"""
    user = request.user
    battles = BattleResponse.objects.filter(response__user_id=user.id)
    context = {"battles": battles}
    return render(request, 'battles/battle_user.jinja2', context)


# View the invitations
def invitations(request):
    invitations_user = Battle.objects.filter(invitations_user=request.user.id).all()
    context = {'invitations': invitations_user}
    return render(request,'battles/invitation.jinja2', context)

# Accept the invitation
def battle_invitation(request):
    if request.method == "POST":
        form_post = request.POST
        battle_pk = form_post.get('battle_pk')
        method_return = None
        if form_post.get('accept'):
            battle = Battle.objects.get(id=battle_pk)
            create_battle_response(battle,request.user)
            method_return = redirect(reverse('cs_battles:battle',kwargs={'battle_pk':battle_pk}))
        elif battle_pk and form_post.get('reject'):
            battle_result = Battle.objects.get(id=battle_pk)
            battle_result.invitations_user.remove(request.user)
            method_return = redirect(reverse('cs_battles:view_invitation'))
    return method_return

def create_battle_response(battle,user):
    response = battle.question.get_response(
                                user=user,
                                context=battle.battle_context
                                )
    battle_response = BattleResponse.objects.get_or_create(
        response=response,
        battle=battle
    )
    battle.invitations_user.remove(user)

class BattleCRUDView(CRUDViewPack):
    model = Battle
    template_extension = '.jinja2'
    template_basename = 'battles/'
    check_permissions = False
    raise_404_on_permission_error = False
    exclude_fields = ['battle_owner','battle_winner','battle_context']

    class CreateMixin:

        def get_success_url(self):
            return reverse("cs_battles:battle",kwargs={'battle_pk': self.object.pk})

        def create_context(self,battle):
            last_pk = 1
            if Battle.objects.last() is not None:
                last_pk = Battle.objects.last().pk+1
            return ResponseContext.objects.get_or_create(
                                activity=battle.question,
                                name="battle_"+str(last_pk)
                            )[0]
        def form_valid(self,form):
            self.object = form.save(commit=False)
            self.object.battle_owner = self.request.user
            self.object.battle_context = self.create_context(self.object)
            self.object.save()
            form.save_m2m()
            create_battle_response(self.object,self.request.user)
            return super(ModelFormMixin, self).form_valid(form)

    class DetailViewMixin:
        def get_object(self,queryset=None):
            object = super().get_object(queryset)
            object.determine_winner()
            return object

        def get_context_data(self, **kwargs):
                return super().get_context_data(
                    all_battles=self.object.battles.all(),**kwargs)

