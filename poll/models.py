# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.manager import Manager
from django.contrib.auth import get_user_model
from django.db.models import Count

from taggit.managers import TaggableManager


import datetime

# Create your models here.
class PollCollection(models.Model):
    date = models.DateField(default=datetime.date.today)
    name = models.CharField(max_length=255, unique=True)

    description = models.TextField(default="",blank=True)

    # List of Group Names
    visible         = models.CharField(max_length=255,default="",blank=True)
    visible_results = models.CharField(max_length=255,default="",blank=True)

    is_published = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Umfrage"
        verbose_name_plural = "Umfragen"
        permissions = (
            ('vote_pollcollection',    'Umfrage abstimmen'),
            ('analyze_pollcollection', 'Umfrage auswerten'),
        )

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def can_view(self, user):
        return user.has_perm('view_pollcollection', self) \
            or user.has_perm('vote_pollcollection', self)

    def can_vote(self, user):
        return user.has_perm('vote_pollcollection', self)

    def can_analyze(self, user):
        return user.has_perm('analyze_pollcollection', self)

    def can_change(self, user):
        return user.has_perm('change_pollcollection', self)


class Poll(models.Model):
    poll_collection = models.ForeignKey(PollCollection, on_delete=models.CASCADE)

    RADIO = 'RA'
    CHECKBOX = 'CE'
    TEXT = 'TX'
    TYPE_CHOICES = (
        (RADIO, 'Einfachauswahl'),
        (CHECKBOX, 'Mehrfachauswahl'),
        (TEXT, 'Freitext')
    )

    poll_type = models.CharField(max_length=2,
                                 choices=TYPE_CHOICES,
                                 default=RADIO) 

    question = models.CharField(max_length=255, unique=True)
    description = models.TextField(default="")

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    class Meta:
        verbose_name = "Frage"
        verbose_name_plural = "Fragen"

    def __unicode__(self):
        return self.question

    def __str__(self):
        return self.question

    @property
    def is_text(self):
        return self.poll_type == Poll.TEXT
    
    @property
    def items(self):
        _items = Item.objects.filter(poll=self)
        return reversed(sorted(_items, key=lambda i: i.position))

    @property
    def results(self):
        return [(item, int(item.vote_count/float(self.vote_count)*100)) for item in self.items]

    @property
    def votes(self):
        return Vote.objects \
                   .filter(poll=self)

    @property
    def vote_count(self):
        return self.votes.aggregate(votes=Count('user', distinct=True))['votes']


class Item(models.Model):
    value = models.CharField(max_length=255, unique=True)
    position = models.SmallIntegerField(default=1)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Antwort"
        verbose_name_plural = "Antworten"

    def __unicode__(self):
        return self.value

    def __str__(self):
        return self.value

    @property
    def vote_count(self):
        return Vote.objects.filter(item=self).count()


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), verbose_name='voter', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, verbose_name='voted item', null=True,
                             on_delete=models.CASCADE)
    text = models.TextField(default="", blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
