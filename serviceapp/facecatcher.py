import os
import cv2
from serviceapp import modelapi
from serviceapp.models import Person
from serviceapp.deepfaceapi import initializatedb

def rewindEmbeddings():
    try:
        os.remove("media/representations_facenet512.pkl")
        modelapi.initializate("media", model_name="Facenet512", detector_backend="opencv",
                          distance_metric="euclidean",
                          enable_face_analysis=False, time_threshold=1, frame_threshold=1)
    except:
        modelapi.initializate("media", model_name="Facenet512", detector_backend="opencv",
                              distance_metric="euclidean",
                              enable_face_analysis=False, time_threshold=1, frame_threshold=1)

def facecatch(image):
    try:
        status, person = modelapi.analysis("media", image, model_name="Facenet512", detector_backend="opencv",
                                           distance_metric="euclidean",
                                           enable_face_analysis=False, time_threshold=1, frame_threshold=1)
        if status:
            name = person.split('/')[-1]
            list_of_persons = Person.objects.all()
            for person in list_of_persons:
                asd = person.image.url.split('/')[-1]
                if asd == name:
                    print(person.name)
        else:
            print("Unknown person")
        return status
    except:
        return None


def highlightFaces(frame, userAccess):
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    length0 = frame.shape[1]
    length1 = frame.shape[0]
    #
    # faces = faceCascade.detectMultiScale(
    #     gray,
    #     scaleFactor=1.1,
    #     minNeighbors=5,
    #     minSize=(30, 30)
    # )
    #
    # for (x, y, w, h) in faces:
    #     if userAccess:
    #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
    #     elif userAccess is None:
    #         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 1)
    #     else:
    #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
    if userAccess:
        cv2.rectangle(frame, (0, length1 - 80), (length0 - 1, length1 - 1), (0, 255, 0), -1)  # 7
        cv2.putText(frame, "Access allowed", (30, length1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 3, 1)
    elif userAccess is not None:
        cv2.rectangle(frame, (0, length1 - 80), (length0 - 1, length1 - 1), (0, 0, 255), -1)  # 7
        cv2.putText(frame, "Access denied", (30, length1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 3, 1)

cascPath = "serviceapp/test.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
rewindEmbeddings()