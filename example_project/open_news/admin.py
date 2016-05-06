from django.contrib import admin
from open_news.models import NewsWebsite, googlespider, URLs, genericmodel
from gui.models import entry

class NewsWebsiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url_', 'scraper')
    list_display_links = ('name',)
    
    def url_(self, instance):
        return '<a href="%s" target="_blank">%s</a>' % (instance.url, instance.url)
    url_.allow_tags = True
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'news_website', 'url_',)
    list_display_links = ('title',)
    raw_id_fields = ('checker_runtime',)
    
    def url_(self, instance):
        return '<a href="%s" target="_blank">%s</a>' % (instance.url, instance.url)
    url_.allow_tags = True



class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'monguito'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)

  
#class artadmin(MultiDBModelAdmin):
 #   list_display = articles._meta.get_all_field_names()
    #list_display = '_ID'
    
class googlespideradmin(MultiDBModelAdmin):
    list_display = googlespider._meta.get_all_field_names()
    #list_display = '_ID'

class entryadmin(MultiDBModelAdmin):
    list_display = entry._meta.get_all_field_names()
    #list_display = '_ID'


class generigadmin(MultiDBModelAdmin):
    list_display = ['uniqueid']
    #list_display = '_ID'

admin.site.register(URLs)
#admin.site.register(articles,artadmin)
admin.site.register(googlespider,googlespideradmin)
admin.site.register(NewsWebsite, NewsWebsiteAdmin)
admin.site.register(genericmodel, generigadmin)
admin.site.register(entry, entryadmin)
#admin.site.register(Article, ArticleAdmin)
