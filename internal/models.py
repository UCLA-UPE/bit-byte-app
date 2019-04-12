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

class Profile(models.Model):
    ROLE = (
        ('B', 'Byte'),
        ('b', 'Bit')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', blank=True, null=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=1, choices=ROLE)
    answers = JSONField(blank=True, default=list)

    def __str__(self):
        team_name = "(none)" if self.team == None else self.team.name
        return '%s %s (user: %s, role=%s, team=%s)' % \
            (self.user.first_name, self.user.last_name, self.user.username, self.role, team_name)

    def points(self):
        points = 0.0
        # one-off events: points = worth * frac
        events = Event.objects.all()
        checkoffs = EventCheckoff.objects.filter(person=self)
        for event in events:
            person_event = checkoffs.filter(event=event)
            points_add = person_event.count() * event.points
            if not event.repeatable:
                points_add /= self.team.members().count()
                # one-off: check that there are no duplicates for the same event and person
                if person_event.count() > 1:
                    raise ValueError("Detected duplicate checkoffs for user [%s] in non-repeatable event [%s] when attempting to calculate points." % (self.user.username, event.name))
            points += points_add
        return points

class Choice(models.Model):
    chooser = models.ForeignKey(Profile, related_name="chooser", on_delete=models.CASCADE)
    choosee = models.ForeignKey(Profile, related_name="choosee", on_delete=models.CASCADE)

    def __str__(self):
        return '%s chose %s' % (self.chooser, self.choosee)

class EventCategory(models.Model):

    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

class Event(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(EventCategory, blank=True, null=True, on_delete=models.SET_NULL)
    repeatable = models.BooleanField(default=False)
    points = models.IntegerField()

    def __str__(self):
        if self.category is not None:
            return '%s (%s, worth %s points)' % (self.name, self.category, self.points)
        else:
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
        points = 0.0
        for member in self.members():
            points += member.points()
        return points

    def __str__(self):
        return '%s (%s points)' % (self.name, self.points())

