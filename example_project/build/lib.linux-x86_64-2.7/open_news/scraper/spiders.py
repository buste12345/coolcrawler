from dynamic_scraper.spiders.django_spider import DjangoSpider
from open_news import models

class ArticleSpider(DjangoSpider):
    
    name = 'article_spider'

    def __init__(self, *args, **kwargs):

        self._set_ref_object(models.NewsWebsite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        #self.scraped_obj_class = articles
        #self.scraped_obj_item_class = ArticleItem
        #self.scraped_obj_class = getattr(models,kwargs["class"])
        #self.scraped_obj_item_class = getattr(models,kwargs["itemc"])
        self.scraped_obj_class = models.googlespider
        self.scraped_obj_item_class = models.GoogleItem
        self.dotoboso = kwargs["class"]
        #self.scraped_obj_item_class = models.GenItem(kwargs)
        #print self.scraped_obj_item_class
        #print '$%#%$#%$#%#'
        super(ArticleSpider, self).__init__(self, *args, **kwargs)