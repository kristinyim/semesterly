from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
   """A db object representing comments made on a timetable. """
   message = models.TextField()
   owner = models.ForeignKey(User)
   image_url = models.CharField(max_length=300, default=-1)
   last_updated = models.DateTimeField(auto_now=True)

   @classmethod
   def create(cls, message, owner, img_url):
       comment = cls(message=message, owner=owner, image_url=img_url)
       return comment