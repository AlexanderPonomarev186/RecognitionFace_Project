from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from PIL import Image
import numpy
from serviceapp.deepfaceapi import add_face_to_db


class Person(models.Model):
    image = models.ImageField(upload_to='img')
    name = models.CharField(max_length=200)
    isactive = models.BooleanField()

    def save(self, *args, **kwargs):
        file = self.image.file
        image = Image.open(file)
        image.load()
        img_list = numpy.array(image)
        add_face_to_db(img_list,
                       model_name="Facenet512",
                       detector_backend="retinaface",
                       enforce_detection=False,
                       silent=True, )
        super(Person, self).save(*args, **kwargs)


@receiver(pre_delete, sender=Person)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    try:
        instance.image.delete(False)
    except:
        pass
