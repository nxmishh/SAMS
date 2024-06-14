from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
from .camera import VideoCamera

# Create your views here.

# def index(response):
#     return HttpResponse("<h1 > Hello World !</h1>")

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def login(response):
    return render(response, "main/login.html", {})

def base(response):
    return render(response, "main/base.html", {})

def home(response):
    return render(response, "main/home.html", {})

def monitor(response):
    return render(response, "main/monitor.html", {})

def logger(response):
    return render(response, "main/logger.html", {})

def profile(response):
    return render(response, "main/profile.html", {})
