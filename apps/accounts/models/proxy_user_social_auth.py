from django.utils.translation import gettext_lazy as _
from social_django.models import UserSocialAuth


class ProxyUserSocialAuth(UserSocialAuth):
    class Meta:
        proxy = True
        verbose_name = _("Social account")
        verbose_name_plural = _("Social accounts")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field("user").verbose_name = _("user")
        self._meta.get_field("provider").verbose_name = _("provider")
        self._meta.get_field("uid").verbose_name = _("identifier")
        self._meta.get_field("extra_data").verbose_name = _("extra data")
        self._meta.get_field("created").verbose_name = _("created date")
        self._meta.get_field("modified").verbose_name = _("updated date")
