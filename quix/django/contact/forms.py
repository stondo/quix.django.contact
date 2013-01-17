# coding=UTF-8

from django.conf import settings
from django import forms
from django.core.mail import send_mail
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, label="Nome", required=True)
    last_name = forms.CharField(max_length=50, label="Cognome", required=True)
    address = forms.CharField(max_length=50, label="Indirizzo", required=True)
    city = forms.CharField(max_length=50, label="Città", required=True)
    cap = forms.CharField(max_length=5, label="C.A.P.", required=True)
    provincia = forms.CharField(max_length=2, label="Provincia")
    tel = forms.CharField(max_length=30, label="Telefono")
    email = forms.EmailField(max_length=100, required=True)
    subject = forms.CharField(max_length=100, label="Oggetto")
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}), max_length=500, label="Messaggio")
    
    def send_email(self):
        """
        Send contact form as an email to the address specified in the
        CONTACT_EMAILS setting.
        """
        from_email = self.cleaned_data['email']
        if not hasattr(settings, 'CONTACT_EMAILS'):
            raise ImproperlyConfigured("You need to specify CONTACT_EMAILS in "
                                       "your Django settings file.")
        to_emails = settings.CONTACT_EMAILS
        subject = self.cleaned_data['subject']
        template_name = getattr(settings, 'CONTACT_EMAIL_TEMPLATE', 
                                'contact/email.txt')
        message = render_to_string(template_name, self.cleaned_data)
        
        send_mail(subject, message, from_email, to_emails)
    
