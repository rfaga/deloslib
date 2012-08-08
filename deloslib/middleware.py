
class UserMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            try:
                profile = request.user.get_profile()
                request.unidade = profile.unidade
                request.person = profile
            except:
                request.person = None
                request.unidade = None
        

def user_context(request):
    try:
        unidade = request.unidade
        person = request.person
        user = request.user
    except:
        user = person = unidade = None
    
    #request.session.set_expiry(365*24*60*60) # one year
    request.session.set_expiry(12*60*60) # half day
    
    return { 'user': user, 
            'unidade': unidade,
            'person': person}
    
