from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    # Use Django's built-in form
    form_class = UserCreationForm 
    # Redirect to the login page upon successful registration
    success_url = reverse_lazy("login") 
    # The template we will create next
    template_name = "registration/signup.html"
