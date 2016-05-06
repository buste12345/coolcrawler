from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from scrapy.contrib.djangoitem import DjangoItem
from dynamic_scraper.models import Scraper, SchedulerRuntime
#import open_news
#from mongoengine import MongoDBRouter
#from open_news.routers import MongoDBRouter
#import django.db.models.options as options
#options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('monguito',)

class NewsWebsite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return self.name
        
class articles(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    thumbnail = models.CharField(max_length=200, blank=True)
    htmlcode = models.TextField(blank=True)
 #   _default_manager = MongoDBRouter()

class googlespider(models.Model):
    url = models.URLField(blank=True)
    wholehtml = models.TextField(blank=True)
 #   _default_manager = MongoDBRouter() 
 
    def __unicode__(self):
        return self.url
        



class Article(models.Model):
    title = models.CharField(max_length=200)
    news_website = models.ForeignKey(NewsWebsite) 
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    thumbnail = models.CharField(max_length=200, blank=True)
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    htmlcode = models.TextField(blank=True)
    def __unicode__(self):
        return self.title

class GenItem(DjangoItem):
    #django_model = Article
    def __init__(self, kwargs):
        print '$%#"%"$%"%"$%$"'
        print '$%#"%"$%"%"$%$"'
        a = getattr(self,kwargs["class"])

        
    
class ArticleItem(DjangoItem):
    #django_model = Article
    django_model = articles

class GoogleItem(DjangoItem):
    django_model = googlespider
    
@receiver(pre_delete)
def pre_delete_handler(sender, instance, using, **kwargs):
    if isinstance(instance, NewsWebsite):
        if instance.scraper_runtime:
            instance.scraper_runtime.delete()
    
    if isinstance(instance, Article):
        if instance.checker_runtime:
            instance.checker_runtime.delete()
            
pre_delete.connect(pre_delete_handler)

class celtest(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()