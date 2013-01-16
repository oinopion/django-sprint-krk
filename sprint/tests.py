from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from sprint.forms import LetterForm

data = {
    'sender': 'alice@example.com',
    'subject': 'A famous Quote',
    'text': 'Hello, world!'
}

class LetterFormTest(TestCase):
    def test_requires_sender_subject_text(self):
        form = LetterForm({})
        for field in 'sender subject text'.split():
            self.assertIn(field, form.errors)

    def test_is_valid_with_data(self):
        form = LetterForm(data)
        self.assertTrue(form.is_valid())

    def test_devliver_send_email(self):
        form = LetterForm(data)
        form.deliver()
        self.assertEqual(1, len(mail.outbox))

    def test_deliver_sets_subject(self):
        form = LetterForm(data)
        form.deliver()
        self.assertEqual(mail.outbox[0].subject, data['subject'])

    def test_delivers_message_unchanged(self):
        form = LetterForm(data)
        form.deliver()
        self.assertIn(data['text'], mail.outbox[0].body)

    def test_sets_sender_as_reply_to(self):
        form = LetterForm(data)
        form.deliver()
        self.assertIn(data['sender'], mail.outbox[0].extra_headers['Reply-To'])

    def test_uses_template(self):
        form = LetterForm(data)
        form.deliver()
        self.assertTrue(mail.outbox[0].body.startswith('A new inquiry:'))


class ContactFormViewTest(TestCase):
    url = '/contact'

    def test_get_is_ok(self):
        resp = self.client.get(self.url)
        self.assertEqual(200, resp.status_code)

    def test_renders_contact_template(self):
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, 'contact.html')

    def test_form_present(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, '<form ')

    def test_post_sends_email(self):
        resp = self.client.post(self.url, data)
        self.assertEqual(1, len(mail.outbox))

    def test_post_redirects_to_done(self):
        resp = self.client.post(self.url, data)
        self.assertRedirects(resp, reverse('contact_done'))

