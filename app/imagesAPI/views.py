from rest_framework import viewsets
from rest_framework.response import Response

import math

from .models import Comment, Image
from .serializers import ImageSerializer, CommentSerializer, CommentUpdateSerializer


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if hasattr(self, 'request') and self.request.method == 'PUT':
            serializer_class = CommentUpdateSerializer

        return serializer_class


class StatViewSet(viewsets.ViewSet):
    def list(self, request, format=None):
       image_queryset = Image.objects.all()
       unique_images = len({image.imagefile.size for image in image_queryset})
       size = sum(image.imagefile.size for image in image_queryset)

       comment_queryset = Comment.objects.all()
       unique_comments = Comment.objects.all().distinct('name', 'body', 'image_post')


       stats = {
           'images_total_count': image_queryset.count(), 
           'unique_images_count': unique_images,
           'images_total_size': convert_size(size),
           'comments_total_count': comment_queryset.count(), 
           'unique_comments_count': unique_comments.count(), 
       }
       return Response(stats)
