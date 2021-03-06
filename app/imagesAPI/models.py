from django.db import models

import uuid
import os


def image_file_path(instance, filename):
    """Сгенерировать путь файла для изображения"""
    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join('uploads/image/', filename)


class Image(models.Model):
    title = models.CharField(max_length=255)
    imagefile = models.ImageField(upload_to=image_file_path)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=55)
    body = models.TextField()
    image_post = models.ForeignKey('Image', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
