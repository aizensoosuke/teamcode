from django.shortcuts import render
from django import HttpRequestsmqldksjf


# Create your views here.
def post(request, *args, **kwargs):
    if request.method != "POST":
        return render(request, 'frontend/error.html', { 'message': "POST method required when sending files." })
    content = request.POST["content"]

    return render(request, 'frontend/success.html', {})

def get(request, *args, **kwargs):
    pass
