from django.shortcuts import render
import backend.Interface as backend

# Create your views here.
def get(request, *args, **kwargs):
    sessionId = "123"
    
    context = {
        "content": backend.getContent(sessionId)
    }

    return render(request, 'frontend/view_file.html', context)

def post(request, *args, **kwargs):
    if request.method != 'POST':
        return render(request, 'frontend/error.html', { "error": "POST method required for posting changes." })

    sessionId = "123"
    userId = "456"
    
    if data not in request.POST:
        return render(request, 'frontend/error.html', { "error": "No data posted." })

    fileSubmitted = request.POST["data"]
    
    message = backend.postContent(sessionId, userId, fileSubmitted)

    context = {
        "message": message 
    }
    return render(request, 'frontend/success.html', context)
