# pages/views.py
from django.shortcuts import render

def home_page_view(request):
    # 'render' combines the request, the template, and an optional data dictionary
    return render(request, "home.html")
