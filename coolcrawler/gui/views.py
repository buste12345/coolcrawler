from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.views.generic import DetailView
from gui.forms import CommentForm
from django.views.generic.detail import SingleObjectMixin 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from gui.basicfunctions import returno, returnosp, getsites, returnosites, geturls, runspider, spiderstatus, returnspider, spiderjobs
from scraperfunc.models import NewsWebsite, NewsWebsiteForm, UrlsForm, ProxyForm, UserAgentForm
from django.shortcuts import render
from slugify import slugify
class PostDetailView(DetailView):
    methods = ['get', 'post']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(object=self.object)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(object=self.object, data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())

        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)
        
#def MainSiteView(resquest):
    #return HttpResponse("Hello, world. You're at the polls index.")
 #   render_to_response('AdmintLTE/index.html')
 
def my_view(request):
    #username = request.POST.get('username', False);
    #password = request.POST.get('password', False);
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print 'Returned1'
                return render_to_response('AdmintLTE/starter.html') 
            else:
                print 'Returned2'
                return HttpResponse("Error")
        else:
            print 'Returned3'
            return render_to_response('registration/login.html')
    else:
        print 'Returned4'
        return render_to_response('registration/login.html')
    

#def foo(request):
#    r = tasks.add.delay(2, 2)
#    return HttpResponse(r.task_id)

@login_required
def logged_in(request):
    return render_to_response('AdminLTE/starter.html',
        context_instance=RequestContext(request)
    )
    
@login_required
def entrypoint(request):
    return render_to_response('AdminLTE/subpagess/entryp.html',
    {'result': returno()},
    context_instance=RequestContext(request)
    )

@login_required
def seewebs(request):
    if(request.POST.get('runspider')):
        runspider( int(request.POST.get('runspider')) )
    
    return render_to_response('AdminLTE/subpagess/webs.html',
    {'result': getsites('profs')},
    context_instance=RequestContext(request)
    )

@login_required
def seeurls(request):
    return render_to_response('AdminLTE/subpagess/surls.html',
    {'result': geturls('urls')},
    context_instance=RequestContext(request)
    )
    
@login_required
def checkstatus(request):
    return render_to_response('AdminLTE/subpagess/checkspiderstatus.html',
    #return render_to_response('AdminLTE/subpagess/scrapydgui.html',
    {'result': spiderstatus()
    #,'jobbies':spiderjobs()
    },
    context_instance=RequestContext(request)
    )

@login_required
def add_urls(request):
    if request.method == 'POST':
        form = UrlsForm(request.POST)
        if form.is_valid():
            new_site = form.save()

            return HttpResponseRedirect(reverse('urlsview'))
    else:
        form = UrlsForm()

    return render(request, 'AdminLTE/subpagess/addurl.html', {'form': form})

@login_required
def seeadvset(request):
    if request.method == 'POST':
        formproxy = ProxyForm(request.POST)
        formagents = UserAgentForm(request.POST)
        if formproxy.is_valid() and formagents.is_valid():
            new_site1 = formproxy.save()
            new_site2 = formagents.save()
            
            return HttpResponseRedirect(reverse('urlsview'))
    else:
        formproxy = ProxyForm(request.POST)
        formagents = UserAgentForm(request.POST)

    return render(request, 'AdminLTE/subpagess/advancesettings.html', {'proxys': formproxy, 'usera':formagents})

@login_required
def entrypointdet(request,slug):
    return render_to_response('AdminLTE/subpagess/entrypdet.html',
    {'result': returnosp(slug)},
    context_instance=RequestContext(request)
    )    

@login_required
def webdet(request,slug):
    print 'uck'
    return render_to_response('AdminLTE/subpagess/websdet.html',
    {'result': returnosites(slug)},
    context_instance=RequestContext(request)
    )    

@login_required
def statusget(request,slug):
    #print 'uck'
    #print request
    #print slug
    return render_to_response('AdminLTE/subpagess/statusdet.html',
    {'result': returnspider(slug)},
    context_instance=RequestContext(request)
    )   

@login_required
def spideritems(request,slug):
    #print 'uck'
    #print request
    #print slug
    return render_to_response('AdminLTE/subpagess/statusdet.html',
    {'result': spiderjobs(slug)},
    context_instance=RequestContext(request)
    )   

@login_required
def test11(request):
    return HttpResponse('TEST LOGGED')
    
@login_required
def add_site(request):
    if request.method == 'POST':
        form = NewsWebsiteForm(request.POST)
        if form.is_valid():
            new_site = form.save()

            return HttpResponseRedirect(reverse('sitesview'))
    else:
        form = NewsWebsiteForm()

    return render(request, 'AdminLTE/subpagess/addsite2.html', {'form': form})