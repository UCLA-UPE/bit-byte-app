from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import JSONField

# Create your models here.
class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

def questions():
    return [
        'question1',
        'question2',
        'question3',
        'question4',
        'question5',
    ]

class SiteSettings(SingletonModel):
    class Meta:
        verbose_name_plural = "Site Settings"
    byte_signup_pass = models.CharField(max_length=255, default="upe_byte")
    bit_signup_pass = models.CharField(max_length=255, default="bits_2019")
    questions = JSONField(default=questions)

class Profile(models.Model):
    ROLE = (
        ('B', 'Byte'),
        ('b', 'Bit')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=ROLE)
    answers = JSONField(blank=True, default=list)

    def __str__(self):
        return self.user.username

class Choice(models.Model):
    chooser = models.ForeignKey(Profile, related_name="chooser", on_delete=models.CASCADE)
    choosee = models.ForeignKey(Profile, related_name="choosee", on_delete=models.CASCADE)
    final = models.BooleanField("Choice Finalized", default=False)