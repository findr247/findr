from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _

# from main.models import Collection, ShippingMethod


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password for a staff account. Note that both "
            "fields may be case-sensitive."
        ), "inactive": _("This account is inactive.")}
