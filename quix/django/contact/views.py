from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.utils.importlib import import_module

from django.http import HttpRequest

# import contact form class based on value in settings.py
full_class = getattr(settings, 'CONTACT_FORM_CLASS', 'quix.django.contact.forms.ContactForm')
module_name = '.'.join(full_class.split('.')[0:-1])
module = import_module(module_name)
class_instance = getattr(module, full_class.split('.')[-1])

class ContactView(FormView):
    if HttpRequest.session['flavour'] == 'full':
        template_name = getattr(settings, 'CONTACT_FORM_TEMPLATE', 'contact/form.html')
        success_url = reverse_lazy("contact-success")
    elif HttpRequest.session['flavour'] == 'mobile':
        template_name = getattr(settings, 'CONTACT_FORM_MOBILE_TEMPLATE', 'contact/mobileForm.html')
        success_url = reverse_lazy("contact-mobileSuccess")
    else:
        template_name = getattr(settings, 'CONTACT_FORM_TEMPLATE', 'contact/form.html')
        success_url = reverse_lazy("contact-success")

    form_class = class_instance


    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)
