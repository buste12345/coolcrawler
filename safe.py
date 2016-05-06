import urllib2

#url = 'http://localhost:6800/listjobs.json?project=default'
url = 'http://localhost:6800/logs/default/article_spider/c03cfe22468c11e592d60242ac11b5c1.log'

response = urllib2.urlopen(url)
webContent = response.read()

print webContent