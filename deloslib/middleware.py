from deloslib.users.models import DelosApplication


class UserMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            try:
                request.unidade = profile.unidade
                request.person = profile
            except:
                request.person = None
                request.unidade = None
            request.apps = profile.get_possible_apps()
        else:
            request.apps = DelosApplication.objects.filter(is_public=True).values()
        request.app = None
        for app in request.apps:
            if app['url'] in request.get_full_path():
                request.app = app
        

def user_context(request):
    try:
        unidade = request.unidade
        person = request.person
        user = request.user
    except:
        user = person = unidade = None
    app = request.app
    apps = request.apps
    #request.session.set_expiry(365*24*60*60) # one year
    request.session.set_expiry(12*60*60) # half day
    
    return { 'user': user, 
            'unidade': unidade,
            'person': person,
            'app': app,
            'apps': apps,
            }
    
