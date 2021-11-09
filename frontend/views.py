from django.shortcuts import render
from backend.models import Session, User

# Create your views here.
def new(request, *args, **kwargs):
    if request.method != 'GET':
        return render(request, 'frontend/error.html', { "error": "GET method required for creating a session." })

    host = User.create()
    host.save()

    context = {
        "sessionId": host.session.sessionId,
        "userId": host.userId
    }

    return render(request, 'frontend/new.html', context)

def get(request, *args, **kwargs):
    if request.method != 'GET':
        return render(request, 'frontend/error.html', { "error": "GET method required for getting file." })

    sessionId = request.GET["sessionId"]
    
    context = {
        "content": Session.objects.all().filter(sessionId == sessionId)[0].get()
    }

    return render(request, 'frontend/view_file.html', context)

def post(request, *args, **kwargs):
    if request.method != 'POST':
        return render(request, 'frontend/error.html', { "error": "POST method required for posting changes." })

    sessionId = request.POST["sessionId"]
    userId = request.POST["userId"]
    
    if data not in request.POST:
        return render(request, 'frontend/error.html', { "error": "No data posted." })

    fileSubmitted = request.POST["content"]
    
    user = User.objects.all().filter(userId == userId, session__sessionId == sessionId)
    message = user.write(fileSubmitted)
    user.save()

    context = {
        "message": message 
    }
    return render(request, 'frontend/success.html', context)
