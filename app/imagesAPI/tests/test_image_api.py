from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

import os

from ..models import Image, Comment
from ..serializers import CommentSerializer, ImageSerializer

IMAGES_URL = reverse('imagesAPI:image-list')
COMMENTS_URL = reverse('imagesAPI:comment-list')


def detail_url(image_id):
    return reverse('imagesAPI:image-detail', args=[image_id])


def comment_detail_url(comment_id):
    return reverse('imagesAPI:comment-detail', args=[comment_id])


one_pixel_image = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)


class ImageApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.image = SimpleUploadedFile(name='image.jpg', content=one_pixel_image, content_type='image/jpeg')

    def test_image_list(self):
        image_post1 = Image.objects.create(title='Test image 1', imagefile=self.image)
        image_post2 = Image.objects.create(title='Test image 2', imagefile=self.image)

        res = self.client.get(IMAGES_URL)

        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, 'Test image 1')
        self.assertContains(res, 'Test image 2')
        self.assertTrue(os.path.exists(image_post1.imagefile.path))
        self.assertTrue(os.path.exists(image_post2.imagefile.path))
        self.assertEqual(res.data[0]['title'], serializer.data[0]['title'])
        self.assertEqual(res.data[1]['title'], serializer.data[1]['title'])

    def test_image_detail(self):
        image_post = Image.objects.create(title='Test image 1', imagefile=self.image)
        image_post.comments.add(Comment.objects.create(name='testname', body='testbody', image_post=image_post))

        url = detail_url(image_post.id)
        res = self.client.get(url)

        serializer = ImageSerializer(image_post)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], serializer.data['title'])
        self.assertEqual(res.data['comments'][0], serializer.data['comments'][0])

    def test_create_image(self):
        data = {
            'title': 'Test image 777',
            'imagefile': self.image
        }
        res = self.client.post(IMAGES_URL, data)

        exists = Image.objects.filter(title=data['title']).exists()
        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_image(self):
        new_image = SimpleUploadedFile(name='new_image.jpg', content=one_pixel_image, content_type='image/jpeg')
        image_post = Image.objects.create(title='Test image 111', imagefile=new_image)
        data = {
            'title': 'Test image 555',
            'imagefile': self.image
        }
        url = detail_url(image_post.id)
        self.client.put(url, data)

        image_post.refresh_from_db()
        self.assertEqual(image_post.title, data['title'])


class CommentApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.image = SimpleUploadedFile(name='image.jpg', content=one_pixel_image, content_type='image/jpeg')
        self.image_model = Image.objects.create(title='Test image 100', imagefile=self.image)

    def test_comment_list(self):
        Comment.objects.create(name='YIL GUY', body='JOOOO BIDEN', image_post=self.image_model)
        Comment.objects.create(name='YIL GUY 2', body='JOOOOOO BIDEN', image_post=self.image_model)

        res = self.client.get(COMMENTS_URL)

        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, 'YIL GUY')
        self.assertContains(res, 'YIL GUY 2')
        self.assertEqual(res.data, serializer.data)

    def test_comment_detail(self):
        comment = Comment.objects.create(name='YIL GUY', body='JOOOO BIDEN', image_post=self.image_model)

        url = comment_detail_url(comment.id)
        res = self.client.get(url)

        serializer = CommentSerializer(comment)
        self.assertEqual(res.data, serializer.data)

    def test_create_comment(self):
        data = {
            'name': 'test name',
            'body': 'very good',
            'image_post': self.image_model.id
        }
        res = self.client.post(COMMENTS_URL, data)

        exists = Comment.objects.filter(name=data['name']).exists()
        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_comment(self):
        comment = Comment.objects.create(name='firstname surname', body='hello', image_post=self.image_model)
        data = {
            'body': 'hi'
        }
        url = comment_detail_url(comment.id)
        self.client.put(url, data)

        comment.refresh_from_db()
        self.assertEqual(comment.body, data['body'])
