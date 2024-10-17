import factory
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=60)
    team_lead = models.ForeignKey(
        Person, null=True, on_delete=models.SET_NULL, related_name="lead_teams"
    )
    members = models.ManyToManyField(Person, related_name="teams")


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    name = factory.Faker("name")


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Faker("name")
