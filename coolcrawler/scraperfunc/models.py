from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from scrapy.contrib.djangoitem import DjangoItem
from dynamic_scraper.models import Scraper, SchedulerRuntime
from slugify import slugify
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.contrib.auth.models import User
import re
#import open_news
#from mongoengine import MongoDBRouter
#from open_news.routers import MongoDBRouter
#import django.db.models.options as options
#options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('monguito',)


#class UserProfile(models.Model):
#    user   = models.OneToOneField(User)
#    avatar = models.ImageField()
    
namespace_regex = re.compile(r'^[A-z][\w-]{2,31}$')

class URLs(models.Model):
    url = models.TextField()
    nameid = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.nameid

    class Meta:
        ordering = ['nameid',]

class PROXYs(models.Model):
    proxy = models.TextField()
    proxyid = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.proxyid

    class Meta:
        ordering = ['proxyid',]
   
class NewsWebsite(models.Model):
    name = models.CharField(max_length=200,unique = True, validators=[RegexValidator(regex=namespace_regex)] )
    #url = models.URLField()
    url = models.ForeignKey(URLs, null=True, on_delete=models.SET_NULL)
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    table_destination = models.CharField(max_length=100)
    item_class = models.CharField(max_length=100)
    delay_per_request = models.IntegerField(max_length=10000,default=0)
    randomdelay = models.BooleanField(default=False)
    useProxy = models.BooleanField(default=False)
    randomizeProxyUsage = models.BooleanField(default=False)
    proxylist = models.ForeignKey(PROXYs, null=True, blank=True, on_delete=models.SET_NULL)
    
    @property
    def slug(self):
        return slugify(self.name)
  
    def __unicode__(self):
        return self.name

class NewsWebsiteForm(ModelForm):

    class Meta:
        model = NewsWebsite
        
class UrlsForm(ModelForm):

    class Meta:
        model = URLs




#Pending!!    
class ProxyForm(ModelForm):

    class Meta:
        model = URLs
#Pending!!!
class UserAgentForm(ModelForm):

    class Meta:
        model = URLs





#class articles(models.Model):
#    title = models.CharField(max_length=200)
#    description = models.TextField(blank=True)
#    url = models.URLField(blank=True)
#    thumbnail = models.CharField(max_length=200, blank=True)
#    htmlcode = models.TextField(blank=True)
 #   _default_manager = MongoDBRouter()

class googlespider(models.Model):
    url = models.URLField(blank=True)
    wholehtml = models.TextField(blank=True)
 #   _default_manager = MongoDBRouter() 
 

class genericmodel(models.Model):
    uniqueid = models.CharField(max_length=100)
    el1 = models.TextField(blank=True)
    el2 = models.TextField(blank=True)
    el3 = models.TextField(blank=True)
    el4 = models.TextField(blank=True)
    el5 = models.TextField(blank=True)
    el6 = models.TextField(blank=True)
    el7 = models.TextField(blank=True)
    el8 = models.TextField(blank=True)
    el9 = models.TextField(blank=True)
    el10 = models.TextField(blank=True)
    el11 = models.TextField(blank=True)
    el12 = models.TextField(blank=True)
    el13 = models.TextField(blank=True)
    el14 = models.TextField(blank=True)
    el15 = models.TextField(blank=True)
    el16 = models.TextField(blank=True)
    el17 = models.TextField(blank=True)
    el18 = models.TextField(blank=True)
    el19 = models.TextField(blank=True)
    el20 = models.TextField(blank=True)
 #   _default_manager = MongoDBRouter() 

    def __unicode__(self):
        return self.uniqueid




#class Article(models.Model):
#    title = models.CharField(max_length=200)
#    news_website = models.ForeignKey(NewsWebsite) 
#    description = models.TextField(blank=True)
#    url = models.URLField(blank=True)
#    thumbnail = models.CharField(max_length=200, blank=True)
#    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
#   # htmlcode = models.TextField(blank=True)
#    def __unicode__(self):
#        return self.title

class GenItem(DjangoItem):
    #django_model = Article
    def __init__(self, kwargs):
        print '$%#"%"$%"%"$%$"'
        print '$%#"%"$%"%"$%$"'
        django_model = getattr(self,kwargs["class"])

        
#class ArticleItem(DjangoItem):
    #django_model = Article
#    django_model = articles

class GoogleItem(DjangoItem):
    django_model = googlespider
    
class GenericItem(DjangoItem):
    django_model = genericmodel

#@receiver(pre_delete)
#def pre_delete_handler(sender, instance, using, **kwargs):
#    if isinstance(instance, NewsWebsite):
#        if instance.scraper_runtime:
#            instance.scraper_runtime.delete()
#    
#    if isinstance(instance, Article):
#        if instance.checker_runtime:
#            instance.checker_runtime.delete()
            
#pre_delete.connect(pre_delete_handler)

class celtest(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()