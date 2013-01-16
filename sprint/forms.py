from django import forms
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.forms.widgets import Input
from django.template.loader import render_to_string


class EmailInput(Input):
    input_type = 'email'

class LetterForm(forms.Form):
    sender = forms.EmailField(label='Your email', widget=EmailInput())
    subject = forms.CharField(label='Subject')
    text = forms.CharField(label='Message', widget=forms.Textarea())

    def deliver(self):
        self.is_valid()
        msg = EmailMessage(to=[mngr[1] for mngr in settings.MANAGERS])
        msg.subject = self.cleaned_data['subject']
        msg.extra_headers = {'Reply-To': self.cleaned_data['sender']}
        msg.body = render_to_string('contact_email.txt', self.cleaned_data)
        msg.send()


