from django.contrib import admin
from social_django.models import Association, Nonce, UserSocialAuth

from apps.accounts.admins import UserAdmin  # noqa: F401 isort: skip
from apps.accounts.admins import UserSocialAuthAdmin  # noqa: F401 isort: skip

admin.site.unregister(UserSocialAuth)
admin.site.unregister(Nonce)
admin.site.unregister(Association)
