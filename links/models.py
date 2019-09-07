from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse # For get_absolute_url

class LinkVoteCountManager(models.Manager):
    def get_queryset(self):
        return super(LinkVoteCountManager, self).get_queryset().annotate(
            votes=Count('vote')).order_by("-votes")


class Link(models.Model):
    title = models.CharField("Headline", max_length=100)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    submitted_on = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    url = models.URLField("URL", max_length=250, blank=True)
    thumbnail = models.URLField("Thumbnail", max_length=250, blank=True)
    description = models.TextField(blank=True)

    with_votes = LinkVoteCountManager()
    objects = models.Manager()            # default manager

    def __unicode__(self):
        return self.title

    # Solve "“Either provide a url or define a get_absolute_url method on the Model.” error
    def get_absolute_url(self):
        return reverse('link_detail', kwargs={'pk': str(self.id)})

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.PROTECT)
    link = models.ForeignKey(Link, on_delete=models.PROTECT)

    def __unicode__(self):
        return "%s voted %s" % (self.voter.username, self.link.title)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.PROTECT)
    # Extra attributes
    bio = models.TextField(null=True)

    def __unicode__(self):
        return "%s's profile" % self.user

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)
