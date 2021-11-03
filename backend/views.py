from django.shortcuts import render

# Create your views here.
def post(request, args, kwargs**):
    if request.method != "POST":
        return render(request, 'frontend/error.html', { 'message': "POST method required when sending files." })
    file = 
    return render(request, 'frontend/success.html', {})

def get(request, *args, **kwargs):


