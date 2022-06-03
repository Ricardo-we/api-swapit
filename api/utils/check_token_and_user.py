# from api.models import User
from django.forms import ValidationError
from rest_framework.authtoken.models import Token

def check_user_and_token(user_id, token):
    user_token = Token.objects.get(user_id=user_id)
    token_ = Token.objects.get(key=token.split('Token')[1].strip())
    if user_token.key != token_.key: raise ValidationError('Invalid token or userid')
    return True
        