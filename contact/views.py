from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    # (после успешн сраб формы) будет перенаправлять на "главную"
    success_url = "/" 