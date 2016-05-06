from gui.models import entry
from open_news.models import NewsWebsite, URLs
from mongoengine import queryset
from slugify import slugify
from open_news.task_utils import TaskUtils
from open_news.scraper.spiders import ArticleSpider, ExtensionThatAccessStats
import urllib2
import re
import json

def returno():
    itemss = entry.objects.using('monguito').all()
    print 'lolno'
    return itemss
    
def returnosp(slugg):
    itemss = entry.objects.using('monguito').get(slug=slugg)
    return itemss
    
def getsites(param):
    if param is 'profs':
        webs = NewsWebsite.objects.all()
        print webs
        return webs
    
def geturls(param):
    if param is 'urls':
        urls = URLs.objects.all()
        return urls

def spiderstatus():
    
    url = 'http://localhost:6800/listjobs.json?project=default'
    response = urllib2.urlopen(url)
    webContent = response.read()
    b = json.loads(webContent)
    
    #UNCOMMENT LATER##
    #b= defino('finished',b)
    #b= defino('running',b)
    #b= defino('pending',b)


    
    return b
    #return ExtensionThatAccessStats(ArticleSpider)


def defino(param, contentn):
    ids = []
    for i in range (0, len (contentn[param])):
        #ids = b['finished'][i]['id']
        #print b['finished'][i]['id']
        ids.append(contentn[param][i]['id'])
    #print ids
    #print 'cuckk'
    #a_dict = {'itemsc': []}
    #contentn.update(a_dict)
    i=0
    for ida in ids:
        
        #url = 'http://localhost:6800/items/default/article_spider/'+ida+'.jl'
        #response = urllib2.urlopen(url)
        #if response.getcode() = 404
        if param == 'finished':    
            try:
                url = 'http://localhost:6800/logs/default/article_spider/'+ida+'.log'
                response = urllib2.urlopen(url)
                webContent = response.read()
                c = webContent
                c = re.search("'item_scraped_count': (.*?),", c).group(1)

            except urllib2.HTTPError:
                print 'Could not download', url
                c = 0
        
            contentn[param][i]['count'] = c

        if param == 'running':    
            try:
                url = 'http://localhost:6800/items/default/article_spider/'+ida+'.jl'
                response = urllib2.urlopen(url)
                webContent = response.read()
                c = webContent.count('uniqueid')
                #c = re.search("'item_scraped_count': (.*?),", c).group(1)
           
            except urllib2.HTTPError:
                print 'Could not download', url
                c = 0
        
            contentn[param][i]['count'] = c
            
        i+=1
    return contentn

def runspider(idspider):
    t = TaskUtils()
    t.run_spider_once(idspider,'article_spider',NewsWebsite)
    return None

def returnosites(slugg):
    itemss = NewsWebsite.objects.get(name=slugg)
    return itemss
    
def returnspider(slugg):
    print slugg
    url = 'http://localhost:6800/logs/default/article_spider/'+slugg+'.log'
    response = urllib2.urlopen(url)
    webContent = response.read()
    return webContent

def spiderjobs(slugg):
    print slugg
    url = 'http://localhost:6800/items/default/article_spider/'+slugg+'.jl'
    response = urllib2.urlopen(url)
    webContent = response.read()
    return webContent