# coding=UTF-8

from django.conf import settings
from django import forms
from django.core.mail import send_mail
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string

#from django.forms.widgets import Select


PROVINCE = (('AG', 'AGRIGENTO'), ('AL', 'ALESSANDRIA'), ('AN', 'ANCONA',), ('AO', 'AOSTA',), ('AR', 'AREZZO',), ('AP', 'ASCOLI PICENO',), ('AT', 'ASTI',), ('AV', 'AVELLINO',), ('BA', 'BARI',), ('BT','Barletta-Andria-Trani',), ('BL', 'BELLUNO',), ('BN', 'BENEVENTO',), ('BG','BERGAMO',), ('BI', 'BIELLA',), ('BO', 'BOLOGNA',), ('BZ','BOLZANO',), ('BS','BRESCIA',), ('BR','BRINDISI',), ('CA','CAGLIARI',), ('CL','CALTANISSETTA',), ('CB','CAMPOBASSO',), ('CI','Carbonia-Iglesias',), ('CE','CASERTA',), ('CT','CATANIA',), ('CZ','CATANZARO',), ('CH','CHIETI',), ('CO','COMO',), ('CS','COSENZA',), ('CR','CREMONA',), ('KR','CROTONE',), ('CN','CUNEO',), ('EN','ENNA',), ('FM','FERMO',), ('FE','FERRARA',), ('FI','FIRENZE',), ('FG','FOGGIA',), ('FC','FORLI’-CESENA',), ('FR','FROSINONE',), ('GE','GENOVA',), ('GO','GORIZIA',), ('GR','GROSSETO',), ('IM','IMPERIA',), ('IS','ISERNIA',), ('SP','LA SPEZIA',), ('AQ','L’AQUILA',), ('LT','LATINA',), ('LE','LECCE',), ('LC','LECCO',), ('LI','LIVORNO',), ('LO','LODI',), ('LU','LUCCA',), ('MC','MACERATA',), ('MN','MANTOVA',), ('MS','MASSA-CARRARA',), ('MT','MATERA',), ('VS',' MEDIO CAMPIDANO',), ('ME','MESSINA',), ('MI','MILANO',), ('MO','MODENA',), ('MB','MONZA E DELLA BRIANZA',), ('NA','NAPOLI',), ('NO','NOVARA',), ('NU','NUORO',), ('OG','OGLIASTRA',), ('OT','OLBIA-TEMPIO',), ('OR','ORISTANO',), ('PD','PADOVA',), ('PA','PALERMO',), ('PR','PARMA',), ('PV','PAVIA',), ('PG','PERUGIA',), ('PU','PESARO E URBINO',), ('PE','PESCARA',), ('PC','PIACENZA',), ('PI','PISA',), ('PT','PISTOIA',), ('PN','PORDENONE',), ('PZ','POTENZA',), ('PO','PRATO',), ('RG','RAGUSA',), ('RA','RAVENNA',), ('RC','REGGIO DI CALABRIA',), ('RE','REGGIO NELL’EMILIA',), ('RI','RIETI',), ('RN','RIMINI',), ('RM','ROMA',), ('RO','ROVIGO',), ('SA','SALERNO',), ('SS','SASSARI',), ('SV','SAVONA',), ('SI','SIENA',), ('SR','SIRACUSA',), ('SO','SONDRIO',), ('TA','TARANTO',), ('TE','TERAMO',), ('TR','TERNI',), ('TO','TORINO',), ('TP','TRAPANI',), ('TN','TRENTO',), ('TV','TREVISO',), ('TS','TRIESTE',), ('UD','UDINE',), ('VA','VARESE',), ('VE','VENEZIA',), ('VB','VERBANO-CUSIO-OSSOLA',), ('VC','VERCELLI',), ('VR','VERONA',), ('VV','VIBO VALENTIA',), ('VI','VICENZA',), ('VT','VITERBO',))

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, label="Nome", required=True)
    last_name = forms.CharField(max_length=50, label="Cognome", required=True)
    address = forms.CharField(max_length=50, label="Indirizzo", required=True)
    city = forms.CharField(max_length=50, label="Città", required=True)
    cap = forms.CharField(max_length=5, label="C.A.P.", required=True)
#    provincia = forms.CharField(max_length=2, label="Provincia")
    provincia = forms.ChoiceField(widget=forms.Select, choices=PROVINCE, label="Provincia")
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
    
