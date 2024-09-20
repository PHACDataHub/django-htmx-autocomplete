from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=60)
    members = models.ManyToManyField(Person)

