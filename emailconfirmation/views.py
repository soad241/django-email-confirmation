from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect
from emailconfirmation.models import EmailConfirmation

def confirm_email(request, confirmation_key):
    confirmation_key = confirmation_key.lower()
    email_address = EmailConfirmation.objects.confirm_email(confirmation_key)
    messages.add_message(request, messages.INFO,
                         'Congrats, your email is confirmed!')
    return HttpResponseRedirect('/')
