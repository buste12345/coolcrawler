from celery.task import task
from django.db.models import Q
from open_news.task_utils import TaskUtils
#from dynamic_scraper.utils.task_utils import TaskUtils
from open_news.models import NewsWebsite, Article

@task()
def run_spiders():
    t = TaskUtils()
    #Optional as well: For more complex lookups you can pass Q objects vi args argument

    print 'tur12'
    t.run_spiders(NewsWebsite, 'scraper', 'scraper_runtime', 'article_spider')
    print 'tur13'
    #'id=2','do_action=yes','class=googlespider','itemc=GoogleItem')
    
@task()
def run_checkers():
    t = TaskUtils()
    t.run_checkers(Article, 'news_website__scraper', 'checker_runtime', 'article_checker')