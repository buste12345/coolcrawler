import ast, json

from jsonpath_rw import jsonpath, parse
from jsonpath_rw.lexer import JsonPathLexerError

#from scrapy import scrapy
import scrapy
from scrapy import log
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.exceptions import CloseSpider
from scrapy.selector import HtmlXPathSelector

from dynamic_scraper.spiders.django_base_spider import DjangoBaseSpider
from dynamic_scraper.models import ScraperElem
from dynamic_scraper.utils.loader import JsonItemLoader
from dynamic_scraper.utils.scheduler import Scheduler
from dynamic_scraper.utils import processors


class DjangoSpider(DjangoBaseSpider):

    def __init__(self, *args, **kwargs):
        self.mandatory_vars.append('scraped_obj_class')
        self.mandatory_vars.append('scraped_obj_item_class')
        
        super(DjangoSpider, self).__init__(self, *args, **kwargs)
        
        #SET CONFIGS#
        self._set_config(**kwargs)
        
        #PAGINATION METHOD GOES FIRST# 
        self._set_start_urls(self.scrape_url)
        self.scheduler = Scheduler(self.scraper.scraped_obj_class.scraper_scheduler_conf)
        self.from_detail_page = False
        self.loader = None
        
        self.items_read_count = 0
        self.items_save_count = 0
        
        msg = "Spider for " + self.ref_object.__class__.__name__ + " \"" + str(self.ref_object) + "\" (" + str(self.ref_object.pk) + ") initialized."
        self.log(msg, log.INFO)


    def _set_config(self, **kwargs):
        log_msg = ""
        #max_items_read 
        if 'max_items_read' in kwargs:
            try:
                self.conf['MAX_ITEMS_READ'] = int(kwargs['max_items_read'])
            except ValueError:
                raise CloseSpider("You have to provide an integer value as max_items_read parameter!")
            if len(log_msg) > 0:
                log_msg += ", "
            log_msg += "max_items_read " + str(self.conf['MAX_ITEMS_READ'])
        else:
            self.conf['MAX_ITEMS_READ'] = self.scraper.max_items_read
        #max_items_save 
        if 'max_items_save' in kwargs:
            try:
                self.conf['MAX_ITEMS_SAVE'] = int(kwargs['max_items_save'])
            except ValueError:
                raise CloseSpider("You have to provide an integer value as max_items_save parameter!")
            if len(log_msg) > 0:
                log_msg += ", "
            log_msg += "max_items_save " + str(self.conf['MAX_ITEMS_SAVE'])
        else:
            self.conf['MAX_ITEMS_SAVE'] = self.scraper.max_items_save
            
        super(DjangoSpider, self)._set_config(log_msg, **kwargs)


    def _set_start_urls(self, scrape_url):
        
        if self.scraper.pagination_type != 'N':
            if not self.scraper.pagination_append_str:
                raise CloseSpider('Please provide a pagination_append_str for pagination (e.g. "/archive/{page}/")!')
            if self.scraper.pagination_append_str.find('{page}') == -1:
                raise CloseSpider('Pagination_append_str has to contain "{page}" as placeholder for page replace!')
            if not self.scraper.pagination_page_replace:
                raise CloseSpider('Please provide a pagination_page_replace context corresponding to pagination_type!')
        
        if self.scraper.pagination_type == 'R':
            try:
                pages = self.scraper.pagination_page_replace
                pages = pages.split(',')
                if len(pages) > 3:
                    raise Exception
                pages = range(*map(int, pages)) 
            except Exception:
                raise CloseSpider('Pagination_page_replace for pagination_type "RANGE_FUNCT" ' +\
                                  'has to be provided as python range function arguments ' +\
                                  '[start], stop[, step] (e.g. "1, 50, 10", no brackets)!')
        
        if self.scraper.pagination_type == 'F':
            try:
                pages = self.scraper.pagination_page_replace
                pages = pages.strip(', ')
                pages = ast.literal_eval("[" + pages + ",]")
            except SyntaxError:
                raise CloseSpider('Wrong pagination_page_replace format for pagination_type "FREE_LIST", ' +\
                                  "Syntax: 'Replace string 1', 'Another replace string 2', 'A number 3', ...")   
        
        if self.scraper.pagination_type != 'N':
            print 'puto'
            append_str = self.scraper.pagination_append_str
            for page1 in scrape_url:
                print page1

                if page1[-1:] == '/' and append_str[0:1] == '/':
                    append_str = append_str[1:]
                print append_str
                print 'puto2'
                for page in pages:
                    url = page1 + append_str.format(page=page)
                    self.start_urls.append(url)
                if not self.scraper.pagination_on_start:
                    self.start_urls.append(page1)
        
        if self.scraper.pagination_type == 'N':
            print 'xd123'
            print scrape_url
            print 'xd124'
            for page in scrape_url:
                
                print 'sosaaaa'
                self.start_urls.append(page)


    def _set_loader_context(self, context_str):
        try:
            context_str = context_str.strip(', ')
            context = ast.literal_eval("{" + context_str + "}")
            context['spider'] = self
            self.loader.context = context
        except SyntaxError:
            self.log("Wrong context definition format: " + context_str, log.ERROR)


    def _get_processors(self, procs_str):
        procs = [TakeFirst(), processors.string_strip,]
        if not procs_str:
            return procs
        procs_tmp = list(procs_str.split(','))
        for p in procs_tmp:
            p = p.strip()
            if hasattr(processors, p):
                procs.append(getattr(processors, p))
            else:
                self.log("Processor '%s' is not defined!" % p, log.ERROR)
        procs = tuple(procs)
        return procs


    def _scrape_item_attr(self, scraper_elem):
        if(self.from_detail_page == scraper_elem.from_detail_page):
            procs = self._get_processors(scraper_elem.processors)
            self._set_loader_context(scraper_elem.proc_ctxt)
            
            static_ctxt = self.loader.context.get('static', '')
            print "$$$$$$$CYKA$$$$$$$$$"
            if processors.static in procs and static_ctxt:
                print "######OPT 0"
                self.loader.add_value(scraper_elem.scraped_obj_attr.name, static_ctxt)
            elif(scraper_elem.reg_exp):
                print "######OPT 1"
                self.loader.add_xpath(scraper_elem.scraped_obj_attr.name, scraper_elem.x_path, *procs,  re=scraper_elem.reg_exp)
            else:
                print "######OPT 2"
                print scraper_elem.scraped_obj_attr.name
                print scraper_elem.x_path
                print procs
                self.loader.add_xpath(scraper_elem.scraped_obj_attr.name, scraper_elem.x_path, *procs)
            msg  = '{0: <20}'.format(scraper_elem.scraped_obj_attr.name)
            c_values = self.loader.get_collected_values(scraper_elem.scraped_obj_attr.name)
            if len(c_values) > 0:
                msg += "'" + c_values[0] + "'"
            else:
                msg += u'None'
            self.log(msg, log.DEBUG)


    def _set_loader(self, response, xs, item):
        if not xs:
            self.from_detail_page = True
            item = response.request.meta['item']
            if self.scraper.detail_page_content_type == 'J':
                json_resp = json.loads(response.body_as_unicode())
                self.loader = JsonItemLoader(item=item, selector=json_resp)
            else:
                self.loader = ItemLoader(item=item, response=response)
        else:
            self.from_detail_page = False
            if self.scraper.content_type == 'J':
                self.loader = JsonItemLoader(item=item, selector=xs)
            else:
                self.loader = ItemLoader(item=item, selector=xs)
        self.loader.default_output_processor = TakeFirst()
        self.loader.log = self.log


    def start_requests(self):
        for url in self.start_urls:
            meta = {}
            if self.scraper.content_type == 'H' and self.scraper.render_javascript:
                meta['splash'] = {
                    'endpoint': 'render.html',
                    'args': self.conf['SPLASH_ARGS'].copy()
                }
            yield Request(url, self.parse, meta=meta)


    def _check_for_double_item(self, item):
        idf_elems = self.scraper.get_id_field_elems()
        num_item_idfs = 0
        for idf_elem in idf_elems:
            idf_name = idf_elem.scraped_obj_attr.name
            if idf_name in item:
                num_item_idfs += 1

        cnt_double = 0
        if num_item_idfs == len(idf_elems):
            qs = self.scraped_obj_class.objects
            for idf_elem in idf_elems:
                idf_name = idf_elem.scraped_obj_attr.name
                qs = qs.filter(**{idf_name:item[idf_name]})
            cnt_double = qs.count()

        # Mark item as DOUBLE item
        if cnt_double > 0:
            for idf_elem in idf_elems:
                idf_name = idf_elem.scraped_obj_attr.name
                if item[idf_name][0:6] != 'DOUBLE':
                    item[idf_name] = 'DOUBLE' + item[idf_name]
            return item, True
        else:
            return item, False
    
    
    def parse_item(self, response, xs=None):
        self._set_loader(response, xs, self.scraped_obj_item_class())
        if not self.from_detail_page:
            self.items_read_count += 1
            
        elems = self.scraper.get_scrape_elems()
        
        for elem in elems:
            self._scrape_item_attr(elem)
        # Dealing with Django Char- and TextFields defining blank field as null
        item = self.loader.load_item()
        for key, value in item.items():
            if value == None and \
               self.scraped_obj_class()._meta.get_field(key).blank and \
               not self.scraped_obj_class()._meta.get_field(key).null:
                item[key] = ''
        if self.from_detail_page:
            #item, is_double = self._check_for_double_item(item)
            print 'DONT DO ANYTHING##'
        
        return item


    def parse(self, response):
        xs = Selector(response)
        base_elem = self.scraper.get_base_elem()

        if self.scraper.content_type == 'J':
            json_resp = json.loads(response.body_as_unicode())
            try:
                jsonpath_expr = parse(base_elem.x_path)
            except JsonPathLexerError:
                raise CloseSpider("JsonPath for base elem could not be processed!")
            base_objects = [match.value for match in jsonpath_expr.find(json_resp)]
            if len(base_objects) > 0:
                base_objects = base_objects[0]
        else:
            base_objects = response.xpath(base_elem.x_path)

        if(len(base_objects) == 0):
            self.log("No base objects found!", log.ERROR)
        
        if(self.conf['MAX_ITEMS_READ']):
            items_left = min(len(base_objects), self.conf['MAX_ITEMS_READ'] - self.items_read_count)
            base_objects = base_objects[0:items_left]
        

        for obj in base_objects:
            item_num = self.items_read_count + 1
            self.log("Starting to crawl item %s." % str(item_num), log.INFO)
            item = self.parse_item(response, obj)
            
            if self.scraper.scrape_urls:
                print "scraper allowed"
            else:
                print "scraper not allowed"
                
            print '#############LOOOK##############'
            print item
            print '#############FINISH##############'
            
            if item:
                only_main_page_idfs = True
                idf_elems = self.scraper.get_id_field_elems()
                for idf_elem in idf_elems:
                    if idf_elem.from_detail_page:
                        only_main_page_idfs = False

                is_double = False
                if only_main_page_idfs:
                    #item, is_double = self._check_for_double_item(item)
                    print 'DONT DO ANYTHING 2##'
                
                meta = {}
                meta['item'] = item
                
                if self.scraper.detail_page_content_type == 'H' and self.scraper.render_javascript:
                    meta['splash'] = {
                        'endpoint': 'render.html',
                        'args': self.conf['SPLASH_ARGS'].copy()
                    }
                # Don't go on reading detail page when...
                # No detail page URL defined or
                # DOUBLE item with only main page IDFs and no standard update elements to be scraped from detail page or 
                # generally no attributes scraped from detail page
                cnt_sue_detail = self.scraper.get_standard_update_elems_from_detail_page().count()
                cnt_detail_scrape = self.scraper.get_from_detail_page_scrape_elems().count()

                if self.scraper.get_detail_page_url_elems().count() == 0 or \
                    (is_double and cnt_sue_detail == 0) or cnt_detail_scrape == 0:
                    print "----#######DETAIL PAGE URL EXISTS#######----"
                    print 'sxsxsxsxsxs'
                    yield item
                else:
                    print "----#######DETAIL PAGE URL DOES NOT EXISTS#######----"
                    url_elem = self.scraper.get_detail_page_url_elems()[0]
                    
                    print 'zxzxzxzxzxzxzxzxxz'
                    print url_elem
                    print 'zxzxzxzxzxzxzxzxxz'
                    url = item[url_elem.scraped_obj_attr.name]
                    print 'zxzxzxzxzxzxzxzxxz'
                    print url
                    print 'zxzxzxzxzxzxzxzxxz'
                    #request = Request(item['url'], callback=lambda r:self.parse_htmlcoderet(r,item))
                    yield Request(url, callback=self.parse_item, meta=meta)
                    #yield request
            else:
                self.log("Item could not be read!", log.ERROR)

        
    def parse_item2(self, response, xs=None):
        self._set_loader(response, xs, self.scraped_obj_item_class())
        if not self.from_detail_page:
            self.items_read_count += 1
            
        elems = self.scraper.get_scrape_elems()
        
        for elem in elems:
            self._scrape_item_attr(elem)
        # Dealing with Django Char- and TextFields defining blank field as null
        item = self.loader.load_item()
        for key, value in item.items():
            if value == None and \
               self.scraped_obj_class()._meta.get_field(key).blank and \
               not self.scraped_obj_class()._meta.get_field(key).null:
                item[key] = ''
        if self.from_detail_page:
            #item, is_double = self._check_for_double_item(item)
            print 'DONT DO ANYTHING##'
        
        item['wholehtml'] = item['url'].split("adurl=",1)[1]
        #item['wholehtml'] = bung.split("%3F",1)[0]
        if self.scraper.scrape_urls:
            item['wholehtml'] = response.body
        return item