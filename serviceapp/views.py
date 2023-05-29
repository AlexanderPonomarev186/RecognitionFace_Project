from django.views.decorators import gzip
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse
import cv2
import numpy
import pdb
from serviceapp.timer import Timer
from PIL import Image
from serviceapp.facecatcher import facecatch, highlightFaces
from django.views.decorators.csrf import csrf_exempt


class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture('http://192.168.31.225:8080/video')
        # self.video = cv2.VideoCapture(0)
        # (self.grabbed, self.frame) = self.video.read()
        # threading.Thread(target=self.update, args=()).start()
        self.timer = Timer()
        self.timer.start()
        self.access = None

    def __del__(self):
        self.video.release()

    def get_frame(self):
        grabbed, image = self.video.read()
        if self.timer.elapseTime() >= 10 and not self.access:
            self.access = facecatch(image)
            self.timer.restart()
            highlightFaces(image, self.access)
        # else: highlightFaces(image, self.access)
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