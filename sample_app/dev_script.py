import random

from django.db import transaction

from sample_app.models import Person, PersonFactory, Team, TeamFactory


@transaction.atomic
def run():
    Team.objects.all().delete()
    Person.objects.all().delete()

    people = PersonFactory.create_batch(200)
    teams = TeamFactory.create_batch(40)

    for team in teams:
        team_members = random.sample(people, random.randint(0, 8))
        if team_members:
            team.members.set(team_members)
            team.team_lead = random.choice(team_members)
            team.save()
