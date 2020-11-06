from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import CandidateSignUpForm, InstituteSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib.auth.decorators import login_required
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import pyautogui
import keyboard
import argparse
import tempfile
import queue
import sys
import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)


def home(request):
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow("preview")

    return render(request, 'index.html')


def search(request):
    return render(request, 'search.html')


def searchbar(request):
    if request.method=='GET':
        search=request.GET.get('search')
        post=User.objects.all().filter(username=search)
        return render(request,'searchbar.html',{'post':post})


def filter(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'filter.html', {'filter': user_filter})

# def register(request):
#     return render(request, 'register.html')


@login_required(login_url='login')
def dash(request):
    return render(request, 'dash.html')


class candidate_register(CreateView):
    model = User
    form_class = CandidateSignUpForm
    template_name = 'candidate_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')


class institute_register(CreateView):
    model = User
    form_class = InstituteSignUpForm
    template_name = 'institute_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('home2')
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"Invalid username or password")
    return render(request, 'login.html',context={'form':AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')

# def home(request):
#         return render(request, 'home.html')


def home2(request):
    def active():
        face_classifier = cv2.CascadeClassifier(
                      'C:/Users/harsh/AppData/Local/Programs/Python/Python38-32/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

        def face_extractor(img):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            if faces is ():
                return None
            for (x, y, w, h) in faces:
                cropped_face = img[y:y + h, x:x + w]

            return cropped_face

        cap = cv2.VideoCapture(0)
        count = 0
        while True:
            ret, frame = cap.read()
            if face_extractor(frame) is not None:
                count += 1
                face = cv2.resize(face_extractor(frame), (200, 200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                file_name_path = 'C:/Users/harsh/govhack/photos/user' + str(count) + '.jpg'
                cv2.imwrite(file_name_path, face)
                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Face Cropper', face)
            else:
                print("Face not found")
                pass
            if cv2.waitKey(1) == 13 or count == 60:
                break
        cap.release()
        cv2.destroyAllWindows()
        print("Collecting Samples Complete")
    active()
    return render(request, 'home2.html')


def home3(request):
    def front():
        data_path = 'C:/Users/harsh/govhack/photos/'
        onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
        Training_Data, Labels = [], []
        for i, files in enumerate(onlyfiles):
            image_path = data_path + onlyfiles[i]
            images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            Training_Data.append(np.asarray(images, dtype=np.uint8))
            Labels.append(i)
        Labels = np.asarray(Labels, dtype=np.int32)
        model = cv2.face.LBPHFaceRecognizer_create()
        model.train(np.asarray(Training_Data), np.asarray(Labels))
        print("Model trained successfully")
        face_classifier = cv2.CascadeClassifier('C:/Users/harsh/AppData/Local/Programs/Python/Python38-32/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

        def face_detector(img):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            if faces is ():
                return img, []
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi = img[y:y + h, x:x + w]
                roi = cv2.resize(roi, (200, 200))
            return img, roi

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            image, face = face_detector(frame)
            try:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                results = model.predict(face)
                if results[1] < 500:
                    confidence = int(100 * (1 - (results[1]) / 300))
                    display_string = str(confidence) + '% Confident it is User'
                cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 120, 150), 2)
                if confidence > 75:
                    cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Face Recognition', image)
                else:
                    cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow('Face Recognition', image)
            except Exception:
                cv2.putText(image, "No Face Found", (220, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Face Recognition', image)
                pass
            if cv2.waitKey(1) == 13:
                break
        cap.release()
        cv2.destroyAllWindows()

    front()
    def sfront():
        screen_size = (1920, 1080)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter("screen.avi", fourcc, 20.0, (screen_size))

        while True:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
            if cv2.waitKey(1) == ord("q"):
                break

    def key():
        while True:
            if keyboard.is_pressed('ctrl'):
                print("ctrl key is pressed")
                break
            if keyboard.is_pressed('alt'):
                print("alt key  is pressed")
                break
            if keyboard.is_pressed('shift'):
                print("shift key is pressed")
                break
            if keyboard.is_pressed('up'):
                print("up key is pressed")
                break
            if keyboard.is_pressed('down'):
                print("down key is pressed")
                break
            if keyboard.is_pressed('left'):
                print("left key is pressed")
                break
            if keyboard.is_pressed('right'):
                print("right key  is pressed")
                break
            if keyboard.is_pressed('esc'):
                print("esc key is pressed")
                break

    sfront()
    # speech()
    # audio()
    key()
    return render(request, 'home3.html')

def result(request):
    op1= int(request.POST['op1'])
    op2= int(request.POST['op2'])
    op3= int(request.POST['op3'])
    op4= int(request.POST['op4'])
    op5= int(request.POST['op5'])
    cor=0

    if(op1==3):
        cor+=1
    if (op2 == 3):
        cor += 1
    if (op3 == 4):
        cor += 1
    if (op4 == 2):
        cor += 1
    if (op5 == 1):
        cor += 1
    return render(request, 'result.html', {'result': cor})