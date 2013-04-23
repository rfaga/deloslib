from deloslib.users.models import DelosApplication, DelosSite
from django.contrib.sites.models import get_current_site
from django.conf import settings

from django.utils.cache import patch_vary_headers
from django.utils import translation



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
        user = request.user
    except:
        user = unidade = None
    app = request.app
    apps = request.apps
    time = getattr(settings, 'EXPIRY_SESSION_TIME', 12*60*60)
    
    current_site = get_current_site(get_current_site)
    delossites = current_site.delossite_set.all()
#    import pdb; pdb.set_trace()
    if delossites:
        delossite = delossites[0]
    else:
        delossite = None
    return { 'user': user, 
            'unidade': unidade,
            'person': user,
            'app': app,
            'apps': apps,
            'delossite': delossite,
            }
    





class SessionBasedLocaleMiddleware(object):
    """
    This Middleware saves the desired content language in the user session.
    The SessionMiddleware has to be activated.
    """
    def process_request(self, request):
        if request.method == 'GET' and 'lang' in request.GET:
                language = request.GET['lang']
                request.session['language'] = language
        elif 'language' in request.session:
                language = request.session['language']
        else:
                language = translation.get_language_from_request(request)
        
        for lang in settings.LANGUAGES:
            if lang[0] == language:
                translation.activate(language)
                
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response