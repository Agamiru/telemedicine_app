from rest_framework.authentication import SessionAuthentication


# Do not enforce csrf_check
class CustomSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass