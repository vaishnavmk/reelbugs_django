from django.contrib.auth.models import User

class EmailAuthenticationBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            user=User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return  User.objects.get(pk=user_id)
        except UserDoesNotExist:
            return None

def get_avatar(backend, strategy, details, response,
        user=None, is_new=False, *args, **kwargs):
    url = None
    if is_new and backend.name == 'facebook':
        url = "https://graph.facebook.com/%s/picture?type=large"%response['id']
    if is_new and backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal','')
    if is_new and backend.name == 'google-oauth2':
        url = response['image'].get('url')
        ext = url.split('.')[-1]
    if url:
        user.person.avatar = url
        user.person.gen_thumb(url)
        user.person.save()