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

from paypal.standard.forms import PayPalPaymentsForm

class CustomPayPalPaymentForm(PayPalPaymentsForm):
    
    def customRender(self):
        return format_html(u"""<form action="{0}" method="post">
    {1}
    <input type="submit" value="Mit Paypal Zahlen" data-wait="Please wait..." class="submit-button w-button" name ="post" formmethod="post">
</form>""", self.get_endpoint(), self.as_p(), self.get_image())

    