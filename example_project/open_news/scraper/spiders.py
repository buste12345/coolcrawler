from open_news.django_spider import DjangoSpider
from open_news import models
from scrapy import signals
import socket
import pymongo
from scrapy.conf import settings

class ArticleSpider(DjangoSpider):
    
    name = 'article_spider'
    def __init__(self, *args, **kwargs):

        
        #print self.ref_object.url
        self._set_ref_object(models.NewsWebsite, **kwargs)
        
        urlarray = self.ref_object.url.url.split("|")
        self.scraper = self.ref_object.scraper
        #self.scrape_url = []
        self.scrape_url = urlarray
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.download_delay = self.ref_object.delay_per_request
        self.randomize_download_delay = self.ref_object.randomdelay
        #self.scraped_obj_class = articles
        #self.scraped_obj_item_class = ArticleItem
        
        
        self.scraped_obj_class = getattr(models,self.ref_object.table_destination)
        self.scraped_obj_item_class = getattr(models,self.ref_object.item_class)
        
        #self.scraped_obj_class = models.googlespider
        #self.scraped_obj_item_class = models.GoogleItem
        #self.dotoboso = 'googlespider'
        self.dotoboso = self.ref_object.table_destination
        #self.scraped_obj_item_class = models.GenItem(kwargs)
        #print self.scraped_obj_item_class
        #print '$%#%$#%$#%#'
        super(ArticleSpider, self).__init__(self, *args, **kwargs)
        
class ExtensionThatAccessStats(object):

    name = 'stats'
    def __init__(self, stats):
        self.stats = stats


    @classmethod
    def from_crawler(cls, crawler):
    # print 'nicknack'
    #    print crawler.stats
        #connection = pymongo.Connection(
        #    settings['MONGODB_SERVER'],
        #    settings['MONGODB_PORT']
        #)
        #db = connection[settings['MONGODB_DB']]
        #collection = db['scraplog']
        
        #collection.insert(crawler.stats.get_stats(), safe=True)
        return cls(crawler.stats)
        
