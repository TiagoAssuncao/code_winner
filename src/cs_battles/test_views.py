from codeschool.tests import *
import pytest_selenium
from cs_battles.test_models import battle_fixture
from cs_battles.factories import BattleResponseFactory
from cs_battles.models import *

@pytest.fixture
def many_battles():
    battles = [battle_fixture() for x in range(10)]
    return battles

@pytest.fixture
def client_loged(client):
    user = user_with_password("1234")
    client.login(username=user.username,password='1234')
    return client,user

@pytest.fixture
def battles_invitation(user):
    battles = many_battles()
    for i in range(2):
        battles[i].invitations_user.add(user)

@pytest.fixture
def battle_response_iospec(user):
    battle_response = BattleResponseFactory.create()
    battle_response.battle=battle_fixture()
    battle_response.response=battle_response.battle.question.get_response(user=user)
    battle_response.battle.question.iospec_source = "Oi"
    battle_response.battle.question.save()
    battle_response.save()
    return battle_response


@pytest.mark.django_db
def test_battles_list(client):
    response = client.get('/battles/')
    assert response.templates[0].name == "battles/list.jinja2"
    assert 200 <= response.status_code < 300


@pytest.mark.django_db
def test_battles_find(client):
    many_battles()
    response = client.get('/battles/')
    assert 'battle_list' in response.context
    assert len(response.context['battle_list']) == 10

@pytest.mark.django_db
def test_invitations_user(client):
    client,user = client_loged(client)
    battles_invitation(user)   
    response = client.get('/battles/invitations')
    assert response.templates[0].name == "battles/invitation.jinja2"
    assert 200 <= response.status_code < 300
    assert 'invitations' in response.context
    assert len(response.context['invitations']) == 2

@pytest.mark.django_db
def test_redirect_battle_response_get(client):
    client,user= client_loged(client)
    response = client.get('/battles/battle/1')
    assert 200 <= response.status_code < 300
    assert response.templates[0].name == 'battles/battle.jinja2'
    assert len(response.context) == 0

@pytest.mark.django_db
def test_battle_submition_accept(client):
    client,user = client_loged(client)
    battle_response = battle_response_iospec(user)
    response = client.post(
                    '/battles/battle/%d'%battle_response.battle.pk,
                    {'code':"print('Oi')"}
                    )
    assert 200 <= response.status_code < 300
    assert 'message' in response.context
    assert 'Sua questão está certa' == response.context['message']

@pytest.mark.django_db
def test_battle_submition_reject(client):
    client,user = client_loged(client)
    battle_response = battle_response_iospec(user)
    response = client.post(
                    '/battles/battle/%d'%battle_response.battle.pk,
                    {'code':"print('O')"}
                    )
    assert 200 <= response.status_code < 300
    assert 'message' in response.context
    assert 'Está errada' == response.context['message']

@pytest.mark.django_db
def test_battles_of_user(client):
    client,user = client_loged(client)
    battle_response_iospec(user)
    battle_response_iospec(user)
    response = client.get('/battles/user')
    
    assert 200 <= response.status_code < 300
    assert 'battles' in response.context
    assert len(response.context['battles']) == 2
    assert response.templates[0].name == 'battles/battle_user.jinja2'

""" 
class _TestURLS(URLBaseTester):
    login_urls = [
        '/battles/',
        '/battles/user',
        '/battles/invitations',
    ]
        url_object.pk
       url(r'^',views.BattleCRUDView.as_include(namespace='battles')),
    url(r'^battle/(?P<battle_pk>\d+)$', views.battle, name='battle'),
    url(r'^user$',views.battle_user, name='user_battle'),
    url(r'^accept$',views.battle_invitation,name="accept_battle"),
    url(r'^invitations$',views.invitations, name="view_invitation"),
"""
