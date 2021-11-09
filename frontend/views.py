import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from backend.models import Session, User

# Create your views here.
def new(request, *args, **kwargs):
    if request.method != 'GET':
        return render(request, 'frontend/error.html', { "error": "GET method required for creating a session." })

    host = User.create()

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

@csrf_exempt
def post(request, *args, **kwargs):
    if request.method != 'POST':
        return render(request, 'frontend/error.html', { "error": "POST method required for posting changes." })

    jsondecoded = json.loads(request.body)
    sessionId = jsondecoded["sessionId"]
    userId = jsondecoded["userId"]
    
    if data not in jsondecoded:
        return render(request, 'frontend/error.html', { "error": "No data posted." })

    fileSubmitted = jsondecoded["content"]

    user = User.objects.all().filter(userId == userId, session__sessionId == sessionId)
    message = user.write(fileSubmitted)

    context = {
        "message": message 
    }
    return render(request, 'frontend/success.html', context)
