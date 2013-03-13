from deloslib.users.models import DelosApplication, DelosSite
from django.contrib.sites.models import get_current_site

class UserMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            try:
                request.unidade = request.user.unidade
            except:
                request.unidade = None
            request.apps = request.user.get_possible_apps()
        else:
            request.apps = DelosApplication.objects.filter(is_public=True).values()
        
        request.app = None
        for app in request.apps:
            if app['url'] in request.get_full_path():
                request.app = app
        

def user_context(request):
    try:
        unidade = request.unidade
        person = request.user
        user = request.user
    except:
        user = person = unidade = None
    app = request.app
    apps = request.apps
    #request.session.set_expiry(365*24*60*60) # one year
    request.session.set_expiry(12*60*60) # half day
    
    current_site = get_current_site(get_current_site)
    delossites = current_site.delossite_set.all()
#    import pdb; pdb.set_trace()
    if delossites:
        delossite = delossites[0]
    else:
        delossite = None
    return { 'user': user, 
            'unidade': unidade,
            'person': person,
            'app': app,
            'apps': apps,
            'delossite': delossite,
            }
    
