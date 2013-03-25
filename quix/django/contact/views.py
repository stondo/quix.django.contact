from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.utils.importlib import import_module

# TEMPLATES = {"full": "checkout/billingaddress.html",
#           "mobile": "checkout/paymentmethod.html"}

# import contact form class based on value in settings.py
full_class = getattr(settings, 'CONTACT_FORM_CLASS', 'quix.django.contact.forms.ContactForm')
module_name = '.'.join(full_class.split('.')[0:-1])
module = import_module(module_name)
class_instance = getattr(module, full_class.split('.')[-1])

class ContactView(FormView):
#    if request.session['flavour'] == 'full':
#        template_name = getattr(settings, 'CONTACT_FORM_TEMPLATE', 'contact/form.html')
#        success_url = reverse_lazy("contact-success")
#    elif request.session['flavour'] == 'mobile':
#        template_name = getattr(settings, 'CONTACT_FORM_MOBILE_TEMPLATE', 'contact/mobileForm.html')
#        success_url = reverse_lazy("contact-mobileSuccess")
#    else:
#        template_name = getattr(settings, 'CONTACT_FORM_TEMPLATE', 'contact/form.html')
#        success_url = reverse_lazy("contact-success")

    form_class = class_instance


    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)


    def get_success_url(self):
        if self.request.COOKIES.get('flavour') == 'full':
            return reverse_lazy("contact-success")
        elif self.request.COOKIES.get('flavour') == 'mobile':
            return reverse_lazy("contact-mobileSuccess")
        else:
            return reverse_lazy("contact-success")


    def get_template_names(self):
        if self.request.COOKIES.get('flavour') == 'full':
            return getattr(settings, 'CONTACT_FORM_TEMPLATE', 'contact/form.html')
        elif self.request.COOKIES.get('flavour') == 'mobile':
            return getattr(settings, 'CONTACT_FORM_MOBILE_TEMPLATE', 'contact/mobileForm.html')
        else:
            return getattr(settings, 'CONTACT_FORM_TEMPLATE', 'contact/form.html')

