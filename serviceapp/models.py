from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Person(models.Model):
    image = models.ImageField(upload_to='img')
    name = models.CharField(max_length=200)
    isactive = models.BooleanField()



@receiver(pre_delete, sender=Person)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    try:
        instance.image.delete(False)
    except: pass