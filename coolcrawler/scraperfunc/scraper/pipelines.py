from django.db.utils import IntegrityError
from scrapy import log
from scrapy.exceptions import DropItem
from dynamic_scraper.models import SchedulerRuntime
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem

            
class DjangoWriterPipeline(object):
    
    def process_item(self, item, spider):
        try:
            
            item['news_website'] = spider.ref_object
            
            checker_rt = SchedulerRuntime(runtime_type='C')
            #checker_rt.save(using='monguito')
            checker_rt.save()
            
            item['checker_runtime'] = checker_rt
            #item.save(using='monguito')
            item.save()
            
            spider.action_successful = True
            spider.log("Item saved.", log.INFO)
                
        except IntegrityError, e:
            spider.log(str(e), log.ERROR)
            raise DropItem("Missing attribute.")
                
        return item




class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.Connection(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]
        
        
    def process_item(self, item, spider):
        print 'KICK'
        uid= spider.scraper.get_name_field_elems()
        print 'KACK'
        self.collection = self.db[settings['MONGODB_COLLECTION']+spider.dotoboso]
        print 'putx'
        print dir(spider)
        try:
            #item['news_website'] = spider.ref_object
            
            #checker_rt = SchedulerRuntime(runtime_type='C')
            #checker_rt.save(using='monguito')
            #checker_rt.save()
            
            #item['checker_runtime'] = checker_rt
            #item.save(using='monguito')
            valid = True
            for data in item:
                if not data:
                    valid = False
                    log.msg("Error in data 1.")
                    raise DropItem("Missing {0}!".format(data))
            if valid:
                #self.collection.insert(dict(item))
                #self.collection.update({'url': item['url']}, dict(item), upsert=True)
                self.collection.update({uid: item[uid]}, dict(item), upsert=True)
                log.msg("Website added/updated to MongoDB database!",
                level=log.DEBUG, spider=spider)
            return item
                
        except IntegrityError, e:
            print 'putx2'
            spider.log(str(e), log.ERROR)
            raise DropItem("Missing attribute.")
        print 'putx3'      
        return item
        #valid = True
        #for data in item:
        #    if not data:
        #        valid = False
        #        raise DropItem("Missing {0}!".format(data))
        #if valid:
        #    self.collection.insert(dict(item))
        #    log.msg("Crawled info added to MongoDB database!",
        #            level=log.DEBUG, spider=spider)
        #return item