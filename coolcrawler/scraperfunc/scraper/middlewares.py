# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
import os
import random
from scrapy.conf import settings

# Start your middleware class
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(settings['HTTP_PROXY']) 
        
        #'https://108.61.180.79:3128'
        #random.choice(settings.get('HTTP_PROXY'))
        
    # Use the following lines if your proxy requires authentication
        #proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        #encoded_user_pass = base64.encodestring(proxy_user_pass)
        #request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        
class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua  = random.choice(settings['USER_AGENT_LIST'])
        if ua:
            request.headers.setdefault('User-Agent', ua)
