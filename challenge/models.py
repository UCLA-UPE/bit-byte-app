from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Profile(models.Model):
    ROLE = (
        ('B', 'Byte'),
        ('b', 'Bit')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    team = models.ForeignKey('Team', blank=True, null=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=1, choices=ROLE, blank=True, null=True)
    answers = JSONField(blank=True, default=list)

    def __str__(self):
        team_name = "(none)" if self.team == None else self.team.name
        return '%s %s (user: %s, role=%s, team=%s)' % \
            (self.user.first_name, self.user.last_name, self.user.username, self.role, team_name)

    def points(self):
        points = 0.0
        # one-off events: points = worth * frac
        event_completions = EventCompletion.objects.all()
        checkoffs = EventCheckoff.objects.filter(person=self)
        for completion in event_completions:
            person_event = checkoffs.filter(event_completion=completion)
            points_add = person_event.count() * completion.points
            if not completion.repeatable:
                points_add /= self.team.members().count()
                # one-off completion type: check that there are no duplicates this person
                if person_event.count() > 1:
                    raise ValueError("Detected duplicate checkoffs for user [%s] in non-repeatable event completion [%s] when attempting to calculate points." % (self.user.username, completion.name))
            points += points_add
        return points
