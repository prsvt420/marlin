from django import forms
from django.contrib.auth import get_user_model


class ProfileForm(forms.ModelForm):
    """Form for editing profile."""

    class Meta:  # noqa: D106
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "middle_name")
