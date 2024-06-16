import io
from django.shortcuts import render, redirect
from django.http import HttpResponse,StreamingHttpResponse, JsonResponse
import pandas as pd
import csv
import requests
from .ipcamera import VideoIPCamera
from .camera import VideoCamera
from django.contrib.auth import authenticate, login as auth_login
from .forms import CSVUploadForm
from datetime import datetime
from io import StringIO


# Create your views here.

# def index(response):
#     return HttpResponse("<h1 > Hello World !</h1>")

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(VideoIPCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def fetch_csv(request):
    # Replace the URL with the actual URL of the CSV file on your private network
    url = 'http://192.168.63.103:8000/alerts'
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the CSV content from the response
        csv_content = response.content.decode('utf-8')
        csv_reader = csv.reader(StringIO(csv_content))
        
        # Create a new CSV content in the desired format
        output = StringIO()
        csv_writer = csv.writer(output)
        
        # Write the header
        csv_writer.writerow(['timestamp', 'details', 'alert_message'])
        
        # Process each row from the original CSV
        for row in csv_reader:
            # Assuming the original CSV has the necessary fields in the correct order,
            # we need to transform them. Let's assume the original CSV fields are:
            # [timestamp, details, alert_message]
            # Convert the timestamp to the desired format if necessary
            timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H.%M')
            details = row[1]
            alert_message = row[2]
            
            # Write the transformed row to the new CSV
            csv_writer.writerow([timestamp, details, alert_message])
        
        # Create the HttpResponse object with the appropriate CSV header.
        response_content = HttpResponse(output.getvalue(), content_type='text/csv')
        response_content['Content-Disposition'] = 'attachment; filename="fetched_record.csv"'

        return response_content
    else:
        return HttpResponse("Failed to fetch CSV file.", status=400)

def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            records = [row for row in reader]
            return render(request, 'main/display_csv.html', {'records': records})
    else:
        form = CSVUploadForm()
    return render(request, 'main/upload_csv.html', {'form': form})
    


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'registration/login.html')

def login(response):
    return render(response, "registration/login.html", {})

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
