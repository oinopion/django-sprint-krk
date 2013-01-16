from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from sprint.forms import LetterForm


class ContactFormView(FormView):
    form_class = LetterForm
    template_name = 'contact.html'

    def form_valid(self, form):
        form.deliver()
        return redirect('contact_done')


home = TemplateView.as_view(template_name='home.html')
contact = ContactFormView.as_view()
contact_done = TemplateView.as_view(template_name='contact_done.html')
