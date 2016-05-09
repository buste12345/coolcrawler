from django.conf.urls import patterns, url, include
from django.views.generic import ListView, TemplateView
from gui.views import PostDetailView, login, seeadvset, logged_in, test11, entrypoint, entrypointdet, seewebs, webdet, add_site,seeurls, add_urls,checkstatus,statusget,spideritems
from gui.models import Post
from django.contrib import admin

from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example_project2.views.home', name='home'),
    # url(r'^example_project2/', include('example_project2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^mongonaut/', include('mongonaut.urls')),
    url(r'^admin/', include(admin.site.urls)),
   # (r'^mongonaut/', include('mongonaut.urls'))
   
   ##
   
   
       url(r'^blot/', ListView.as_view(
        queryset=Post.objects.all(),
        context_object_name="posts_list"),
        name="home"
    ),
    url(r'^post/(?P<slug>[a-zA-Z0-9-]+)/$', PostDetailView.as_view(
        queryset=Post.objects.all(),
        context_object_name="post"),
        name="post"
    ),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^login/$', login)
    url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^login/$', my_view),
    url(r'^welcome/$', logged_in),
    url(r'^welcome/home/$', entrypoint),
    url(r'^home/status/$', checkstatus,name='spiders'),
    url(r'^welcome/urls/$', seeurls, name='urlsview'),
    url(r'^welcome/webs/$', seewebs, name='sitesview'),
    url(r'^home/crawler/advance_settings/$', seeadvset, name='sitesview'),
    # url(r'^home/addsite2/$', addsite),
     url(r'^home/addurls/$', add_urls, name='podd'),
        url(r'^home/addsite/$', add_site, name='padd'),
    url(r'^testo/$', test11),
    #
    url(r'^entry/(?P<slug>[a-zA-Z0-9-]+)/$', entrypointdet, name="entry"),
    url(r'^webs/(?P<slug>[a-zA-Z0-9-]+)/$', webdet, name="urlweb"),
    url(r'^home/status/(?P<slug>[a-zA-Z0-9-]+)/$', statusget, name="statusweb"),
        url(r'^home/status/(?P<slug>[a-zA-Z0-9-]+)/items/$', spideritems, name="stato"),
    #
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^avatar/', include('avatar.urls')),
   
   
   ##
)
