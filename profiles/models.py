from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=50)
    dob = models.DateField()
    # TODO photo


class Certificate(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE
    )
    title=models.CharField(max_length=40)


class Workplace(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE
    )
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=60)


class Position(models.Model):
    workplace = models.ForeignKey(
        Workplace, on_delete=models.CASCADE
    )
    title=models.CharField(max_length=70)
