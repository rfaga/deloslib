from django.contrib.auth.models import check_password
from deloslib.users.models import UserAccount

class EmailAuthBackend(object):
    """
    Email Authentication Backend
    
    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """
    
    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = UserAccount.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserAccount.DoesNotExist:
            try:
                user = UserAccount.objects.get(identification=username)
                if user.check_password(password):
                    return user
            except UserAccount.DoesNotExist:       
                return None 

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return UserAccount.objects.get(pk=user_id)
        except UserAccount.DoesNotExist:
            return None