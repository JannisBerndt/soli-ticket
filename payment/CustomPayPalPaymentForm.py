#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from warnings import warn

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from paypal.standard.conf import (
    BUY_BUTTON_IMAGE, DONATION_BUTTON_IMAGE, PAYPAL_CERT, PAYPAL_CERT_ID, PAYPAL_PRIVATE_CERT, PAYPAL_PUBLIC_CERT,
    POSTBACK_ENDPOINT, SANDBOX_POSTBACK_ENDPOINT, SUBSCRIPTION_BUTTON_IMAGE
)
from paypal.standard.widgets import ValueHiddenInput
from paypal.utils import warn_untested

log = logging.getLogger(__name__)

class CustomPayPalPaymentForm(forms.Form):
    """
    Creates a PayPal Payments Standard "Buy It Now" button, configured for a
    selling a single item with no shipping.

    For a full overview of all the fields you can set (there is a lot!) see:
    http://tinyurl.com/pps-integration

    Usage:
    >>> f = PayPalPaymentsForm(initial={'item_name':'Widget 001', ...})
    >>> f.render()
    u'<form action="https://www.paypal.com/cgi-bin/webscr" method="post"> ...'

    """
    CMD_CHOICES = (
        ("_xclick", "Buy now or Donations"),
        ("_donations", "Donations"),
        ("_cart", "Shopping cart"),
        ("_xclick-subscriptions", "Subscribe"),
        ("_xclick-auto-billing", "Automatic Billing"),
        ("_xclick-payment-plan", "Installment Plan"),
    )
    SHIPPING_CHOICES = ((1, "No shipping"), (0, "Shipping"))
    NO_NOTE_CHOICES = ((1, "No Note"), (0, "Include Note"))
    RECURRING_PAYMENT_CHOICES = (
        (1, "Subscription Payments Recur"),
        (0, "Subscription payments do not recur")
    )
    REATTEMPT_ON_FAIL_CHOICES = (
        (1, "reattempt billing on Failure"),
        (0, "Do Not reattempt on failure")
    )

    BUY = 'buy'
    SUBSCRIBE = 'subscribe'
    DONATE = 'donate'

    # Default fields.
    cmd = forms.ChoiceField(widget=forms.HiddenInput(), initial=CMD_CHOICES[0][0])
    charset = forms.CharField(widget=forms.HiddenInput(), initial="utf-8")
    currency_code = forms.CharField(widget=forms.HiddenInput(), initial="USD")
    no_shipping = forms.ChoiceField(widget=forms.HiddenInput(), choices=SHIPPING_CHOICES,
                                    initial=SHIPPING_CHOICES[0][0])

    def __init__(self, button_type="buy", *args, **kwargs):
        super(CustomPayPalPaymentForm, self).__init__(*args, **kwargs)
        self.button_type = button_type
        if 'initial' in kwargs:
            kwargs['initial'] = self._fix_deprecated_return_url(kwargs['initial'])
            # Dynamically create, so we can support everything PayPal does.
            for k, v in kwargs['initial'].items():
                if k not in self.base_fields:
                    self.fields[k] = forms.CharField(label=k, widget=ValueHiddenInput(), initial=v)

    def _fix_deprecated_return_url(self, initial_args):
        if 'return_url' in initial_args:
            warn("""The use of the initial['return_url'] is Deprecated.
                    Please use initial['return'] instead""", DeprecationWarning)
            initial_args['return'] = initial_args['return_url']
            del initial_args['return_url']
        return initial_args

    def test_mode(self):
        return getattr(settings, 'PAYPAL_TEST', True)

    def get_endpoint(self):
        "Returns the endpoint url for the form."
        if self.test_mode():
            return SANDBOX_POSTBACK_ENDPOINT
        else:
            return POSTBACK_ENDPOINT

    def render(self):
        return format_html(u"""<form action="{0}" method="post">
    {1}
    <input type="submit" value="Mit Paypal Zahlen" data-wait="Please wait..." class="submit-button w-button" name ="post" formmethod="post">
</form>""", self.get_endpoint(), self.as_p(), self.get_image())

    def get_image(self):
        return {
            self.SUBSCRIBE: SUBSCRIPTION_BUTTON_IMAGE,
            self.BUY: BUY_BUTTON_IMAGE,
            self.DONATE: DONATION_BUTTON_IMAGE,
        }[self.button_type]

    def is_transaction(self):
        warn_untested()
        return not self.is_subscription()

    def is_donation(self):
        warn_untested()
        return self.button_type == self.DONATE

    def is_subscription(self):
        warn_untested()
        return self.button_type == self.SUBSCRIBE
