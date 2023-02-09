# Generated by Django 4.1.4 on 2023-02-07 16:53

from django.db import migrations, models

from faker import Faker

def generate_names(apps, schema_editor):
    faker = Faker()
    Person = apps.get_model("ac_test", "Person")
    for x in range(0, 1000):
        p = Person()
        p.name = faker.name()
        p.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=60)),
                ("members", models.ManyToManyField(to="ac_test.person")),
            ],
        ),
        migrations.RunPython(generate_names),
    ]
