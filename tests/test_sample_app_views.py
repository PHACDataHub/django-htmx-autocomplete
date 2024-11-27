from django.urls import reverse

from sample_app.models import Person, PersonFactory, Team, TeamFactory


def create_teams():
    people = PersonFactory.create_batch(3)
    t1 = TeamFactory(team_lead=people[0])
    t1.members.set(people[1:])

    t2 = TeamFactory(team_lead=None)

    return t1, t2


def test_basic_example(client):
    t1, t2 = create_teams()

    url = reverse("edit_team", args=[t1.pk])
    assert client.get(url).status_code == 200

    url = reverse("edit_team", args=[t2.pk])
    assert client.get(url).status_code == 200


def test_with_prefix(client):
    t1, t2 = create_teams()

    url = reverse("edit_team_w_prefix", args=[t1.pk])
    assert client.get(url).status_code == 200

    url = reverse("edit_team_w_prefix", args=[t2.pk])
    assert client.get(url).status_code == 200


def test_with_model(client):
    t1, t2 = create_teams()

    url = reverse("edit_team_w_model", args=[t1.pk])
    assert client.get(url).status_code == 200

    url = reverse("edit_team_w_model", args=[t2.pk])
    assert client.get(url).status_code == 200


def test_static_formset_example(client):
    t1, t2 = create_teams()
    t3, t4 = create_teams()

    url = reverse("static_formset_example")
    assert client.get(url).status_code == 200


def test_dynamic_formset_example(client):
    t1, t2 = create_teams()
    t3, t4 = create_teams()

    url = reverse("dynamic_formset_example")
    assert client.get(url).status_code == 200
