from django.views.decorators import gzip
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse
import cv2
import numpy
from serviceapp.timer import Timer
from PIL import Image
from serviceapp.facecatcher import facecatch, highlightFaces, rewindEmbeddings
from django.views.decorators.csrf import csrf_exempt
from serviceapp.models import Person


class VideoCamera(object):

    def __init__(self):
        # self.video = cv2.VideoCapture('http://192.168.103.62:8080/video')
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        # threading.Thread(target=self.update, args=()).start()
        self.timer = Timer()
        self.timer.start()
        self.access = None

    def __del__(self):
        self.video.release()

    def get_frame(self):
        grabbed, image = self.video.read()
        # image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        if self.timer.elapseTime() >= 10:
            self.access = facecatch(image)
            self.timer.restart()
        if self.access is not None: highlightFaces(image, self.access)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def SetCookie(request, access):
    response = HttpResponse('Setting cookies')
    response.set_cookie("Access", access)
    return response


def works(request):
    return JsonResponse({"asd": request.COOKIES["Access"]})


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass


def cameraPage(request):
    return render(request, "testCamera.html")


def securitypage(request):
    return render(request, "securityPage.html")

def phoneCamera(request):
    return render(request, "phoneCamera.html")

@csrf_exempt
def checkFace(request):
    image = request.FILES["image"].file
    img = Image.open(image)
    width, height = img.size
    if height < width:
        img = img.rotate(270)
        img.save("test.jpg")
    img.load()
    final = numpy.array(img)
    response = facecatch(final)
    return JsonResponse({"access":response})

def database(request):
    context = {"persons":Person.objects.all()}
    return render(request, "databasePage.html", context)


def rewinddatabase(request):
    rewindEmbeddings()
    persons = Person.objects.all()
    for person in persons:
        Person.objects.filter(name=person.name).update(isactive=True)
    return redirect('/database')
