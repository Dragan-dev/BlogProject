from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host =models.ForeignKey(User,on_delete=models.SET_NULL, null=True)  #person who write post
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    participants =models.ManyToManyField(User , related_name="participants", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
            return str(self.name)

    class Meta:
        ordering = ['-updated', '-created'] #when we put minus sign in front of order field it means orders were be descending (from the newest to the oldest)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # this is one to many RS which
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # means that one room can have lots of messages, and attribute on_delete = models.CASCADE stands for case when we delete some
    # room and all messages connected to that room will be deleted
    body = models.TextField(max_length=500)
    # aut_now_add = True takes snapshot when message is created-only once
    created = models.DateTimeField(auto_now_add=True)
    # auto_now = True takes snapshot whenever this field bein filled
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['updated', '-created']  

    def __str__(self):
        return self.body[:30]
