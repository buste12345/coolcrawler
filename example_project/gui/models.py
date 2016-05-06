from django.db import models
from django.core.urlresolvers import reverse

from djangotoolbox.fields import ListField, EmbeddedModelField

class auth_user(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    body = models.TextField()
    comments = ListField(EmbeddedModelField('Comment'), editable=False)

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField(verbose_name="Comments")
    author = models.CharField(verbose_name="Namett", max_length=255)

class celtest(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()

class entry(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    slug = models.SlugField()

   # def get_absolute_url(self):
    #    return reverse('entry', kwargs={"slug": self.slug})
    #def __unicode__(self):
    #    return self.title
    #class Meta:
    #    ordering = ["-title"]