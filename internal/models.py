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
    team = models.ForeignKey('Team', null=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=1, choices=ROLE)
    answers = JSONField(blank=True, default=list)

    def __str__(self):
        return '%s %s (%s)' % (self.user.first_name, self.user.last_name, self.user.username)

class Choice(models.Model):
    chooser = models.ForeignKey(Profile, related_name="chooser", on_delete=models.CASCADE)
    choosee = models.ForeignKey(Profile, related_name="choosee", on_delete=models.CASCADE)

    def __str__(self):
        return '%s chose %s' % (self.chooser, self.choosee)

class Event(models.Model):
    name = models.CharField(max_length=200)
    points = models.IntegerField()

    def __str__(self):
        return '%s (worth %s points)' % (self.name, self.points)

class EventCheckoff(models.Model):

    # class Meta:
    #     permissions = (
    #         ("view_team_checkoff", "Can view their team's event checkoffs"),
    #         ("edit_all_checkoffs", "Can edit everyone's event checkoffs"),
    #     )

    person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return '%s did %s' % (self.person, self.event)

class Team(models.Model):
    name = models.CharField(max_length=200)

    def members(self):
        return Profile.objects.filter(team=self)

    def points(self):
        members = self.members()
        if members.count() == 0: return 0
        checkoffs = EventCheckoff.objects.filter(person__in=members)
        points = 0.0
        for event in Event.objects.all():
            team_event = checkoffs.filter(event=event)
            frac = team_event.count() / members.count()
            points += frac * event.points
        return points

    def __str__(self):
        return '%s (%s points)' % (self.name, self.points())

