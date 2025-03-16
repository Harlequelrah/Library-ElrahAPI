from .database import authentication
from myproject.authapp_user.models import User
from typing import Dict

from typing import Type
authentication.authentication_models = {
    'User': User,
}
authentication_router = authentication.get_auth_router()
